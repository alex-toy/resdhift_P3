import pandas as pd
import boto3
import json
import os
import configparser
from botocore.exceptions import ClientError
import psycopg2


config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))
KEY                    = config.get('AWS','KEY')
SECRET                 = config.get('AWS','SECRET')

reg_n="us-west-2"

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
DWH_PORT               = config.get("DWH","DWH_PORT")
DWH_DB                 = config.get("DWH","DWH_DB")


ec2 = boto3.resource(
    'ec2',
    region_name=reg_n,
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET
)

s3 = boto3.resource(
    's3',
    region_name=reg_n,
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET
)

iam = boto3.client(
    'iam',
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
    region_name=reg_n
)

redshift = boto3.client(
    'redshift',
    region_name=reg_n,
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET
)

    
def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])


myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
df = prettyRedshiftProps(myClusterProps)


DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
DWH_ROLE_ARN = myClusterProps['IamRoles'][0]['IamRoleArn']
DWH_ENDPOINT = DWH_ENDPOINT.replace("/", "\/")
DWH_ROLE_ARN = DWH_ROLE_ARN.replace("/", "\/")

command = f"sed -i 's/DWH_ENDPOINT=/DWH_ENDPOINT={DWH_ENDPOINT}/'  dwh.cfg"
os.system(command)

command = f"sed -i 's/DWH_ROLE_ARN=/DWH_ROLE_ARN={DWH_ROLE_ARN}/'  dwh.cfg"
os.system(command)


try:
    vpc = ec2.Vpc(id=myClusterProps['VpcId'])
    defaultSg = list(vpc.security_groups.all())[0]
    print(defaultSg)
    defaultSg.authorize_ingress(
        GroupName='default',
        CidrIp='0.0.0.0/0',
        IpProtocol='TCP',
        FromPort=int(DWH_PORT),
        ToPort=int(DWH_PORT)
    )
except Exception as e:
    print(e)

    