# the script is to scan exisitng host nodes and register to transport node. 
# there are 7 variables requirement to complete this api call
# hname calls from tn.ls_host (tn.py) to fill "description" and "displayname" 
# uuid calls from tn.ls_host(tn.py) to fill "host node uuid"
# hsn(host switch name) is hard-code for hostnode, because hostnode is only to accept overlay transport zone 
# pool_id calls from pool (pool.py) for tep ip range assignment 
# hspid calls from hsp (hsp.py) for host switch profile. The key must be  "UplinkHostSwitchProfile" or system definition, 
# not the display name what we create. but uuid has to be linked from the profile which we created 
# tz_ol calles from tz (tz.py) for transport zone endpoint id. host node only can accept overlay  

import json,base64,requests
import tz,tn,pool,hsp
mgr="192.168.64.186"
mgruser="admin"
mgrpasswd="Nicira123$"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}
api_ep="/api/v1/transport-nodes"
url="https://"+str(mgr)+str(api_ep)

# retreive transport zone uuid 
zone=tz.ls_tz()
jsz=json.loads(zone)
resultsj=jsz.get('results')
tz_box={}
for zx in resultsj:
    dname=zx.get('display_name')
    id=zx.get('id')
    d={dname:id}
    tz_box.update(d)
tz_ol=tz_box.get('tz_OL')
tz_vl=tz_box.get('tz_VL')

# retreive ip poool for tep
pool=pool.ls_pool()
jsp=json.loads(pool)
resultsp=jsp.get('results')
pool_box={}
for px in resultsp:
    dname=px.get('display_name')
    id=px.get('id')
    d={dname:id}
    pool_box.update(d)
pool_id=pool_box.get('vtep')

#get host swich profile information 
hsp=hsp.ls_hsp()
jshsp=json.loads(hsp)
resultshsp=jshsp.get('results')
hsp_box={}
for hspx in resultshsp:
    pf=hspx.get('display_name')
# if the host switch profile == rkc_profile, we use the uuid as the value, but key is still "UplinkHostSwitchProfile"
# the rkc_profile is the example what i created for host applying 
    if pf=="rkc_profile":
        hspname=hspx.get('display_name')
        hspid=hspx.get('id')

#Get node type is on host 
host=tn.ls_host()
jsh=json.loads(host)
resultsh=jsh.get('results')
host_box={}
for hx in resultsh:
    rt=hx.get('resource_type')
    if rt=='HostNode':
        dname=hx.get('display_name')
        id=hx.get('id')
        d={dname:id}
        host_box.update(d)
    else:
	pass

# Here is only to configure host node, so hsn is hardcode to overlay
# The key under host_switch_profile_ids is hardcode for type requirement
def tn_reg():
    hsn="overlay"
    for key in host_box:
        hname=key
        uuid=host_box.get(hname)
	body="""{
  "description":"%s",
  "display_name":"%s",
  "node_id":"%s",
  "host_switches": [
    {
      "host_switch_name": "%s",
      "static_ip_pool_id": "%s",
      "host_switch_profile_ids": [
        {
          "key":"UplinkHostSwitchProfile",
          "value":"%s"
        }
      ],
      "pnics": [
        {
          "uplink_name":"uplink-1",
          "device_name":"vmnic1"
        }
      ]
    }
  ],
  "transport_zone_endpoints":[
    {
      "transport_zone_id":"%s"
    }
  ]
}"""%(hname,hname,uuid,hsn,pool_id,hspid,tz_ol)
        conn=requests.post(url,verify=False,headers=header,data=body)
	code=conn.status_code
	resp=conn.text
#	print code,resp
#	print body

tn_reg()
