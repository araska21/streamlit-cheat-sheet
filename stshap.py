import streamlit as st
from streamlit_shap import st_shap
import shap
from sklearn.model_selection import train_test_split
import xgboost
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return shap.datasets.adult()

@st.cache_data
def load_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
    d_train = xgboost.DMatrix(X_train, label=y_train)
    d_test = xgboost.DMatrix(X_test, label=y_test)
    params = {
        "eta": 0.01,
        "objective": "binary:logistic",
        "subsample": 0.5,
        "base_score": np.mean(y_train),
        "n_jobs": -1,
    }
    model = xgboost.train(params, d_train, 10, evals = [(d_test, "test")], verbose_eval=100, early_stopping_rounds=20)
    return model

st.title("`streamlit-shap`로 Streamlit 앱에서 SHAP 플롯 표시하기")

with st.expander('앱에 대하여'):
    st.markdown('''[`streamlit-shap`](https://github.com/snehankekre/streamlit-shap)는 [SHAP](https://github.com/slundberg/shap)플롯을 [Streamlit](https://streamlit.io/)에서 표시하기 위한 래퍼를 제공하는 streamlit 컴포넌트입니다.
                이 라이브러리는 저희 내부 직원인 [스네한 케크레](https://github.com/snehankekre)가 개발했으며, [Streamlit 문서화](https://docs.streamlit.io/) 웹사이트도 관리합니다.
                ''')
    
st.header('입력 데이터')
X, y = load_data()
X_display, y_display = shap.datasets.adult(display=True)

with st.expander('데이터에 대하여'):
    st.write('예시 데이터셋으로 성인 인구 조사 데이터를 사용합니다.')
with st.expander('X'):
    st.dataframe(X)
with st.expander('y'):
    st.dataframe(y)

st.header('SHAP 출력')

model = load_model(X, y)

explainer = shap.Explainer(model, X)
shap_values = explainer(X)

with st.expander('워터폴 플롯'):
    st_shap(shap.plots.waterfall(shap_values[0]), height=300)
with st.expander('비스윔 플롯'):
    st_shap(shap.plots.beeswarm(shap_values), height=300)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

with st.expander('포스 플롯'):
    st.subheader('첫 번째 데이터 인스턴스')
    st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:],X_display.iloc[0,:]), height=200, width=1000)
    st.subheader('첫 천 번째 데이터 인스턴스')
    st_shap(shap.force_plot(explainer.expected_value, shap_values[:1000,:], X_display.iloc[:1000,:]), height=400, width=1000)
