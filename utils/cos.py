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

    cors_config = {  # 跨域配置
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config
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


def delete_file_list(bucket, region, file_obj, key_list):
    secret_id = local_settings.Tencent_cos_id
    secret_key = local_settings.Tencent_cos_key
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    objects = {  # 源码里面要求这样传文件
        "Quiet": "true",
        "Object": key_list,
    }
    client.delete_objects(

        Bucket=bucket,
        Delete=objects
    )


def credential(bucket, region):
    """ 获取cos上传临时凭证 """

    from sts.sts import Sts

    config = {
        # 临时密钥有效时长，单位是秒（30分钟=1800秒）
        'duration_seconds': 1800,
        # 固定密钥 id
        'secret_id': local_settings.Tencent_cos_id,
        # 固定密钥 key
        'secret_key': local_settings.Tencent_cos_key,
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': region,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # "name/cos:PutObject",
            # 'name/cos:PostObject',
            # 'name/cos:DeleteObject',
            # "name/cos:UploadPart",
            # "name/cos:UploadPartCopy",
            # "name/cos:CompleteMultipartUpload",
            # "name/cos:AbortMultipartUpload",
            "*",
        ],

    }

    sts = Sts(config)
    result_dict = sts.get_credential()
    return result_dict
