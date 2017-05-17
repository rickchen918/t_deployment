# The script to create transport zone 
import requests,json,base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mgr="192.168.64.186"
user="admin"
passwd="Nicira123$"
cred=base64.b64encode('%s:%s'%(user,passwd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}

def tz_create(dname,sname,type):
    api_ep="/api/v1/transport-zones"
    url="https://"+mgr+api_ep
    body="""{"display_name":"%s", \
"host_switch_name":"%s", \
"transport_type":"%s" \
}"""%(dname,sname,type)
#    print body
    conn=requests.post(url,verify=False,headers=header,data=body)
    print conn.status_code
    print conn.text

tz_create("tz_OL","overlay","OVERLAY")
tz_create("tz_VL","VLAN","VLAN")
