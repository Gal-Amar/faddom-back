from datetime import datetime, timedelta
import boto3
from .config import get_settings
from datetime import datetime, timedelta, timezone


def get_instance_id_from_ip_address(ip):
    settings = get_settings()
    ec2_client = boto3.client('ec2', aws_access_key_id=settings.aws_access_id,
                              aws_secret_access_key=settings.aws_secret_key)
    ec2_instances = ec2_client.describe_instances(Filters=[{
        'Name': 'private-ip-address',
        'Values': [
            ip,
        ]
    }
    ])
    return ec2_instances['Reservations'][0]['Instances'][0]['InstanceId']


def get_cpu_utilization_data(ip, delta, period):
    settings = get_settings()
    cloudwatch = boto3.client(
        'cloudwatch', aws_access_key_id=settings.aws_access_id, aws_secret_access_key=settings.aws_secret_key, region_name=settings.aws_region)

    start_date = datetime.now() - timedelta(seconds=delta) - timedelta(minutes=5)
    start = start_date.replace(tzinfo=timezone.utc)
    end_time = (datetime.now() - timedelta(minutes=5)
                ).replace(tzinfo=timezone.utc).isoformat()
    iso_format = start.isoformat()

    instance_id = get_instance_id_from_ip_address(ip)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            }
        ],
        MetricName='CPUUtilization',
        StartTime=iso_format,
        EndTime=end_time,
        Period=period,
        Statistics=[
            'Maximum'
        ],
    )
    for datapoint in response['Datapoints']:
        datapoint['Timestamp'] = datapoint['Timestamp'].isoformat()

    response['Datapoints'] = sorted(
        response['Datapoints'],
        key=lambda x: datetime.fromisoformat(x['Timestamp'])
    )

    return response


def get_cpu_utilization_data(ip, delta, period):
    settings = get_settings()
    cloudwatch = boto3.client(
        'cloudwatch',
        aws_access_key_id=settings.aws_access_id,
        aws_secret_access_key=settings.aws_secret_key,
        region_name=settings.aws_region
    )

    start_time = (datetime.now() - timedelta(seconds=delta) -
                  timedelta(minutes=5)).replace(tzinfo=timezone.utc)
    end_time = (datetime.now() - timedelta(minutes=5)
                ).replace(tzinfo=timezone.utc).isoformat()

    instance_id = get_instance_id_from_ip_address(ip)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        MetricName='CPUUtilization',
        StartTime=start_time.isoformat(),
        EndTime=end_time,
        Period=period,
        Statistics=['Maximum'],
    )

    for datapoint in response['Datapoints']:
        datapoint['Timestamp'] = datapoint['Timestamp'].isoformat()

    response['Datapoints'].sort(key=lambda x: x['Timestamp'])

    return response
