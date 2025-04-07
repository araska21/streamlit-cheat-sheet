import streamlit as st

st.title('st.experimental_get_query_params')

with st.expander('이 앱에 대하여'):
  st.write("`st.experimental_get_query_params`는 사용자 브라우저의 URL에서 직접 쿼리 매개변수를 검색할 수 있게 해줍니다.")

# 1. 지침
st.header('1. 지침')
st.markdown('''
인터넷 브라우저의 URL 바에서 다음을 추가하세요:
`?firstname=Jack&surname=Beanstalk`
기본 URL `http://share.streamlit.io/dataprofessor/st.experimental_get_query_params/` 뒤에 추가하여
`http://share.streamlit.io/dataprofessor/st.experimental_get_query_params/?firstname=Jack&surname=Beanstalk`가 되도록 합니다.
''')


# 2. st.experimental_get_query_params의 내용
st.header('2. st.experimental_get_query_params의 내용')
st.write(st.experimental_get_query_params())


# 3. URL에서 정보 검색 및 표시
st.header('3. URL에서 정보 검색 및 표시')

firstname = st.experimental_get_query_params()['firstname'][0]
surname = st.experimental_get_query_params()['surname'][0]

st.write(f'안녕하세요 **{firstname} {surname}**, 어떠세요?')
