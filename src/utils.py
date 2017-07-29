import hmac
import base64
import hashlib
import yaml

def hmacb64(obj_str, secret, alg='sha1'):
    '''
    Generate the string after base64 encoding with HMAC algorithm 
    @obj_str: Original string that needs to encrypt, must be string
    @secret: Secret Key, must be string
    @alg: HMAC algorithm, default SHA1

    %return: Encrypted data (string)
    '''
    if (alg == 'sha1'):
        alg = hashlib.sha1
    h = hmac.new(secret.encode(), obj_str.encode(), alg)
    return base64.b64encode(h.digest()).decode()

def parse_config(config_file, part='_all'):
    f = open(config_file, 'r')
    if part == '_all':
        return yaml.load(f)
    else:
        return yaml.load(f).get(part, None)

