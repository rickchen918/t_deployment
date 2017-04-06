import requests,json,base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mgr="192.168.64.186"
user="admin"
passwd="Nicira123$"
cred=base64.b64encode('%s:%s'%(user,passwd))
header={"Authorization":"Basic %s"%cred}
#print header

api_ep="/api/v1/cluster/backups/config"
url="https://"+mgr+api_ep

conn=requests.get(url,verify=False,headers=header)
print conn.status_code
print conn.text
