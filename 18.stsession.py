import streamlit as st

st.title('st.session_state')

def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs/2.2046
def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg*2.2046

st.header('입력')
col1, spacer, col2 =st.columns([2,1,2])
with col1:
    pounds = st.number_input("파운드:", key ="lbs", on_change = lbs_to_kg)
with col2:
    kilogram = st.number_input("킬로그램:", key = "kg", on_change = kg_to_lbs)

st.header('출력')
st.write("st.session_state 객체:", st.session_state)