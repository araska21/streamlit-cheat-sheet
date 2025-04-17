import streamlit as st
import pandas as pd
import json
import os
import hashlib
from datetime import datetime
import re

class UserManager:
    def __init__(self, db_path='users.json'):
        self.db_path = db_path
        self.users = self.load_users()

    def load_users(self):
        """사용자 데이터 로드"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_users(self):
        """사용자 데이터 저장"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def hash_password(self, password):
        """비밀번호 해시화"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_email(self, email):
        """이메일 형식 검증"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def validate_password(self, password):
        """
        비밀번호 복잡성 검증
        - 최소 8자 이상
        - 대문자, 소문자, 숫자, 특수문자 포함
        """
        if len(password) < 8:
            return False
        
        # 대문자, 소문자, 숫자, 특수문자 포함 여부 확인
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        return has_upper and has_lower and has_digit and has_special

    def register_user(self, username, password, email):
        """사용자 등록"""
        # 입력 데이터 검증
        if not username or not password or not email:
            return "모든 필드를 입력해주세요."
        
        if username in self.users:
            return "이미 존재하는 아이디입니다."
        
        if not self.validate_email(email):
            return "유효하지 않은 이메일 형식입니다."
        
        if not self.validate_password(password):
            return "비밀번호는 8자 이상이며, 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다."

        # 사용자 정보 생성
        self.users[username] = {
            'password': self.hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        self.save_users()
        return "회원가입 성공"

    def login_user(self, username, password):
        """사용자 로그인"""
        if username not in self.users:
            return False

        hashed_password = self.hash_password(password)
        if self.users[username]['password'] == hashed_password:
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True
        
        return False

def load_material_data(file_path=r'C:\Users\Cloud\Documents\train\가격정보.xlsx'):
    """엑셀 파일에서 자재 데이터를 불러오는 함수"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    
    except FileNotFoundError:
        st.error(f"파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"파일을 불러오는 중 오류 발생: {e}")
        return None

def search_materials(df, search_term, price_min, price_max, search_column, price_column):
    """품목명과 가격 범위로 복합 검색하는 함수"""
    try:
        filtered_df = df.copy()
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df[search_column].str.contains(search_term, case=False, na=False)
            ]
        
        filtered_df = filtered_df[
            (filtered_df[price_column] >= price_min) & 
            (filtered_df[price_column] <= price_max)
        ]
        
        return filtered_df
    
    except Exception as e:
        st.error(f"검색 중 오류 발생: {e}")
        return pd.DataFrame()

def search_system(user_manager):
    """검색 시스템 메인 함수"""
    st.title(f'🔍 품목 및 가격 복합 검색 시스템')
    
    # 데이터 로드
    materials_df = load_material_data()
    
    if materials_df is not None:
        # 사이드바 설정
        st.sidebar.header('🔎 검색 옵션')
        
        # 검색 컬럼 선택 (문자열 컬럼)
        search_columns = materials_df.select_dtypes(include=['object']).columns.tolist()
        search_column = st.sidebar.selectbox('검색 컬럼 선택', search_columns)
        
        # 가격 컬럼 선택 (숫자 컬럼)
        price_columns = materials_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        price_column = st.sidebar.selectbox('가격 컬럼 선택', price_columns)
        
        # 품목명 검색 입력
        search_term = st.sidebar.text_input('품목명 검색:')
        
        # 가격 범위 입력
        col1, col2 = st.sidebar.columns(2)
        with col1:
            min_price = st.number_input(
                '최소 가격', 
                min_value=0, 
                value=0, 
                step=100
            )
        
        with col2:
            max_price = st.number_input(
                '최대 가격', 
                min_value=min_price, 
                value=int(materials_df[price_column].max()), 
                step=100
            )
        
        # 검색 버튼
        if st.sidebar.button('검색'):
            # 복합 검색 실행
            filtered_df = search_materials(
                materials_df, 
                search_term, 
                min_price, 
                max_price, 
                search_column, 
                price_column
            )
            
            # 결과 표시
            if not filtered_df.empty:
                st.subheader(f"검색 결과")
                
                # 검색 조건 표시
                search_condition = f"""
                - 검색 컬럼: {search_column}
                - 품목명: {search_term if search_term else '전체'}
                - 가격 범위: {min_price}원 ~ {max_price}원
                """
                st.markdown(search_condition)
                
                # 검색 결과 표시
                st.dataframe(filtered_df)
                
                # 결과 통계 (건수만)
                st.metric(
                    label="검색 결과 건수", 
                    value=f"{len(filtered_df)}건"
                )
                
            else:
                st.warning('검색 결과가 없습니다.')

def main():
    st.set_page_config(
        page_title="복합 검색 시스템", 
        layout="wide"
    )
    
    # 사용자 관리자 초기화
    user_manager = UserManager()

    # 세션 상태 초기화
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    # 사이드바 메뉴
    menu = st.sidebar.selectbox(
        "메뉴", 
        ["로그인", "회원가입"] if not st.session_state.logged_in else ["검색 시스템", "로그아웃"]
    )

    # 로그인 상태에 따른 메뉴 처리
    if not st.session_state.logged_in:
        if menu == "로그인":
            st.sidebar.header("🔐 로그인")
            login_username = st.sidebar.text_input("아이디")
            login_password = st.sidebar.text_input("비밀번호", type="password")
            
            if st.sidebar.button("로그인"):
                if user_manager.login_user(login_username, login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.rerun()
                else:
                    st.sidebar.error("아이디 또는 비밀번호가 잘못되었습니다.")

        elif menu == "회원가입":
            st.sidebar.header("🆕 회원가입")
            new_username = st.sidebar.text_input("새 아이디")
            new_password = st.sidebar.text_input("비밀번호", type="password")
            new_password_confirm = st.sidebar.text_input("비밀번호 확인", type="password")
            new_email = st.sidebar.text_input("이메일 주소")
            
            if st.sidebar.button("회원가입"):
                # 비밀번호 일치 확인
                if new_password != new_password_confirm:
                    st.sidebar.error("비밀번호가 일치하지 않습니다.")
                else:
                    result = user_manager.register_user(new_username, new_password, new_email)
                    if result == "회원가입 성공":
                        st.sidebar.success(result)
                    else:
                        st.sidebar.error(result)

    else:
        if menu == "검색 시스템":
            st.title(f'🖐️ {st.session_state.username}님 환영합니다!')
            search_system(user_manager)

        elif menu == "로그아웃":
            st.sidebar.header("로그아웃")
            st.sidebar.write("정말 로그아웃 하시겠습니까?")
            
            if st.sidebar.button("확인"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.rerun()

if __name__ == '__main__':
    main()