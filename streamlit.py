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

#나무위키 대분류 3개에서 어떻게 랜덤하게 키워드를 선별해서(선별기준) history 크롤링했는지 간단히 언급 필요
#나무위키 history 페이지 캡처해서 설명하면 좋을 것 같아요! - 정빈

st.write('크롤링한 데이터를 데이터프레임으로 정리한 것은 아래와 같다.')

# 대분류별 키워드 리스트
culture_list = ['angrybird', 'crashlandingonyou', 'gameserver', 'itzy', 'maplephantom', 'myname', 'readymadelife', 'skycastle', 'ssglanders', 'transformer']
#social_list = ['']
academic_list = ['aesthetic', 'call', 'epidemic', 'greekromanmyth', 'hungarianrevolution', 'imjin', 'montyhall', 'officiallanguage', 'pascaltriangle', 'spotlight']

#전체 데이터
st.write("대중문화 및 서브컬처 분야 키워드: '앵그리버드 시리즈', '사랑의 불시착', '게임 서버', 'ITZY', '팬텀(메이플스토리)', '마이 네임', '레디메이드 인생', 'SKY 캐슬', 'SSG 랜더스/2021년/5월', '트랜스포머: 사라진 시대'")
st.write(df_culture)

#라디오
culture_radio = ['앵그리버드 시리즈', '사랑의 불시착', '게임 서버', 'ITZY', '팬텀(메이플스토리)', '마이 네임', '레디메이드 인생', 'SKY 캐슬', 'SSG 랜더스/2021년/5월', '트랜스포머: 사라진 시대']
culture_status = st.radio('대중문화 및 서브컬처 분야', culture_radio)

for i in range(len(culture_radio)):
    if culture_status == culture_radio[i]:
        st.write(df_culture[df_culture['page'] == culture_list[i]])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

#st.write("일반사회 분야 키워드: '대학수학능력시험', '폭염', '사이버대학', '오마이뉴스', '인터넷 은어', '커뮤니티의 금기', 'i안심', '중앙선거관리위원회', '미제사건', '필카'")
#st.write(df_social)

#전체 데이터
st.write("학문 분야 키워드: '미학', '통화', '전염병', '그리스 로마 신화', '1956년 헝가리 혁명', '임진왜란', '몬티 홀 문제', '공용어', '파스칼의 삼각형', '조명 효과'")
st.write(df_academic)

#라디오
academic_radio = ['미학', '통화', '전염병', '그리스 로마 신화', '1956년 헝가리 혁명', '임진왜란', '몬티 홀 문제', '공용어', '파스칼의 삼각형', '조명 효과']
acadamic_status = st.radio('학문 분야', academic_radio)

# 위 코드랑 똑같은데 학문 분야도 라디오 기능 쓰려니까 오류 나네요.. 일단 각주처리해놓겠습니다!
#for i in range(len(academic_radio)):
#    if acadamic_status == acadamic_radio[i]:
#        st.write(df_acadamic[df_acadamic['page'] == acadamic_list[i]])

#3. 데이터 분석
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 데이터 분석 결과")

# 키워드(페이지)별로 데이터프레임 저장
for i in range(len(culture_list)):
  globals()[culture_list[i]] = df_culture[df_culture['page'] == culture_list[i]]
for i in range(len(academic_list)):
  globals()[academic_list[i]] = df_academic[df_academic['page'] == academic_list[i]]

st.markdown("***1.1. 페이지 수정한 사용자의 수***")
# 대중문화 분야
st.write('대중문화 분야')
for i in range(len(culture_list)):
    st.write(culture_radio[i], len(globals()[culture_list[i]].groupby('uname'))) #한글 키워드 출력

# 학문 분야
st.write('학문 분야')
for i in range(len(academic_list)):
    st.write(academic_radio[i], len(globals()[academic_list[i]].groupby('uname'))) #한글 키워드 출력

st.markdown("***1.2. 사용자별 편집 횟수***")  
st.write('# 이 부분도 라디오 기능을 쓰거나 좀 더 가독성 있게 정리해야 할 것 같습니다')
st.write('# 평균 편집 횟수 추가 필요 (+ 유저별 추가/삭제 양상도 분석해보면 좋을 것)')
# 대중문화 분야
for i in range(len(culture_list)):
    globals()[culture_list[i]+'_user'] = globals()[culture_list[i]].groupby(['uname']).count()['change']
    st.write(culture_radio[i], globals()[culture_list[i]+'_user'])

