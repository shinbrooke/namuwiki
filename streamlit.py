#import settings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from bokeh.plotting import figure
from datetime import datetime

#data loading
# st.cache를 이용하여 데이터 로딩을 하는 함수
@st.cache #데이터를 불러와서 메모리에 가지고 있는 것 (매번 불러오기 번거롭기 때문)
def load_data(filename):
    data = pd.read_csv(filename)
    return data

#df0 = load_data("")
df_culture0 = load_data('dataculture.csv')
#df_social0 = load_data('datasocial.csv')
df_academic0 = load_data('dataacademic.csv')

df_culture = df_culture0.copy()
#df_social = df_social0.copy()
df_academic = df_academic0.copy()

# 3개의 csv 파일에 대해 date, time 칼럼 합치고 데이터타입 datetime으로 변경
df_culture['datetime'] = df_culture['date'] + " " + df_culture['time']
df_culture = df_culture.drop(['date', 'time'], axis=1)
df_culture['datetime'] = pd.to_datetime(df_culture['datetime'])

#df_social['datetime'] = df_social['date'] + " " + df_social['time']
#df_social = df_social.drop(['date', 'time'], axis=1)
#df_social['datetime'] = pd.to_datetime(df_social['datetime'])

df_academic['datetime'] = df_academic['date'] + " " + df_academic['time']
df_academic = df_academic.drop(['date', 'time'], axis=1)
df_academic['datetime'] = pd.to_datetime(df_academic['datetime'])


st.subheader("2022-2 데이터 저널리즘 과제전")
st.title("나무위키 활용 학습의 가능성과 한계")
st.write("10조: 서정빈, 신부경, 정민제")

#1. 문제의식 서술
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 문제의식")
with st.expander("문제의식 설명"):
    st.write("나무위키")
    st.write("설명")

#2. 데이터 소개
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 소개")

#나무위키 대분류 3개에서 어떻게 랜덤하게 키워드를 선별해서 history 크롤링했는지 간단히 언급 필요
#나무위키 history 페이지 캡처해서 설명하면 좋을 것 같아요! - 정빈

st.write('크롤링한 데이터를 데이터프레임으로 정리한 것은 아래와 같다.')

st.write("대중문화 및 서브컬처 분야 키워드: '앵그리버드 시리즈', '팬텀(메이플스토리)', 'SSG 랜더스/2021년/5월', '마이 네임', '게임 서버', '사랑의 불시착', 'ITZY', '트랜스포머: 사라진 시대', 'SKY 캐슬', '레디메이드 인생'")
st.write(df_culture)

culture_radio = ['앵그리버드 시리즈', '팬텀(메이플스토리)', 'SSG 랜더스/2021년/5월', '마이 네임', '게임 서버', '사랑의 불시착', 'ITZY', '트랜스포머: 사라진 시대', 'SKY 캐슬', '레디메이드 인생']
culture_status = st.radio('대중문화 및 서브컬처 분야', culture_radio)

if culture_status == culture_radio[0]:
    st.write(df_culture['page' == 'angrybird'])
elif culture_status == culture_radio[1]:
    st.write(df_culture['page' == 'phantom'])




#st.write("일반사회 분야 키워드: '대학수학능력시험', '폭염', '사이버대학', '오마이뉴스', '인터넷 은어', '커뮤니티의 금기', 'i안심', '중앙선거관리위원회', '미제사건', '필카'")
#st.write(df_social)

st.write("학문 분야 키워드: '파스칼의 삼각형', '전염병', '미학', '몬티 홀 문제', '임진왜란', '공용어', '그리스 로마 신화', '조명 효과', '1956년 헝가리 혁명', '통화'")
st.write(df_academic)

#3. 데이터 분석
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 분석 결과")
st.markdown("***1. 페이지 수정한 사용자의 수***")

st.markdown("***2. 페이지 수정 총 횟수***")
# 키워드(페이지) 종류 확인
page_culture = df_culture.groupby('page')
#page_social = df_social.groupby('page')
page_academic = df_academic.groupby('page')

col1, col2 = st.columns(2) #한 줄에 2개의 column을 나열함
with col1:
    st.write("대중문화/서브컬처 관련")
    st.write(page_culture.size())
with col2:
    st.write("학문 관련")
    st.write(page_academic.size())

#st.write(page_social.size())

st.markdown("***3. 수정 양상***")
st.markdown("*3.1. 삭제 vs 추가 횟수*")

st.markdown("*3.2. 시간에 따른 수정 양상 변화*")
