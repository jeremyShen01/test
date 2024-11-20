import boto3
import datetime

# 配置 AWS 区域
AWS_REGION = 'us-west-2'
S3_BUCKET_NAME = 'your-bucket-name'
CLOUDWATCH_NAMESPACE = 'CustomNamespace'
CLOUDWATCH_METRIC_NAME = 'S3ObjectCount'

def list_s3_objects(bucket_name):
    """列出指定S3存储桶中的对象数量"""
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name)
    objects = response.get('Contents', [])
    object_count = len(objects)
    print(f"Found {object_count} objects in bucket '{bucket_name}'.")
    return object_count

def put_cloudwatch_metric(namespace, metric_name, value):
    """将指标发送到CloudWatch"""
    cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION)
    response = cloudwatch.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Timestamp': datetime.datetime.utcnow(),
                'Value': value,
                'Unit': 'Count'
            }
        ]
    )
    print(f"Metric {metric_name} with value {value} sent to CloudWatch.")

if __name__ == "__main__":
    # 获取S3存储桶中的对象数量
    object_count = list_s3_objects(S3_BUCKET_NAME)
    
    # 将对象数量作为指标发送到CloudWatch
    put_cloudwatch_metric(CLOUDWATCH_NAMESPACE, CLOUDWATCH_METRIC_NAME, object_count)
