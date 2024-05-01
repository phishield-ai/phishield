import json

from loguru import logger
from minio import Minio


def minio_setup_bucket(endpoint_url, user, password, bucket, secure=True):
    client = Minio(endpoint_url, access_key=user, secret_key=password, secure=secure)

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
                "Resource": f"arn:aws:s3:::{bucket}",
            },
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket}/*",
            },
        ],
    }
    client.set_bucket_policy(bucket, json.dumps(policy))


def minio_health_check(endpoint_url, user, password, secure=True):
    client = Minio(endpoint_url, access_key=user, secret_key=password, secure=secure)
    try:
        client.list_buckets()
        logger.info("MinIO Health Check: Service is up.")
        return True
    except Exception as e:
        logger.warning(f"MinIO Health Check: Service is down. Error: {e}")
        return False
