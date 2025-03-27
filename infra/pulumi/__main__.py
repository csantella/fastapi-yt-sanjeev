import os
import pulumi
import pulumi_aws as aws
from pulumi import Config

LOCAL_IP = os.environ.get('LOCAL_IP', '0.0.0.0')

# Configuration
config = Config()
vpc_id = config.get("vpc_id") or "vpc-08fa77c93020e0090"

# 1. Create ECR Repository
ecr_repo = aws.ecr.Repository("fastapi-repo",
    name="fastapi-yt-tutorial",
    image_tag_mutability="MUTABLE",
    image_scanning_configuration=aws.ecr.RepositoryImageScanningConfigurationArgs(
        scan_on_push=True
    ))

# 2. Network Setup
vpc = aws.ec2.get_vpc(id=vpc_id)
subnets = aws.ec2.get_subnets(filters=[aws.ec2.GetSubnetsFilterArgs(
    name="vpc-id",
    values=[vpc.id]
)])

# 3. Security Group
app_sg = aws.ec2.SecurityGroup("fastapi-sg",
    vpc_id=vpc.id,
    description="FastAPI Security Group",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp", from_port=80, to_port=80, cidr_blocks=["0.0.0.0/0"]
        )
    ])

# 4. ECS Cluster
cluster = aws.ecs.Cluster("fastapi-cluster")

# 5. ECS Task Execution Role
ecs_task_execution_role = aws.iam.Role("ecsTaskExecutionRole",
    assume_role_policy=pulumi.Output.json_dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Effect": "Allow"
        }]
    }))

# 6. Attach policy to role
aws.iam.RolePolicyAttachment("ecsTaskExecutionPolicy",
    role=ecs_task_execution_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy")

# Get the official ECS-optimized Amazon Linux 2023 AMI
ecs_optimized_ami = aws.ec2.get_ami(
    owners=["amazon"],
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["al2023-ami-ecs-*-x86_64"]
        )
    ],
    most_recent=True
).id

launch_template = aws.ec2.LaunchTemplate("ecs-launch-template",
    image_id=ecs_optimized_ami,  # Official ECS-optimized AMI
    instance_type="t2.micro",  # Instance type defined here
    vpc_security_group_ids=[app_sg.id],
    iam_instance_profile=aws.ec2.LaunchTemplateIamInstanceProfileArgs(
        name=aws.iam.InstanceProfile("ecs-instance-profile",
            role=aws.iam.Role("ecs-instance-role",
                assume_role_policy=pulumi.Output.json_dumps({
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": "ec2.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }]
                })
            ).name
        ).name
    ),
    user_data=pulumi.Output.all(cluster.name).apply(
        lambda args: pulumi.Output.secret(f"""#!/bin/bash
        echo ECS_CLUSTER={args[0]} >> /etc/ecs/ecs.config
        """
        )
    )
)

# 8. Auto Scaling Group (now properly included)
asg = aws.autoscaling.Group("ecs-asg",
    min_size=1,
    max_size=3,
    vpc_zone_identifiers=subnets.ids,
    launch_template=aws.autoscaling.GroupLaunchTemplateArgs(
        id=launch_template.id,
        version="$Latest"
    ))


# 9. Capacity Provider
capacity_provider = aws.ecs.CapacityProvider("ecs-capacity-provider",
    auto_scaling_group_provider=aws.ecs.CapacityProviderAutoScalingGroupProviderArgs(
        auto_scaling_group_arn=asg.arn,
        managed_termination_protection="ENABLED",
        managed_scaling={
            "maximum_scaling_step_size": 1000,
            "minimum_scaling_step_size": 1,
            "status": "ENABLED",
            "target_capacity": 10,
        },
    )
)

# 10. Associate Capacity Provider with Cluster
aws.ecs.ClusterCapacityProviders("cluster-capacity-providers",
    cluster_name=cluster.name,
    capacity_providers=[capacity_provider.name],
    default_capacity_provider_strategies=[aws.ecs.ClusterCapacityProvidersDefaultCapacityProviderStrategyArgs(
        base=1,
        weight=100,
        capacity_provider=capacity_provider.name
    )])

# 11. Task Definition
task_definition = aws.ecs.TaskDefinition("fastapi-task",
    family="fastapi",
    network_mode="awsvpc",
    requires_compatibilities=["EC2"],
    cpu="256",
    memory="512",
    execution_role_arn=ecs_task_execution_role.arn,
    container_definitions=pulumi.Output.all(ecr_repo.repository_url).apply(
        lambda repo_url: pulumi.Output.json_dumps([{
            "name": "fastapi",
            "image": repo_url +":latest",
            "essential": True,
            "portMappings": [{
                "containerPort": 80,
                "hostPort": 80,
                "protocol": "tcp"
            }]
        }])
    ))

# 12. ECS Service
service = aws.ecs.Service("fastapi-service",
    cluster=cluster.arn,
    task_definition=task_definition.arn,
    desired_count=1,
    launch_type="EC2",
    capacity_provider_strategies=[aws.ecs.ServiceCapacityProviderStrategyArgs(
        capacity_provider=capacity_provider.name,
        weight=100
    )])

# Export outputs
pulumi.export("ecr_repo_url", ecr_repo.repository_url)
pulumi.export("cluster_name", cluster.name)
pulumi.export("service_name", service.name)
