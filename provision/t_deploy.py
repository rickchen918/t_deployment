import os,paramiko,json,base64,time
vc="192.168.0.65"
vc_user="administrator@rkc.local"
vc_pass="Nicira123$"
vc_dc="Home"
vc_cluster="nsx"
vc_ds="nsx_lab"
vc_net="64-0"
disk_mode="thick"
vc_domain="rkc.local"

ctr_mask="255.255.255.0"
ctr_gateway="192.168.64.1"
ctr_dns1_0="192.168.0.96"
ctr_domain_0="rkc.local"
ctr_ntp="192.168.0.58"
ctr_ssh="True"
ctr_root="True"
ctr_pass="Nicira123$"
ctr_cli_pass="Nicira123$"
nsx_user="admin"
nsx_pass="Nicira123$"
esg_nw0="64-0"
esg_nw1="65-0"
esg_nw2="VM Network"
esg_nw3="VM Network"


mgr_name='t-mgr'
mgr_ip="192.168.64.186"
ctr1_name="t-ctr1"
ctr1_ip="192.168.64.110"
ctr2_name="t-ctr2"
ctr2_ip="192.168.64.111"
ctr3_name="t-ctr3"
ctr3_ip="192.168.64.112"
edge1_name="t-edge1"
edge1_ip="192.168.64.20"
edge2_name="t-edge2"
edge2_ip="192.168.64.21"
mgr_file="../../nsx-manager-1.1.0.0.0.4788147.ova"
ctr_file="../../nsx-controller-1.1.0.0.0.4788146.ova"
esg_file="../../nsx-edge-1.1.0.0.0.4788148.ova"

###########################################################################################################
# NSX appliance deployment
###########################################################################################################
def script(app_ip,app_mask,app_name,ovfname):
    deploy_script="""ovftool --X:injectOvfEnv --X:logFile=ovftool.log --allowExtraConfig \
--acceptAllEulas --noSSLVerify --name=%s --diskMode=%s --powerOn --datastore=%s --network=%s --prop:nsx_ip_0=%s \
--prop:nsx_netmask_0=%s --prop:nsx_gateway_0=%s --prop:nsx_dns1_0=%s --prop:nsx_domain_0=%s --prop:nsx_ntp_0=%s \
--prop:nsx_isSSHEnabled=True --prop:nsx_allowSSHRootLogin=True \
--prop:nsx_passwd_0=%s --prop:nsx_cli_passwd_0=%s --prop:nsx_hostname=%s %s \
vi://"%s":"%s"@"%s"/%s/host/%s """ %(app_name,disk_mode,vc_ds,vc_net,app_ip,app_mask,ctr_gateway,ctr_dns1_0,vc_domain,ctr_ntp,ctr_pass,ctr_cli_pass,app_name,ovfname,vc_user,vc_pass,vc,vc_dc,vc_cluster)
    return deploy_script

def esg_script(app_ip,app_mask,app_name,ovfname):
    deploy_script="""ovftool --X:injectOvfEnv --X:logFile=ovftool.log --allowExtraConfig \
--acceptAllEulas --noSSLVerify --name=%s --diskMode=%s --powerOn --datastore=%s --net:"Network 0=%s" --net:"Network 1=%s" --net:"Network 2=%s" \
--net:"Network 3=%s" --prop:nsx_ip_0=%s --prop:nsx_netmask_0=%s --prop:nsx_gateway_0=%s --prop:nsx_dns1_0=%s --prop:nsx_domain_0=%s --prop:nsx_ntp_0=%s \
--prop:nsx_isSSHEnabled=True --prop:nsx_allowSSHRootLogin=True \
--prop:nsx_passwd_0=%s --prop:nsx_cli_passwd_0=%s --prop:nsx_hostname=%s %s \
vi://"%s":"%s"@"%s"/%s/host/%s """ %(app_name,disk_mode,vc_ds,esg_nw0,esg_nw1,esg_nw2,esg_nw3,app_ip,app_mask,ctr_gateway,ctr_dns1_0,vc_domain,ctr_ntp,ctr_pass,ctr_cli_pass,app_name,ovfname,vc_user,vc_pass,vc,vc_dc,vc_cluster)
    return deploy_script


print "*" * 100
print "NSX components Deployment"
mgt=script(mgr_ip,ctr_mask,mgr_name,mgr_file)
ctr1=script(ctr1_ip,ctr_mask,ctr1_name,ctr_file)
ctr2=script(ctr2_ip,ctr_mask,ctr2_name,ctr_file)
ctr3=script(ctr3_ip,ctr_mask,ctr3_name,ctr_file)
edge1=esg_script(edge1_ip,ctr_mask,edge1_name,esg_file)
edge2=esg_script(edge2_ip,ctr_mask,edge2_name,esg_file)

os.system(mgt)
os.system(ctr1)
os.system(ctr2)
os.system(ctr3)
os.system(edge1)
os.system(edge2)
time.sleep(180)

###########################################################################################################
# NSX initilaization
###########################################################################################################
print "*" * 100
print "NSX components Registration"
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(mgr_ip,username=nsx_user,password=nsx_pass)
stdin,stdout,stderr=ssh.exec_command("get certificate api thumbprint")
mgr_tp=stdout.readlines()[0]
print mgr_tp

def ctr_reg(ctr):
    print ctr+" is on process"
    ssh.connect(ctr,username=nsx_user,password=nsx_pass)
    stdin,stdout,stderr=ssh.exec_command("join management-plane %s username %s password %s thumbprint %s"%(mgr_ip,nsx_user,nsx_pass,mgr_tp))
    print stdout.readlines()[0]
    stdin,stdout,stderr=ssh.exec_command("set control-cluster security-model shared-secret secret vmware")
    print stdout.readlines()[0]
    stdin,stdout,stderr=ssh.exec_command("get control-cluster certificate thumbprint")
    ctr_tp=stdout.readlines()[0]
    return ctr_tp

def ctr_master(master):
    print "master controller activation"
    ssh.connect(master,username=nsx_user,password=nsx_pass)
    stdin,stdout,stderr=ssh.exec_command("initialize control-cluster")
    print stdout.readlines()[0]

def ctr_join(master,ctr_ip,ctr_tp):
    print ctr_ip+" is joining"
    ssh.connect(master,username=nsx_user,password=nsx_pass)
    stdin,stdout,stderr=ssh.exec_command("join control-cluster %s thumbprint %s"%(ctr_ip,ctr_tp))
    print stdout.readlines()[0]
    stdin,stdout,stderr=ssh.exec_command("activate control-cluster")
    print stdout.readlines()[0]

def esg_reg(esg):
    print esg+" is on process" 
    ssh.connect(esg,username=nsx_user,password=nsx_pass)
    stdin,stdout,stderr=ssh.exec_command("join management-plane %s username %s password %s thumbprint %s"%(mgr_ip,nsx_user,nsx_pass,mgr_tp))

ctr1_tp=ctr_reg(ctr1_ip)
print ctr1_tp
ctr2_tp=ctr_reg(ctr2_ip)
print ctr2_tp
ctr3_tp=ctr_reg(ctr3_ip)
print ctr3_tp
ctr_master(ctr1_ip)
ctr_join(ctr1_ip,ctr2_ip,ctr2_tp)
ctr_join(ctr1_ip,ctr3_ip,ctr3_tp)
esg_reg(edge1_ip)
esg_reg(edge2_ip)
