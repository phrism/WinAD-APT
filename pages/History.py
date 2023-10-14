from  utils import *

st.set_page_config(page_title="History",layout="wide")

st.sidebar.markdown("# History")
st.sidebar.markdown("History of executing command")
st.title("History")

st.subheader("Command History:")
for i in range(0,len(st.session_state.command_history)):
	rev_i = len(st.session_state.command_history)-i-1
	st.write(f"**Command {rev_i}:**")
	st.code(st.session_state.command_history[rev_i])
	st.write(f"**Output {rev_i}:**")
	with st.expander("See Output"):
		st.code(st.session_state.output_history[rev_i])

