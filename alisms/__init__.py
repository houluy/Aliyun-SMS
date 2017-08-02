from collections import OrderedDict
import uuid
import time
from urllib.parse import quote, urlencode
import requests
import json

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
        self._form_sys_params()

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
    
    def _form_sys_params(self):
        self._sms_params = dict(
            SignatureMethod='HMAC-SHA1',
            SignatureNonce=str(uuid.uuid4()),
            AccessKeyId=self._config.get('access_key_id'),
            Timestamp=self._gen_utc_time(),
            SignatureVersion='1.0',
            Format='JSON'
        )

    def _form_bus_params(self, business, **kwargs):
        self._sms_params.update(dict(
            Action=business,
            Version='2017-05-25',
            RegionId=self._config.get('region_id'),
        ))
        self._sms_params.update(kwargs)
        if not kwargs.get('BizId', None) and business == 'QuerySendDetails':#Optional Params
            self._sms_params.pop('BizId')
                
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

    def _send_req(self, url, method='GET'):
        self._sms_params = self._sort_params(self._sms_params) 
        signature = self.generate_signature()
        self._sms_params['Signature'] = signature
        self._sms_params.move_to_end('Signature', last=False) #Move this param to the top
        if (url == '/'):
            url = ''
        final_url = self._config.get('host') + '?' + '&'.join(['{}={}'.format(key, quote(val, safe='')) for key, val in self._sms_params.items()])
        return requests.get(url=final_url)
        
    def send_sms(self, phone_numbers, sign_name, template_code, template_params=None, raw=True, **kwargs):
        '''
        Send SMS message via Aliyun API
        @phone_numbers: The list of phone numbers, can be a string if only one number
        @sign_name: Sign name configured in Aliyun console
        @template_code: The template code defined in Aliyun console
        @template_params: The params that need to be used in template
        %Status: success or failure
        '''
        url = '/'
        method = 'GET'
        template_params = json.dumps(template_params, separators=(',', ':')) #Must not have whitespace
        self._form_bus_params(business='SendSms', PhoneNumbers=phone_numbers, SignName=sign_name, TemplateCode=template_code, TemplateParam=template_params, **kwargs)
        if raw:
            return self._send_req(url=url)
        
    def query_details(self, phone_number, serial_number='', send_date='', page_size='10', current_page='1', raw=True, **kwargs):
        '''
        Query the details of SMS service
        @phone_number: One phone number
        @serial_number(optional): Serial number from send_sms API
        @send_date: Query date, less than 30 days
        @page_size: Paging, less than 50 items
        @current_page: Current page, from 1
        %Details
        '''
        url='/'
        method='GET'
        self._form_bus_params(business='QuerySendDetails', PhoneNumber=phone_number, BizId=serial_number, SendDate=send_date, PageSize=page_size, CurrentPage=current_page)
        if raw:
            return self._send_req(url=url)
        else:
            res = self._send_req(url=url)
            return res.json()
