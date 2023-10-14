import streamlit as st
import subprocess
import inspect
import textwrap
import random
import string
import time 
import os

if 'output_history' not in st.session_state:
	st.session_state.output_history = []
if 'command_history' not in st.session_state:
    st.session_state.command_history = []
if 'show_command' not in st.session_state:
	st.session_state.show_command = ''
def init():
	if 'username' not in st.session_state:
		st.session_state.username = ''
	if 'password' not in st.session_state:
		st.session_state.password = ''
	if 'user_hash' not in st.session_state:
		st.session_state.user_hash = ''
	if 'ticket_file_path' not in st.session_state:
		st.session_state.ticket_file_path = ''

def run_command(command):
	if command:
		try:
			result = subprocess.run(
				command, shell=True, text=True, capture_output=True
			)
			if not result.stdout:
				output = result.stderr
			else:
				output = result.stdout
			st.success("Command executed successfully.")
			st.write("Output:")
			st.session_state.output_history.append(output)
			st.code(st.session_state.output_history[-1])
		except subprocess.CalledProcessError as e:
			st.error(f"Error executing the command: {e}")
	return output

def show_command(command):
    
    st.session_state.command_history.append(command)
    if st.session_state.show_command:
        st.markdown("## Command")
        st.code(st.session_state.command_history[-1])

def DC_format(domain):
	DCs  = domain.split(".")
	DC_string = ""
	for DC in DCs:
		DC_string += "DC={},".format(DC)
	return DC_string[:-1]

def GROUP_format(group_name):
	group = group_name.split("@")[0]
	DC = group_name.split("@")[1]
	flat_group = "OU={},".format(group)
	flat_group += DC_format(DC)
	return flat_group

	

def get_date_diff(ip):
	result = subprocess.run("ntpdate {}".format(ip), shell=True, text=True, capture_output=True)
	output = result.stdout
	result = subprocess.run("date -d '{}' +%s".format(output.split(".")[0]), shell=True, text=True, capture_output=True)
	output = result.stdout
	diff = int((int(output) - int(time.time()))/3600)
	if diff>0:
		return "+"+str(diff)
	else:
		return str(diff)

def create_folder(path):
	letters = string.ascii_lowercase
	folder_name = ''.join(random.choice(letters) for _ in range(5))
	folder_path = os.path.join(path, folder_name)
	while  os.path.exists(folder_path):
		folder_name = ''.join(random.choice(letters) for _ in range(5))
		folder_path = os.path.join(path, folder_name)
	os.mkdir(folder_path)
	return folder_name

def warning(options, string):
	if options is "missing":
		st.warning("Missing {} input, please check and try again".format(string))
	if options is "select":
		st.warning("Please select a credential to use")