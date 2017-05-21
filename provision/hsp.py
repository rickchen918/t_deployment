# The script is template to create host switch profile, the profile is mainly for uplink configuration 
import requests,json,base64,paramiko
requests.packages.urllib3.disable_warnings()

mgr="192.168.64.186"
mgruser="admin"
mgrpasswd="Nicira123$"
api_ep="/api/v1/host-switch-profiles"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
url="https://"+str(mgr)+str(api_ep)

# create host switch profile
def hsp(name,standby,active,vlan):
    body="""{
  "resource_type": "UplinkHostSwitchProfile",
  "display_name": "%s",
  "mtu": 1600,
  "teaming": {
      "standby_list": [{
            "uplink_name": "%s",
            "uplink_type": "PNIC"
        }
      ],
      "active_list": [
        {
            "uplink_name": "%s",
            "uplink_type": "PNIC"
        }
      ],
      "policy": "FAILOVER_ORDER"
    },
    "transport_vlan": %s
  }"""%(name,standby,active,vlan)

    conn=requests.post(url,verify=False,headers=header,data=body)
    resp=conn.text

#hsp("rkc_profile","uplink-2","uplink-1","0")


# list  host switch profile  
def ls_hsp():
    conn=requests.get(url,verify=False,headers=header)
    resp=conn.text
#    print resp
    return resp

#print ls_hsp()


