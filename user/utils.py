# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import json

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models

ACCESS_KEY_ID = 'LTAI5tDFRf4NqJax1c2R78Ub'
ACCESS_KEY_SECRET = 'X8IT5TeylfhZV7CgOU5iasux5mYuBf'


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send(phone, code):
        client = Sample.create_client(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name='晨曦记录',
            template_code='SMS_225981393',
            template_param="{'code': %d}" % code
        )
        # 复制代码运行请自行打印 API 的返回值
        response = str(client.send_sms(send_sms_request))
        response = response.replace('\'', '"')
        body = json.loads(response).get('body')
        return body

    # @staticmethod
    # async def main_async(
    #         args: List[str],
    # ) -> None:
    #     client = Sample.create_client('accessKeyId', 'accessKeySecret')
    #     send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
    #         phone_numbers='18530834620',
    #         sign_name='晨曦记录',
    #         template_code='SMS_224357117',
    #         template_param="{'code': 975285}"
    #     )
    #     # 复制代码运行请自行打印 API 的返回值
    #     await client.send_sms_async(send_sms_request)


if __name__ == '__main__':
    print(Sample.send('18530834620', 458231))
