# The script is template to get host thumbprint and call api to regitser host node to nsx manager 
# if we have volume hosts which needs to register, we could add additional loop to fulfill requirement 
import requests,json,base64,paramiko
requests.packages.urllib3.disable_warnings()

mgr="192.168.64.186"
mgruser="admin"
mgrpasswd="Nicira123$"
hostuser="root"
hostpasswd="nicira123"

# Get thumbprint from host and return to global variable 
def hosthumb(esx):
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(esx,username=hostuser,password=hostpasswd)
    stdin,stdout,stderr=ssh.exec_command("openssl x509 -in /etc/vmware/ssl/rui.crt -fingerprint -sha256 -noout")
    esx_tp=stdout.readlines()[0]
    thumb=esx_tp.split("=")[1].strip("\n")
    print thumb
    return thumb

# register host, the thumbprint is required when call registration api
def hostreg(esx):
    cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
    header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
    api_ep="/api/v1/fabric/nodes"
    url="https://"+str(mgr)+str(api_ep)
    tp=hosthumb(esx)
    print tp
    body="""{
  "resource_type": "HostNode",
  "display_name": "%s",
  "ip_addresses": [
    "%s"
  ],
  "os_type": "ESXI",
  "os_version": "6.5.0",
  "host_credential": {
    "username": "%s",
    "password": "%s",
    "thumbprint":"%s"
  }
}"""%(esx,esx,hostuser,hostpasswd,tp)
    conn=requests.post(url,verify=False,headers=header,data=body)
    resp=conn.text
    print resp

hostreg("192.168.64.150")
