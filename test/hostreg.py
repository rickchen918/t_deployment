# the script templetae to register host to nsx manager, the thumprint is required to avoid ssl challenge
import requests,json,base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mgr="192.168.64.186"
user="admin"
passwd="Nicira123$"
cred=base64.b64encode('%s:%s'%(user,passwd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
url_ep="https://192.168.64.186/api/v1/fabric/nodes"

body="""{
  "resource_type": "HostNode",
  "display_name": "t-esx1",
  "ip_addresses": [
    "192.168.64.150"
  ],
  "os_type": "ESXI",
  "os_version": "6.5.0",
  "host_credential": {
    "username": "root",
    "password": "nicira123",
    "thumbprint":"A0:7E:39:B7:EB:75:B7:34:6B:FC:BB:DD:E5:3B:47:09:BB:D0:A1:43:22:3B:CE:1F:20:99:0C:98:1F:77:4D:21"
  }
}"""

conn=requests.post(url_ep,verify=False,headers=header,data=body)
resp=conn.text
print resp