# 학문 분야
for i in range(len(academic_list)):
    globals()[academic_list[i]+'_user'] = globals()[academic_list[i]].groupby(['uname']).count()['change']
    st.write(academic_radio[i], globals()[academic_list[i]+'_user'])
    
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
st.write('# 키워드(페이지)의 수정(+, -) 글자수 리스트에 저장까지 함')
st.write('# 삭제/추가 양상 가시화 필요')
for i in range(len(culture_list)): #대중문화
  globals()[culture_list[i]+'_plus_list'] = [] # 변수명 e.g. angrybird_plus_list
  globals()[culture_list[i]+'_minus_list'] = []
  for change in globals()[culture_list[i]]['change']:
    if '+' in change:
      globals()[culture_list[i]+'_plus_list'].append(int(change[2:-1])) #괄호, 기호 제외하고 int로 변경하여 리스트에 저장
    elif '-' in change:
      globals()[culture_list[i]+'_minus_list'].append(int(change[2:-1]))

for i in range(len(academic_list)): #학문
  globals()[academic_list[i]+'_plus_list'] = []
  globals()[academic_list[i]+'_minus_list'] = []
  for change in globals()[academic_list[i]]['change']:
    if '+' in change:
      globals()[academic_list[i]+'_plus_list'].append(int(change[2:-1])) #괄호, 기호 제외하고 int로 변경하여 리스트에 저장
    elif '-' in change:
      globals()[academic_list[i]+'_minus_list'].append(int(change[2:-1]))

#예시
st.write('앵그리버드-추가 글자수 리스트', angrybird_plus_list)
st.write('앵그리버드-삭제 글자수 리스트', angrybird_minus_list)



st.markdown("*3.2. 시간에 따른 수정 양상 변화*")

# [필요하면 코드 사용하기] 키워드(페이지)별 편집 기간
# (추가) max, min 값도 제시해서 얼마나 오래되었는지, 얼마나 최근까지 수정되었는지 파악할 수 있을 것
#for i in range(len(culture_list)): #대중문화
#  st.write(globals()[culture_list[i]]['datetime'].max() - globals()[culture_list[i]]['datetime'].min())
#for i in range(len(academic_list)): #학문
#  st.write(globals()[academic_list[i]]['datetime'].max() - globals()[academic_list[i]]['datetime'].min())

st.write('키워드(페이지)별 편집 글자수 추이 (파랑: 추가/빨강색: 삭제)')
st.write('[참고] x값: 최근부터 시간순으로 부여된 인덱스, y값: 편집된 글자수')

st.pyplt.scatter(list(range(len(df1_plus_list))), df1_plus_list, color="blue", alpha=0.3)
st.pyplt.scatter(list(range(len(df1_minus_list))), df1_minus_list, color="red", alpha=0.3)
st.pyplt.figure(figsize=(60,80))
st.pyplt.show()

st.markdown("***4. 코멘트 분석***")
st.write("# '되돌림', '편집요청' 따로 분석할 필요?")
st.write('# 코멘트 키워드 분석 - 리스트 저장까지 완료 (워드클라우드 만들어야 함)')

for i in range(len(culture_list)): #대중문화
  globals()['comment_'+culture_list[i]] = globals()[culture_list[i]]['other'].values.tolist()
  globals()['comment_'+culture_list[i]] = [x for x in globals()['comment_'+culture_list[i]] if x not in '()'] # 비어 있는 열(괄호만 있는 경우) 삭제
  globals()['comment_'+culture_list[i]] = [x[1:-1] for x in globals()['comment_'+culture_list[i]]] # 앞뒤 괄호 삭제

for i in range(len(academic_list)): #학문
  globals()['comment_'+academic_list[i]] = globals()[academic_list[i]]['other'].values.tolist()
  globals()['comment_'+academic_list[i]] = [x for x in globals()['comment_'+academic_list[i]] if x not in '()'] # 비어 있는 열(괄호만 있는 경우) 삭제
  globals()['comment_'+academic_list[i]] = [x[1:-1] for x in globals()['comment_'+academic_list[i]]] # 앞뒤 괄호 삭제

#변수명 예시: st.write(comment_angrybird)

