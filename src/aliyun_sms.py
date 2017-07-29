from collections import OrderedDict
import uuid
import time
from urllib.parse import quote, urlencode
import requests

from .utils import hmacb64, parse_config

class AliyunSMS():
    def __init__(self, config_file=None, access_key_id='', access_key_secret='', region_id='', host='http://dysmsapi.aliyuncs.com'):
        self._sms_params = OrderedDict()
        if config_file:
            self._config = parse_config(config_file)
        else:
            self._config = {
                'access_key_id': access_key_id,
                'access_key_secret': access_key_secret,
                'region_id': region_id,
                'host': host,
            }

    @property
    def sms_params(self):
        return self._sms_params

    @sms_params.setter
    def sms_params(self, value):
        if not isinstance(value, dict):
            raise TypeError("An dict instance is required")

        self._sms_params.update(value)

    def _gen_utc_time(self):
        return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time()))

    def _form_params(self, phone_numbers, sign_name, template_code, template_params=None, **kwargs):
        self._sms_params = dict(
            SignatureMethod='HMAC-SHA1',
            SignatureNonce=str(uuid.uuid4()),
            AccessKeyId=self._config.get('access_key_id'),
            Timestamp=self._gen_utc_time(),
            SignatureVersion='1.0',
            Format='JSON',
            OutId='123',
            Action='SendSms',
            Version='2017-05-25',
            RegionId=self._config.get('region_id'),
            PhoneNumbers=phone_numbers,
            SignName=sign_name,
            TemplateParam=template_params,
            TemplateCode=template_code,
        )

    def generate_signature(self, params=None, method='GET', url='/'):
        '''
        Generate Signature for requests
        @params: Parameters dict, self._sms_params for default
        @method: HTTP Method, GET default
        @url: url endpoint, / default
        %signature
        '''
        params = params if params else self._sms_params
        secret = self._config.get('access_key_secret') + '&' #Must add & to the end
        querystring = quote(urlencode(params))
        return hmacb64('&'.join([method, quote(url, safe=''), querystring]), secret)

    def _sort_params(self, dic):
        return OrderedDict(sorted(dic.items(), key=lambda x: x[0]))
        
    def send_sms(self, phone_numbers, sign_name, template_code, template_params=None, raw=True, **kwargs):
        url = '/'
        method = 'GET'
        '''
        Send SMS message via Aliyun API
        @phone_numbers: The list of phone numbers, can be a string if only one number
        @sign_name: Sign name configured in Aliyun console
        @template_code: The template code defined in Aliyun console
        @template_params: The params that need to be used in template
        %Status: success or failure
        '''
        self._form_params(phone_numbers, sign_name, template_code, template_params, **kwargs)
        self._sms_params = self._sort_params(self._sms_params) 
        signature = self.generate_signature()
        self._sms_params['Signature'] = signature
        self._sms_params.move_to_end('Signature', last=False) #Move this param to the top
        final_url = self._config.get('host') + '?' + '&'.join(['{}={}'.format(key, quote(val, safe='')) for key, val in self._sms_params.items()])
        if raw:
            return requests.get(url=final_url)

if __name__ == '__main__':
    a = AliyunSMS(access_key_id='testId', access_key_secret='testSecret', region_id='cn-hangzhou')
