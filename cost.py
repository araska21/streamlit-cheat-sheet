import streamlit as st
import requests
import pandas as pd

def fetch_material_prices():
    # API 엔드포인트 URL (실제 API 주소로 대체해야 함)
    api_url = "https://your-material-price-api.com/prices"
    
    try:
        # API 요청
        response = requests.get(api_url)
        response.raise_for_status()  # 오류 발생 시 예외 처리
        
        # JSON 데이터를 DataFrame으로 변환
        prices_data = response.json()
        df = pd.DataFrame(prices_data)
        
        return df
    
    except requests.RequestException as e:
        st.error(f"API 요청 중 오류 발생: {e}")
        return None

def main():
    # 페이지 제목 설정
    st.title("재료비 가격 조회 애플리케이션")
    
    # 재료비 데이터 불러오기
    st.header("최근 재료비 가격")
    
    # 데이터 페치
    price_data = fetch_material_prices()
    
    if price_data is not None:
        # 데이터 테이블 표시
        st.dataframe(price_data)
        
        # 검색 기능 추가
        search_term = st.text_input("재료명으로 검색:")
        if search_term:
            filtered_data = price_data[price_data['name'].str.contains(search_term, case=False)]
            st.dataframe(filtered_data)
        
        # 차트 옵션 추가
        st.header("가격 추이 차트")
        chart_type = st.selectbox("차트 유형 선택", ["선 그래프", "막대 그래프"])
        
        if chart_type == "선 그래프":
            st.line_chart(price_data.set_index('name')['price'])
        else:
            st.bar_chart(price_data.set_index('name')['price'])

if __name__ == "__main__":
    main()