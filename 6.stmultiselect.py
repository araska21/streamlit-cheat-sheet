import streamlit as st

st.header('st.multiselect')

options = st.multiselect(
     '가장 좋아하는 색상은 무엇인가요',
     ['초록', '노랑', '빨강', '파랑'],
     ['노랑', '빨강'])

st.write('당신이 선택한 색상:', options)
