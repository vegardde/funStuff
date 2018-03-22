import time
import base64
from M2Crypto import RSA
import httplib, urllib
import json
import os

os.chdir(r"C:\dev\GIT\funStuff")

def print_json(j,prefix=''):
    for key, value in j.items():
        if isinstance (value,dict):
            print '%s%s' % (prefix,key)
            print_json(value, prefix+'  ')
        else:
            print '%s%s:%s' % (prefix,key,value)

username = 'vegardde'
password = 'xKy7sn.2'
service  = 'NEXTAPI'
URL='api.test.nordnet.se'
API_VERSION='2'

timestamp = int(round(time.time()*1000))
timestamp = str(timestamp)
buf = base64.b64encode(username)+':'+base64.b64encode(password)+':'+base64.b64encode(timestamp)
rsa=RSA.load_pub_key('NEXTAPI_TEST_public.pem')
encrypted_hash = rsa.public_encrypt(buf, RSA.pkcs1_padding)
hash = base64.b64encode(encrypted_hash)

headers = {"Accept": "application/json"}
conn = httplib.HTTPSConnection(URL)

# GET server status
conn.request('GET','/next/'+API_VERSION + '/', '', headers)
r=conn.getresponse()
response=r.read()
j = json.loads(response)
print_json(j)

# POST login
params = urllib.urlencode({'service': 'NEXTAPI', 'auth': hash})
conn.request('POST','/next/'+API_VERSION+'/login',params,headers)
r=conn.getresponse()
response=r.read()
j = json.loads(response)
print_json(j)


params = urllib.urlencode({'service': 'NEXTAPI', 'auth': hash})