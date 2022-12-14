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
df_social0 = load_data('datasocial.csv')
df_academic0 = load_data('dataacademic.csv')

df_culture = df_culture0.copy()
df_social = df_social0.copy()
df_academic = df_academic0.copy()

# 3개의 csv 파일에 대해 date, time 칼럼 합치고 데이터타입 datetime으로 변경
df_culture['datetime'] = df_culture['date'] + " " + df_culture['time']
df_culture = df_culture.drop(['date', 'time'], axis=1)
df_culture['datetime'] = pd.to_datetime(df_culture['datetime'])

df_social['datetime'] = df_social['date'] + " " + df_social['time']
df_social = df_social.drop(['date', 'time'], axis=1)
df_social['datetime'] = pd.to_datetime(df_social['datetime'])

df_academic['datetime'] = df_academic['date'] + " " + df_academic['time']
df_academic = df_academic.drop(['date', 'time'], axis=1)
df_academic['datetime'] = pd.to_datetime(df_academic['datetime'])


st.subheader("2022-2 데이터 저널리즘 과제전")
st.title("나무위키 활용 학습의 가능성과 한계")
st.write("10조: 서정빈, 신부경, 정민제")

#1. 문제의식 서술
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 문제의식")

#2. 데이터 소개
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 소개")

#나무위키 history 페이지 캡처해서 설명하면 좋을 것 같아요! - 정빈

st.write('크롤링한 데이터를 데이터프레임으로 정리한 것은 아래와 같다.')
st.write(df_culture)
#st.write(df_social)
st.write(df_academic)

#3. 데이터 분석
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 분석 결과")


# 키워드(페이지) 종류 확인
page_culture = df_culture.groupby('page')
page_social = df_social.groupby('page')
page_academic = df_academic.groupby('page')

st.write(page_culture.size())
st.write(page_social.size())
st.write(page_academic.size())
