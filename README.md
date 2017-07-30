# Python SDK for Aliyun SMS Services

## Installation
The `alisms` package is available on `pypi`, so use  

    pip install alisms

to install it.  

## AliyunSMS Object
AliyunSMS Object has the following attributes and methods  
  
### class aliyun\_sms.AliyunSMS(config\_file='', access\_key\_id='', access\_key\_secret='', region\_id='', host='ht<span>tp://</span>dysmsapi.aliyuncs.com')  
    Class  

    * config\_file: Configure file name  
    * access\_key\_id: accessKeyId of Aliyun *sub-account* (Sub account is recommended for security)  
    * access\_key\_secret: accessKeySecret of the id (vital)   
    * region\_id: Region name of your SMS service  
    * host: API host, default is enough
    % A new instance of AliyunSMS class.  

## AliyunSMS Methods  
### AliyunSMS.generate\_signature(params=None, method='GET', url='/')
    This function can generate signature based on the `params`, `method` and `url`. Of course access\_key\_secret is necessary!  

    * params: A `dict` parameters for the request, `OrderedDict` is better since the sequence is of importance.  
    * method: HTTP method for the request, default 'GET'.  
    * url: Url endpoint of the request, default is '/' if using `send\_sms()` 
    % The signature string  

### AliyunSMS.send\_sms(phone\_numbers, sign\_name, template\_code, template\_params=None, raw=True, \*\*kwargs)
    This function is used to send SMS via Aliyun API.  

    * phone\_numbers: The list of phone numbers, can be a string if only one number  
    * sign\_name: Sign name configured in Aliyun console  
    * template\_code: The template code defined in Aliyun console  
    * template\_params: The params that need to be used in template  
    * raw: If to return the original `requests` instance  
    % Status: success or failure  

## AliyunSMS Attributes  
### AliyunSMS.sms\_params
    This is the `dict` of parameters for SMS request. It can be get and set directly (A `dict` is mandatory)  

## Useful functions

### utils.hmac64(object\_str, secret, alg='sha1')  
    Compute the *HMAC-\{alg\}* of the `object\_str` with `secret` and get the return after `base64` encoding  

    * object\_str: Original string that needs to be encrypted  
    * secret: secret string  
    * alg: HMAC algorithm, default 'sha1'  
    % The encrypted string  

### utils.parse\_config(config\_file, part='\_all')  
    Parse config file, a *YAML* file is mandatory  

    * config\_file: Configure file name  
    * part: Return part of the configures, default is *\_all*  
    % The configures in `dict`
