import streamlit as st

# Title for the Streamlit web app
st.set_page_config(page_title="View_File")
st.sidebar.markdown("# View_File")
st.sidebar.markdown("View, check and modify some files on the system")
st.title("View_File")

option = st.selectbox('view files: ',('user', 'password','note'))
if option:
    if option is 'user':
        file = "./winhack/user"
    elif option is 'password':
        file = "./winhack/password"
    elif option is 'note':
        file = "./winhack/note"
    f = open(file,"r")
    content = f.read()
    f.close()
    update_content = st.text_area("",content,height=800)
    if st.button("update file"):
        try:
                fw = open(file, "w")
                fw.write(update_content)
                st.success("Command executed successfully.")
        except subprocess.CalledProcessError as e:
                st.error(f"Error executing the command: {e}")
