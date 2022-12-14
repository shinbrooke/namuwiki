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
df_culture = load_data('dataculture.csv')
df_social = load_data('datasocial.csv')
df_academic = load_data('dataacademic.csv')
#df = df0.copy()

#df_culture['datetime'] = df_culture['date'] + " " + df_culture['time']
#df_culture = df_culture.drop(['date', 'time'], axis=1)
#df_culture['datetime'] = pd.to_datetime(df_culture['datetime'])

#df_social['datetime'] = df_social['date'] + " " + df_social['time']
#df_social = df_social.drop(['date', 'time'], axis=1)
#df_social['datetime'] = pd.to_datetime(df_social['datetime'])

df_academic['datetime'] = df_academic['date'] + " " + df_academic['time']
df_academic = df_academic.drop(['date', 'time'], axis=1)
df_academic['datetime'] = pd.to_datetime(df_academic['datetime'])

st.write(df_academic) #test

st.subheader("2022-2 데이터 저널리즘 과제전")
st.title("나무위키 활용 학습의 가능성과 한계")
st.write("10조: 서정빈, 신부경, 정민제")

#문제의식 서술
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 문제의식")

#데이터 소개
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 소개")

#데이터 분석
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 분석 결과")
