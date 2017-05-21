# The script is template to create transport zone
import requests,json,base64,paramiko
requests.packages.urllib3.disable_warnings()

mgr="192.168.64.186"
mgruser="admin"
mgrpasswd="Nicira123$"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
api_ep="/api/v1/transport-zones"
url="https://"+str(mgr)+str(api_ep)

# create transport zone with name, hostswicth, description and type specifiction 
def tz(name,hsn,desc,type):
    body="""{
  "display_name":"%s",
  "host_switch_name":"%s",
  "description":"%s",
  "transport_type":"%s"
}"""%(name,hsn,desc,type)
    conn=requests.post(url,verify=False,headers=header,data=body)
    resp=conn.text
    print resp

# list transport zone on existing nsx manager 
def ls_tz():
    conn=requests.get(url,verify=False,headers=header)
    resp=conn.text
    return resp

#print ls_tz()

