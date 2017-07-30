# Python SDK for Aliyun SMS Services

## AliyunSMS Object
  
class AliyunSMS  
### AliyunSMS.send\_sms(phone\_numbers, sign\_name, template\_code, template\_params=None, raw=True, \*\*kwargs)
This function is used to send SMS via Aliyun API. 
    @phone\_numbers: The list of phone numbers, can be a string if only one number
    @sign\_name: Sign name configured in Aliyun console
    @template\_code: The template code defined in Aliyun console
    @template\_params: The params that need to be used in template
    %Status: success or failure

