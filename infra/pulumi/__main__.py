import os
import pulumi
import pulumi_aws as aws

LOCAL_IP = os.environ.get('LOCAL_IP', '0.0.0.0')
# Create a security group with inbound rules
security_group = aws.ec2.SecurityGroup("FastAPITutorialSecurityGroup",
    description="launch-wizard-1 created 2025-03-27T03:05:29.635Z",
    name="fastapi-yt-sg-1",
    vpc_id="vpc-08fa77c93020e0090",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow SSH access from specific IP",
            from_port=22,
            to_port=22,
            protocol="tcp",
            cidr_blocks=[f"{LOCAL_IP}/32"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow HTTPS access from anywhere",
            from_port=443,
            to_port=443,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow HTTP access from anywhere",
            from_port=80,
            to_port=80,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
    )]
)

# Create the EC2 instance
instance = aws.ec2.Instance("FastAPIInstance",
    instance_type="t2.micro",
    ami="ami-04f167a56786e4b09",
    vpc_security_group_ids=[security_group.id],
    key_name="fastapi-tutorial-kp",
    root_block_device=aws.ec2.InstanceRootBlockDeviceArgs(
        volume_type="gp3",
        volume_size=8,
        iops=3000,
        throughput=125,
        delete_on_termination=True,
        encrypted=False,
    ),
    credit_specification=aws.ec2.InstanceCreditSpecificationArgs(
        cpu_credits="standard"
    ),
    metadata_options=aws.ec2.InstanceMetadataOptionsArgs(
        http_endpoint="enabled",
        http_put_response_hop_limit=2,
        http_tokens="required"
    ),
    private_dns_name_options=aws.ec2.InstancePrivateDnsNameOptionsArgs(
        hostname_type="ip-name",
        enable_resource_name_dns_aaaa_record=False,
        enable_resource_name_dns_a_record=True
    ),
    tags={
        "Name": "fastapi-yt",
    }
)

# Export the instance public IP
pulumi.export("InstancePublicIP", instance.public_ip)
