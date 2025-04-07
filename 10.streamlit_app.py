import streamlit as st

st.title('Streamlit 앱의 테마 사용자 정의하기')

st.write('이 앱의 `.streamlit/config.toml` 파일 내용')

st.code("""
[theme]
primaryColor="#F39C12"
backgroundColor="#2E86C1"
secondaryBackgroundColor="#AED6F1"
textColor="#FFFFFF"
font="monospace"
""")

number = st.sidebar.slider('숫자를 선택하세요:', 0, 10, 5)
st.write('슬라이더 위젯에서 선택된 숫자:', number)
