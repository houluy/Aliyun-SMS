# Python SDK for Aliyun SMS Services

[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg?style=plastic)]()
[![CocoaPods](https://img.shields.io/cocoapods/l/AFNetworking.svg?style=plastic)]()
[![PyPI](https://img.shields.io/pypi/status/Django.svg?style=plastic)]()
[![](https://img.shields.io/badge/version-1.1.0-ff69b4.svg?style=plastic)]()
[![](https://github.com/houluy/logo/blob/master/Logo.png)]()

## Installation
The `alisms` package is available on `pypi`, so use  

    pip install alisms

to install it.  

## Document
Please refer to [document](http://aliyun-sms-api.readthedocs.io) to read the full docs.  


## Tutorial
Here is a quick example of sending SMS messages for a phone user:  

    import alisms

    client = alisms.AliyunSMS(access_key_id='testId', access_key_secret='testSecret', region_id='cn-hangzhou')
    template_params = {
        'code': '123456',
    }
    client.send_sms(phone_numbers='13000000000', sign_name='阿里云', template_code='SMS_10000000', template_params=template_params)
