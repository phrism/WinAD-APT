import streamlit as st
import subprocess
from utils import *



st.set_page_config(page_title="nmap",layout= "wide")
st.sidebar.markdown("# Nmap")
st.sidebar.markdown("use nmap to scan open port and fist-step information")

css='''
<style>
    section.main > div {max-width:75rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)
st.session_state.show_command = st.sidebar.checkbox("Show command", True)

st.title("Nmap")
st.info("Current Target IP :  "+st.session_state.ip)
parameters = ""
with st.form('set_target'):
    c1, c2,c3,c4,c5,c6,c7,c8 = st.columns([1,1,1,1,1,1,1,1]) 
    with c1:
        sV = st.checkbox('-sV')
    with c2:
        sT = st.checkbox('-sT')
    with c3:
        sU = st.checkbox('-sU')
    with c4:
        sS = st.checkbox('-sS')
    with c5:
        sC = st.checkbox('-sC')
    with c6:
        sn = st.checkbox('-sn')
    with c7:
        A = st.checkbox('-A')
    with c8:
        Pn = st.checkbox('-Pn')
    with st.container():
        col1,col2 =st.columns([1,15])
        with col1:
            p = st.checkbox('-p')
        with col2:
            ports = st.text_input("ports",placeholder="scan ports, example: 22,80,8080",label_visibility='collapsed')
    with st.container():
        col1,col2 =st.columns([1,9])
        with col1:
            script = st.checkbox('--script')
        with col2:
            scripts = st.text_input("scripts",placeholder="scrip, example: 'smb*'",label_visibility='collapsed')
    
    if sV:
        parameters += " -sV"
    if sT:
        parameters += " -sT"
    if sU:
        parameters += " -sU"
    if sS:
        parameters += " -sS"
    if sC:
        parameters += " -sC"
    if sn:
        parameters += " -sn"
    if A:
        parameters += " -A"
    if Pn:
        parameters += " -Pn"
    if p and ports:
        parameters += " -p " +ports
    if script and scripts:
        parameters += " --script "+ scripts

    with st.expander("See notes"):
        st.markdown("""
    use nmap as the first step to gather information\n
    default parameters: -sV -sC -Pn -A -T4\n
    -Pn : For the cases that windows server cannot be pinged\n
    -sV : Probe open ports to determine service/version info\n
    -sC : --script=default\n
    -A : all ports scanned, which is considered be worth to do\n
    -T4 : speed up the nmap process\n
    """)
    if parameters is "":
        parameters = " -sV -sC -Pn -A "
    if st.form_submit_button("Execute!"):    
        if st.session_state.ip:
            command = "nmap{} -T4 ".format(parameters)+ st.session_state.ip
            run_command(command )
            show_command(command)
        else:
            warning("missing", "ip")


with st.form('set_target_domain'):
    col1, col2 = st.columns([3,1]) 
    with col1:
        st.session_state.domain = st.text_input("target_domain",placeholder="Input your target domain here",label_visibility='collapsed')
    # Use the second column for the submit button
    with col2:
        button = st.form_submit_button("submit")
    if button:
        st.success("success")