
# The script is to list registered host node
import requests,json,base64,paramiko
requests.packages.urllib3.disable_warnings()

mgr="192.168.64.186"
mgruser="admin"
mgrpasswd="Nicira123$"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
api_ep="/api/v1/fabric/nodes"
url="https://"+str(mgr)+str(api_ep)

# list host node on existing nsx manager 
def ls_host():
    conn=requests.get(url,verify=False,headers=header)
    resp=conn.text
    return resp

