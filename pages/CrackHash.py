import streamlit as st
import subprocess
from utils import run_command
from utils import show_command 



st.set_page_config(page_title="crack hash")
st.sidebar.markdown("# crackhash")
st.sidebar.markdown("Hashcat or john to crack the password")
st.title("crack hash")
st.session_state.show_command = st.sidebar.checkbox("Show command", True)
    


# Input text box for entering the command
option = st.selectbox('hash format',('john', 'hashcat'))
hash_value = st.text_area("hash value:",height=400)
wordlist = st.text_input("wordlist","/usr/share/wordlists/rockyou.txt")
if st.button("crack!"):
    if hash_value and option:
        if option is 'john':
            command = "echo '{}' >  ./winhack/hash;john ./winhack/hash --wordlist={};rm ./winhack/hash".format(hash_value,wordlist)
            run_command(command )
            show_command(command)
        else:
            command = "hashcat -a 0 '{}' {}".format(hash_value,wordlist)
            run_command(command )
            show_command(command)
    else:
        st.warning("Please enter a command.")