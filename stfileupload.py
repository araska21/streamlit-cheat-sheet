import streamlit as st
import pandas as pd

st.title('st.file_uploader')

st.subheader('CSV 입력')
uploaded_file = st.file_uploader("파일 선택")

if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.subheader('DataFrame')
  st.write(df)
  st.subheader('기술 통계')
  st.write(df.describe())
else:
  st.info('☝️ CSV 파일을 업로드하세요')
