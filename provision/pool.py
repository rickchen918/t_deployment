# The script is template to create ip pool
import requests,json,base64,paramiko
requests.packages.urllib3.disable_warnings()

mgr="192.168.64.186"
mgruser="admin"
mgrpasswd="Nicira123$"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
api_ep="/api/v1/pools/ip-pools"
url="https://"+str(mgr)+str(api_ep)

# create ip pools 
def pool(name,des,dns,start,end,gw,cidr):
    body="""{
  "display_name": "%s",
  "description": "%s",
  "subnets": [
    {
        "dns_nameservers": ["%s"],
        "allocation_ranges": [
            {
                "start": "%s",
                "end": "%s"
            }
        ],
       "gateway_ip": "%s",
       "cidr": "%s"
    }
  ]
}""" %(name,des,dns,start,end,gw,cidr)

    conn=requests.post(url,verify=False,headers=header,data=body)
    resp=conn.text
#    print resp

#pool('vtep','vtep pool','192.168.0.96','192.168.65.200','192.168.65.223','192.168.65.1','192.168.65.0/24')

# list ip pools on existing nsx manager 
def ls_pool():
    conn=requests.get(url,verify=False,headers=header)
    resp=conn.text
#    print resp
    return resp


#ls_pool()

