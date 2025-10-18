from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging
from django.conf import settings
from S_plant import local_settings


def create_bucket(bucket, region='ap-guangzhou'):
    secret_id = local_settings.Tencent_cos_id
    secret_key = local_settings.Tencent_cos_key
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)
    response = client.create_bucket(
        Bucket=bucket,
        ACL='public-read',
    )


def upload_file(bucket, region, file_obj, key):
    secret_id = local_settings.Tencent_cos_id
    secret_key = local_settings.Tencent_cos_key
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_obj,  # 被存储的文件对象
        Key=key  # 上传给桶的文件名
    )

    # 还需要接收上传到桶里面的文件路径
    # https://sakura-1381991211.cos.ap-guangzhou.myqcloud.com/text.png
    return 'https://{}.cos.{}.myqcloud.com/{}'.format(bucket, region, key)


def delete_file(bucket, region, file_obj, key):
    secret_id = local_settings.Tencent_cos_id
    secret_key = local_settings.Tencent_cos_key
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    response = client.delete_objects(
        Bucket=bucket,
        Key=key  # 上传给桶的文件名
    )

