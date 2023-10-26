from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import CfnOutput

class VpcPeeringStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Prod_configs = self.node.try_get_context("envs")["Prod"]

        #  Create a custome VPC
        custom_vpc = ec2.Vpc(
            self, "customvpc",
            ip_addresses= ec2.IpAddresses.cidr(Prod_configs['vpc_config']['vpc_cidr']),
            max_azs= 2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet", cidr_mask=Prod_configs["vpc_config"]["cidr_mask"], subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet", cidr_mask=Prod_configs["vpc_config"]["cidr_mask"], subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                ),
            ])

        # Import Default VPC to my stack
        default_vpc = ec2.Vpc.from_lookup(self,
                                   "defaultvpc",
                                   is_default=True)
        
        # Establish Vpc Peering between Custom VPC and Default VPC
        peer_connection = ec2.CfnVPCPeeringConnection(self,
                                               "mypeerconnection",                     
                                               peer_vpc_id=custom_vpc.vpc_id,
                                               vpc_id=default_vpc.vpc_id)
        
        # Modify Route table of the custom VPC private table to add the peering route
        custome_privare_RT = ec2.CfnRoute(self, "PrivateRT",
                                        destination_cidr_block= default_vpc.vpc_cidr_block,
                                        route_table_id= custom_vpc.isolated_subnets[0].route_table.route_table_id,
                                        vpc_peering_connection_id=peer_connection.attr_id
                                        )
        
        # Modify Route table of the default VPC Public table to add the peering route
        defaultroutetable = ec2.CfnRoute(self, "PublicRT",
                                        destination_cidr_block=custom_vpc.vpc_cidr_block,
                                        route_table_id= default_vpc.public_subnets[0].route_table.route_table_id,
                                        vpc_peering_connection_id=peer_connection.attr_id
                                        )
        
         # get AMI ID
        ami = ec2.MachineImage.latest_amazon_linux2(
            edition= ec2.AmazonLinuxEdition.STANDARD,
            storage= ec2.AmazonLinuxStorage.EBS,
            virtualization= ec2.AmazonLinuxVirt.HVM,
            cpu_type=ec2.AmazonLinuxCpuType.X86_64
        )
        # Instance in the private subnet of the custom VPC
        private_Instance = ec2.Instance(self, "Instance_PVT_subnet",
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="PrivateInstance", 
            machine_image=ami,
            vpc=custom_vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )     
        )

        # Open and read the user data file
        with open("bootstrap_script/install_httpd.sh", "r") as file:
            user_data = file.read()

        # Instance in the Public subnet of the Default VPC
        public_Instance = ec2.Instance(self,"Public_Webserver",
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="PublicInstance",
            machine_image=ami,
            vpc= default_vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            key_name="keypair",
            user_data= ec2.UserData.custom(user_data)
        )

        # Allow ICMP on the private instance for ping
        private_Instance.connections.allow_from_any_ipv4(
            ec2.Port.all_icmp(),
            description="ICMP for ping"
        )
        # Open port 22 for ssh on the public instance
        public_Instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(22),
            description="Allow shh traffic on port 22"
        )
        # Open port 80 for the public instance to test if the user data worked.
        public_Instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),
            description="Allow HTTP traffic on port 80"
        )

        # Get the private IPV 4 of the private instance
        CfnOutput(self,
                  "myprivateIp",
                  value=private_Instance.instance_private_ip,
                  export_name="privateIpv4")
        
        # Get the public IPV 4 of the public instance
        CfnOutput(self,
                  "public",
                  value=public_Instance.instance_public_ip,
                  export_name="PublicIpv4")