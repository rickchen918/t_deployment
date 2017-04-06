import requests,json,base64,paramiko
requests.packages.urllib3.disable_warnings()

mgr="192.168.64.186"
ctr1="192.168.64.110"
ctr2="192.168.64.111"
ctr3="192.168.64.112"
user="admin"
passwd="Nicira123$"


ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(mgr,username=user,password=passwd)
stdin,stdout,stderr=ssh.exec_command("get certificate api thumbprint")
mgr_tp=stdout.readlines()[0]
print mgr_tp

#stdin,stdout,stderr=ssh.exec_command("set service install-upgrade enable")
#print stdout.readlines()[0]

def mgt_reg(ctr):
    ssh.connect(ctr,username=user,password=passwd)
    stdin,stdout,stderr=ssh.exec_command("join management-plane %s username %s password %s thumbprint %s"%(mgr,user,passwd,mgr_tp))
    print stdout.readlines()[0]
    stdin,stdout,stderr=ssh.exec_command("set control-cluster security-model shared-secret secret vmware")
    print stdout.readlines()[0]
    stdin,stdout,stderr=ssh.exec_command("get control-cluster certificate thumbprint")
    ctr_tp=stdout.readlines()[0]
    return ctr_tp

mgt_reg(ctr1)
ctr1_tp=mgt_reg(ctr1)
print ctr1_tp
mgt_reg(ctr2)
ctr2_tp=mgt_reg(ctr2)
print ctr2_tp
mgt_reg(ctr3)
ctr3_tp=mgt_reg(ctr3)
print ctr3_tp



