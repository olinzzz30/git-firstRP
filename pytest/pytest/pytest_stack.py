from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_eks as eks,
)


class PytestStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, 'Vpc', is_default=True)
        #vpc = ec2.Vpc.from_lookup(self, 'Vpc', vpc_id='vpc-f76c208f')
        #vpc = ec2.Vpc(self, 'Vpc', max_azs=3, nat_gateways=1)

        cluster = eks.Cluster(self, 'Cluster',
            # vpc=vpc,
            version=eks.KubernetesVersion.V1_21,
            default_capacity=0)

        # cluster = eks.Cluster(self, 'Cluster',
        # version='1.15',
        # default_capacity=0
        # )

        # cluster.add_capacity('SpotCapacity',
        cluster.add_auto_scaling_group_capacity('SpotCapacity',
            instance_type=ec2.InstanceType('t3.large'),
            spot_price='0.035',
            min_capacity=4
        )

        core.CfnOutput(self, 'Region', value=self.region)
        core.CfnOutput(self, 'VpcId', value=vpc.vpc_id)

        # The code that defines your stack goes here
