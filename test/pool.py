# The script to create TEP IP Pool 
import requests,json,base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mgr="192.168.64.186"
user="admin"
passwd="Nicira123$"
cred=base64.b64encode('%s:%s'%(user,passwd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}

def ippool_create(name,dns,ipstart,ipend,gw,cidr):
    api_ep="/api/v1/pools/ip-pools"
    url="https://"+mgr+api_ep
    body="""
{"display_name":"%s", \
"subnets":[ \
{ \
"dns_nameservers":["%s"], \
"allocation_ranges":[ \
{ \
"start":"%s", \
"end":"%s" \
} \
], \
"gateway_ip":"%s", \
"cidr":"%s" }]}""" %(name,dns,ipstart,ipend,gw,cidr)


    print body
    conn=requests.post(url,verify=False,headers=header,data=body)
    print conn.status_code
    print conn.text

ippool_create("tep","192.168.0.96","192.168.65.200","192.168.65.254","192.168.65.1","192.168.65.0/24")
