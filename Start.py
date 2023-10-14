# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import os

LOGGER = get_logger(__name__)

if 'ip' not in st.session_state:
    st.session_state.ip = ""
if 'domain' not in st.session_state:
    st.session_state.domain = ""


def run():
    
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋",
    )
    css='''
    <style>
        section.main > div {max-width:75rem}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
    st.write("# Welcome to WinAD-APT! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        WinAD-APT is for windows AD auto pentesting framework,
        this framework is made using streamlit and python, which is used to make windows AD exploit more easily. 
        The framework is still being developed, it is welcomed to commnicate and share some ideas.
        **👈 Select a demo from the sidebar** to start your windows AD hacking journey
        ### What can this framwork do?
        - Simple nmap function for entrence ip
        - Auto gather information and possible username and password of target
        - Auto LateralPenetration from one account to another
        - Auto Privilege Escalation
        ### How to use my framework?
        - Started by adding a targte ip in **this** page
        - Find the target domain using nmap and add it to **this** page
        - Other things you can just type in and click, the result will show to U after the command is complete
        - All your histoy command is in history page
        - [CAUTION] Do not refresh any page even if it went something wrong !!! It is no difference with rerun the whole app and U will lose everything
        ### First thing to do
        The first thing for pentesting a target —— is to set a target! U can set a target blow and start 
        your journey of pentesting:
        """
    )
    with st.form('set_target_ip'):
        col1, col2 = st.columns([3,1]) 
        with col1:
            st.session_state.ip = st.text_input("target_ip",placeholder="Input your target ip here",label_visibility='collapsed')
        # Use the second column for the submit button
        with col2:
            button = st.form_submit_button("submit")
        if button:
            st.success("success")


    st.markdown(
        """
        It is recommand to start NMAP page to scan your target , and get the basic information of your pentesing target
        """
    )
    st.info("note : please do not let others visit your streamlit website! It is dangerous!")


if __name__ == "__main__":
    run()
