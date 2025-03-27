
# Get path of script location regardless of where script is called from
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get public IP (for AWS EC2 SSH ingress access)
export LOCAL_IP=$(curl https://ipinfo.io/ip)

# Run Pulumi up
cd $SCRIPTDIR/infra/pulumi
pulumi up
