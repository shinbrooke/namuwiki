#import settings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import altair as alt
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
st.markdown("# 문제의식")
with st.expander("문제의식 설명"):
    st.write("""**1. 나무위키의 활용**""")
    st.write("""현재 나무위키, 위키피디아와 같은 '위키'들은 우리에게 너무나도 친숙한 존재가 되었습니다. 특히, 나무위키는 한국어 중심으로 구성된 플랫폼이라는 점에서 더 가깝게 느껴지기도 합니다. 구글과 같은 서치엔진에서 검색을 할 때도, 나무위키 문서가 검색 1페이지에 등장하는 모습을 자주 확인할 수 있습니다.  2022년 12월 기준 4,763,273개 가량의 문서가 나무위키에 작성되어 있으며, 이 문서들은 실시간으로 수정되기도 하고, 새로 만들어지고 있기도 합니다.""")
    st.write("""**2. 나무위키의 신뢰성 문제**""")
    st.write("""그렇지만 동시에, 나무위키가 의견 교류 및 축적의 플랫폼이 된다는 점에서 긍정적인 **집단지성(collective intelligence)**의 사례가 될 수 있는 가능성도 지닌다고 볼 수 있습니다. 나무위키 페이지에서는 '다른 위키와의 차이점'에서 개인적인 견해를 서술하는 것이 완전히 금지되지는 않는다는 점, 각주가 출처 제시보다는 부연 설명 용도로 자주 사용된다는 점 등을 꼽고 있습니다. 또한, 누구나 위키를 활용할 수 있다는 점, 자유롭게 의견을 나눌 수 있다는 점을 기본 방침에서도 강조하고 있습니다. 이러한 나무위키의 특성은 효과적인 의견 축적을 통한 집단지성의 발현 및 집단 학습으로 이어질 가능성이 있습니다. \n
지금까지 집단지성의 개념적 모형, 집단지성을 활용한 협력학습의 가능성 등에 대한 연구는 다수 이루어졌지만, 일상적으로 사용되는 위키에서 이루어지고 있는 협력학습과 집단지성의 형성에 대한 연구는 부족해보입니다. 특히, 많은 사용자들이 활용하고 있는 나무위키의 경우, 특정 사건이나 이슈에 대한 편향된 시각을 지적하는 논문은 있었지만, 여기에서 이루어질 수 있는 학습과 공유된 의사소통 및 지식기반 형성의 과정을 탐색한 경우는 부족했습니다. 
따라서 이번 프로젝트에서는 **나무위키의 '문서 역사' 데이터**를 분석해 봄으로써 나무위키에서 어떻게 지식이 형성되고 축적되는지를 대주제별로 확인하였습니다. 이를 통해 나무위키를 통해 학습하게 되는 양상을 확인하고, 나무위키 활용의 시사점을 얻을 수 있다고 생각합니다.
""")

#2. 데이터 소개
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("# 데이터 소개")

#나무위키 대분류 3개에서 어떻게 랜덤하게 키워드를 선별해서(선별기준) history 크롤링했는지 간단히 언급 필요
#나무위키 history 페이지 캡처해서 설명하면 좋을 것 같아요! - 정빈

st.write("""데이터는 나무위키의 대분류 중 '대중문화 및 서브컬처', '학문'을 중심으로 Selenium을 활용하여 '문서 역사' 정보를 크롤링했습니다. 각 분야에서 랜덤으로 키워드 10개씩 뽑아서 먼저 분석했습니다. 그 후, 더 많은 데이터를 수집하여 전체적인 경향성을 확인했습니다. 각 분류별 뽑은 10개의 키워드와 데이터의 모습을 데이터프레임으로 정리한 것은 아래와 같습니다.""")

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

#3. 데이터 분석 1: 10개씩 페이지 대조
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("# 데이터 분석 결과 1: 10개씩 페이지 대조")

# 키워드(페이지)별로 데이터프레임 저장
for i in range(len(culture_list)):
    df_culture2 = df_culture.sort_values(['datetime'], ascending = True)
    globals()[culture_list[i]] = df_culture2[df_culture2['page'] == culture_list[i]]
for i in range(len(academic_list)):
    df_academic2 = df_academic.sort_values(['datetime'], ascending = True)
    globals()[academic_list[i]] = df_academic2[df_academic2['page'] == academic_list[i]]

st.markdown("## 1. 페이지 수정한 사용자")
st.write("먼저 페이지를 수정한 사용자가 몇 명 있는지, 사용자 각각이 몇 번의 문서 편집을 했는지를 확인했습니다.")
st.markdown("### 1.1. 페이지를 수정한 사용자의 수 (unique username 개수)")

col1_1, col1_2 = st.columns(2) #한 줄에 2개의 column을 나열함

with col1_1:
    st.markdown('***대중문화 분야***')
    for i in range(len(culture_list)):
        st.write(culture_radio[i], len(globals()[culture_list[i]].groupby('uname'))) #한글 키워드 출력
with col1_2:
    st.markdown('***학문 분야***')
    for i in range(len(academic_list)):
        st.write(academic_radio[i], len(globals()[academic_list[i]].groupby('uname'))) #한글 키워드 출력

st.markdown("""
**결과** \n
- 좀 더 많은 데이터를 살펴보아야겠지만, 대분류(대중매체/학문)에 따라 양상이 구분된다기보다는 1. 인기 있고 최신 동향이 자주 업데이트되는지(e.g. 게임, 드라마)/2. 사람마다 해석이나 의견이 달라 토론이 필요한 분야(e.g. 역사)인지에 따라 나뉘는 것으로 보입니다. \n
- 일반적인 개념을 서술하거나 이미 내용이 정립된 (내용 보충 외의 별다른 조치가 필요하지 않은/논란이 없는/더 이상 활발히 연구되고 있지 않은) 학술 용어 등은 편집자 수도, 편집 정도도 적은 것 같습니다. \n
- 편집자 수가 많은 경우, 추가되는 내용도 많기 때문에 문서의 내용도 더 충실할 경향이 있을 것으로 보입니다. 그렇지만 그만큼 몇몇 특정 사용자가 편향된 내용을 방대한 양으로 작성한다든지, 반달리즘이 일어날 위험도 큰 것 같습니다. 
""")
        
st.markdown("### 1.2. 사용자별 편집 횟수")  
st.write('cf. 이 부분도 라디오 기능을 쓰거나 좀 더 가독성 있게 정리해야 할 것 같습니다')
st.write('cf. 평균 편집 횟수 추가 필요 (+ 유저별 추가/삭제 양상도 분석해보면 좋을 것)')
# 대중문화 분야
#for i in range(len(culture_list)):
#    globals()[culture_list[i]+'_user'] = globals()[culture_list[i]].groupby(['uname']).count()['change']
#    st.write(culture_radio[i], globals()[culture_list[i]+'_user'])

# 학문 분야
#for i in range(len(academic_list)):
#    globals()[academic_list[i]+'_user'] = globals()[academic_list[i]].groupby(['uname']).count()['change']
#    st.write(academic_radio[i], globals()[academic_list[i]+'_user'])

fig1_2_1 = px.histogram(df_culture, x='uname', color="page", opacity = 0.6)
fig1_2_1.update_layout(title_text='대중문화/서브컬처 분야 사용자별 편집 횟수')
st.plotly_chart(fig1_2_1, use_container_width=True)
fig1_2_2 = px.histogram(df_academic, x='uname', color="page", opacity = 0.6)
fig1_2_2.update_layout(title_text='학문 분야 사용자별 편집 횟수')
st.plotly_chart(fig1_2_2, use_container_width=True)    

st.markdown("""
**결과** \n
- x축 영역이 넓을수록 편집에 참여한 사용자가 많고, y값이 클수록 한 사용자가 여러 번, 집중적으로 편집했다고 볼 수 있습니다. \n
- 편집자가 많을수록 다양한 사람이 편집에 고루 참여하는 것이라고 단정짓기는 어려워 보입니다. 예컨대 임진왜란 키워드를 보면 특정 몇 명이 100번 넘게 수정하고 있는 것을 확인할 수 있습니다. 보통 문서 편집이 활발하지 않을수록 편향성이 심할 것이라고 생각하기 쉬운데, 편집이 활발한 문서이더라도 특정 몇몇 편집자들의 편향이 크게 들어갈 우려가 있다고 볼 수 있을 듯합니다. \n
- 이렇게 요약해볼 수 있을 것 같습니다: 편집자 수와 편집 횟수는 어느 정도 비례하는 것으로 보입니다. 둘 다 적은 경우는 상대적으로 내용이 빈약할 수밖에 없습니다 (소수가 방대한 양을 작성할 수 있으나, 정보가 편향될 우려가 있습니다). // 반면 수정이 빈번하게 이루어지는 키워드는 내용이 상대적으로 충실해질 것이나, 편집자 수가 많아지는 만큼 특정 소수 편집자들에 의한 반달리즘에 취약하다고 볼 수 있을 것입니다 (특히 논란 있는 키워드일 경우 더욱 그러합니다). \n
""")

st.markdown("## 2. 페이지 수정 총 횟수")
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

col21, col22 = st.columns(2) #한 줄에 2개의 column을 나열함
with col21:
    fig2_1 = px.histogram(df_culture, x='page', color="page", opacity = 0.6)
    st.plotly_chart(fig2_1, use_container_width=True)
with col22:
    fig2_2 = px.histogram(df_academic, x='page', color="page", opacity = 0.6)
    st.plotly_chart(fig2_2, use_container_width=True)
   
st.markdown("""
**결과** \n
업데이트가 자주 되고, 다양한 의견을 낼 수 있는 키워드가 수정 횟수도 많고 편집에 참여하는 사람 수도 많은 것으로 보입니다. 특히 '학문' 분야에서는 '임진왜란'과 같은 한국사 관련 페이지가 다른 페이지에 비해 월등히 높은 수정 횟수를 보여주고 있습니다. 이는 '임진왜란'이 활발한 토론의 장이 되고 있음을 시사하나, 이 토론이 반달리즘에 가까울지 건설적인 지식 구성에 가까운지는 더 자세히 데이터를 살펴보아야 알 수 있을 듯합니다.
""")

st.markdown("## 3. 수정 양상")
st.write("수정이 어떻게 이루어지는지를 더 자세히 살펴보기 위해, 문서 역사의 여러 정보를 활용하여 각 페이지의 수정 양상 또한 알아보았습니다. 먼저, 삭제 및 추가된 글자의 수 및 삭제/추가된 횟수를 페이지별로 살펴보았습니다. 다음으로, 시간에 따른 수정 양상의 변화를 cumulativs sum 그래프로 나타내었습니다.")
st.markdown("### 3.1. 삭제 vs 추가 횟수")
st.write("파란색: 추가, 빨간색: 삭제")
#'cf. 키워드(페이지)의 수정(+, -) 글자수 리스트에 저장까지 함'
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

#figure 그리기
c_plist = [angrybird_plus_list, crashlandingonyou_plus_list, gameserver_plus_list, itzy_plus_list, maplephantom_plus_list, myname_plus_list, readymadelife_plus_list, skycastle_plus_list, ssglanders_plus_list, transformer_plus_list]
c_mlist = [angrybird_minus_list, crashlandingonyou_minus_list, gameserver_minus_list, itzy_minus_list, maplephantom_minus_list, myname_minus_list, readymadelife_minus_list, skycastle_minus_list, ssglanders_minus_list, transformer_minus_list]
selected_item1 = st.radio("대중문화/서브컬처 추가 vs 삭제", culture_list)	

for i in range(len(culture_list)):
    if selected_item1 == culture_list[i]:
        st.write("추가: {}번, 삭제: {}번".format(len(c_plist[i]),len(c_mlist[i])))

a_plist = [aesthetic_plus_list, call_plus_list, epidemic_plus_list, greekromanmyth_plus_list, hungarianrevolution_plus_list, imjin_plus_list, montyhall_plus_list, officiallanguage_plus_list, pascaltriangle_plus_list, spotlight_plus_list]
a_mlist = [aesthetic_minus_list, call_minus_list, epidemic_minus_list, greekromanmyth_minus_list, hungarianrevolution_minus_list, imjin_minus_list, montyhall_minus_list, officiallanguage_minus_list, pascaltriangle_minus_list, spotlight_minus_list]
selected_item2 = st.radio("학문 추가 vs 삭제", academic_list)	

for i in range(len(academic_list)):
    if selected_item2 == academic_list[i]:
        st.write("추가: {}번, 삭제: {}번".format(len(a_plist[i]),len(a_mlist[i])))
        
        
st.markdown("### 3.2. 시간에 따른 수정 양상 변화")

# [필요하면 코드 사용하기] 키워드(페이지)별 편집 기간
# (추가) max, min 값도 제시해서 얼마나 오래되었는지, 얼마나 최근까지 수정되었는지 파악할 수 있을 것
#for i in range(len(culture_list)): #대중문화
#  st.write(globals()[culture_list[i]]['datetime'].max() - globals()[culture_list[i]]['datetime'].min())
#for i in range(len(academic_list)): #학문
#  st.write(globals()[academic_list[i]]['datetime'].max() - globals()[academic_list[i]]['datetime'].min())

st.markdown("***키워드(페이지)별 편집 글자수 추이 (파랑: 추가/빨강색: 삭제)***")
with st.expander("참고"):
    st.write("파란색: 추가, 빨간색: 삭제")
    st.write('x값: 최근부터 시간순으로 부여된 인덱스, y값: 편집된 글자수')
st.markdown("*대중문화/서브컬처 편집 글자수 추이*")
selected_item3 = st.radio("대중문화/서브컬처 수정 양상", culture_list)	

for i in range(len(culture_list)):
    if selected_item3 == culture_list[i]:
        figc, x = plt.subplots()
        x.scatter(list(range(len(c_plist[i]))), c_plist[i], color="blue", alpha=0.3)
        x.scatter(list(range(len(c_mlist[i]))), c_mlist[i], color="red", alpha=0.3)
        #pltc.figure(figsize=(60,80))
        st.pyplot(figc)

st.markdown("*학문 편집 글자수 추이*")
selected_item4 = st.radio("학문 수정 양상", academic_list)	

for i in range(len(academic_list)):
    if selected_item4 == academic_list[i]:
        figa, x = plt.subplots()
        x.scatter(list(range(len(a_plist[i]))), a_plist[i], color="blue", alpha=0.3)
        x.scatter(list(range(len(a_mlist[i]))), a_mlist[i], color="red", alpha=0.3)
        #plta.figure(figsize=(60,80))
        st.pyplot(figa)
        
st.markdown("***페이지별 수정 양상 추이***")
st.write("변화한 글자수의 cumulative sum이 페이지별로 시간에 따라 어떻게 변화했는지를 확인한 그래프입니다.")
# change column 숫자로 변환
df_culture['change2'] = df_culture['change'].map(lambda x: x.lstrip('(').rstrip(')'))
df_culture['change2'] = df_culture.change2.apply(lambda x: float(x))
df_culture = df_culture.sort_values(['datetime'], ascending = True)
df_culture['cumsum'] = df_culture.groupby('page')['change2'].transform(pd.Series.cumsum)
#페이지별 편집 양상 line graph
st.write("*대중문화/서브컬처, 페이지별 수정 양상 추이*")
basic_chart1 = alt.Chart(df_culture).mark_line().encode(
    x='datetime',
    y='cumsum',
    color='page',
)
st.altair_chart(basic_chart1, use_container_width=True)

# change column 숫자로 변환 (학문)
df_academic['change2'] = df_academic['change'].map(lambda x: x.lstrip('(').rstrip(')'))
df_academic['change2'] = df_academic.change2.apply(lambda x: float(x))
df_academic = df_academic.sort_values(['datetime'], ascending = True)
df_academic['cumsum'] = df_academic.groupby('page')['change2'].transform(pd.Series.cumsum)
#페이지별 편집 양상 line graph
st.write("*학문, 페이지별 수정 양상 추이*")
basic_chart2 = alt.Chart(df_academic).mark_line().encode(
    x='datetime',
    y='cumsum',
    color='page',
)
st.altair_chart(basic_chart2, use_container_width=True)

st.markdown("""
**결과**\n
- 키워드(페이지)별 시기에 따른 수정 양상 추이로, 추가/삭제된 글자수의 총합(즉, 당시 문서의 총 글자수)을 파악할 수 있는 그래프입니다. 각각의 페이지는 다른 색상으로 표현되어 있습니다.\n
- 기울기가 수평에 가까울수록 거의 문서가 수정되지 않았다(글자수가 변화하지 않았다)고 해석할 수 있습니다. (e.g. 게임서버의 경우 문서의 큰 변화가 없는 것으로 보입니다.)\n
- y=0에 가까울수록 문서 글자수가 적으므로, 문서 내용이 충실하지 못하다고도 해석할 수 있을 것 같습니다. (키워드가 지엽적이라서 설명할 내용 자체가 상대적으로 적을 수도 있고, 글자수가 많다고 충실한 문서라 해석할 순 없겠지만, 글자수 또한 문서 내용의 질에 기여하는 한 가지 지표이므로, 이러한 해석을 해볼 수 있습니다.)\n
- 수직으로 선이 그어지는 경우, 그리고 이런 수직선이 많이 보이는 경우, 급속한 문서의 변화가 지속되는 것으로 반달리즘 등을 의심해 볼 수 있습니다.\n
- 어느 정도 지점이 되면 기울기가 완만해지는 모습을 보일 때, 충실하고 질이 높은 문서라고 볼 수 있습니다. 문서 내용이 축적되고, 어느 정도 합의에 이르렀다는 것을 의미하기 때문입니다.
""")

st.markdown("### 3.3. 코멘트 분석")
st.write("cf. '되돌림', '편집요청' 따로 분석할 필요?")
st.write('cf. 코멘트 키워드 분석 - 리스트 저장까지 완료 (워드클라우드 만들어야 함)')

for i in range(len(culture_list)): #대중문화
  globals()['comment_'+culture_list[i]] = globals()[culture_list[i]]['other'].values.tolist()
  globals()['comment_'+culture_list[i]] = [x for x in globals()['comment_'+culture_list[i]] if x not in '()'] # 비어 있는 열(괄호만 있는 경우) 삭제
  globals()['comment_'+culture_list[i]] = [x[1:-1] for x in globals()['comment_'+culture_list[i]]] # 앞뒤 괄호 삭제

for i in range(len(academic_list)): #학문
  globals()['comment_'+academic_list[i]] = globals()[academic_list[i]]['other'].values.tolist()
  globals()['comment_'+academic_list[i]] = [x for x in globals()['comment_'+academic_list[i]] if x not in '()'] # 비어 있는 열(괄호만 있는 경우) 삭제
  globals()['comment_'+academic_list[i]] = [x[1:-1] for x in globals()['comment_'+academic_list[i]]] # 앞뒤 괄호 삭제

#변수명 예시: st.write(comment_angrybird)



#4. 데이터 분석 결과 2
st.markdown("<hr>", unsafe_allow_html=True)
st.write('# 데이터 분석 결과 2: 학문 분야 500개, 대중문화 분야 397개 데이터 비교')

df_culture_aug0 = load_data('dataculture_aug.csv')
df_academic_aug0 = load_data('dataacademic_aug_mod.csv')

df_culture_aug = df_culture_aug0.copy()
df_academic_aug df_academic_aug0.copy()

# 편집 텀
st.write('## 1. 편집 텀')
def get_edit_counts(df):
  edit_counts = df['page'].value_counts(sort=False)
  return list(edit_counts)

def get_date_diffs(df):
  all_pages = df['page'].unique()
  date_diffs = []
  strptime_format = '%Y-%m-%d %H:%M:%S'

  for page in all_pages:
    diff = datetime.strptime(df[df['page'] == page]['time'].iloc[0], strptime_format) - datetime.strptime(df[df['page'] == page]['time'].iloc[-1], strptime_format)
    date_diffs.append(diff)

  return date_diffs

def get_mean_edit_terms(df):
  date_diffs = get_date_diffs(df)
  date_diffs = [diff.days + diff.seconds/(3600*24) for diff in date_diffs]
  edit_counts = get_edit_counts(df)
  edit_terms = [diff / count for diff, count in zip(date_diffs, edit_counts)]

  return edit_terms

def plot_edit_terms(df, bin_interval=10, maxbin=500, isrel=True, target='edit_terms'):
  fig = plt.figure(figsize=(10, 10))
  if target == 'edit_terms':
    data = get_mean_edit_terms(df)
  bins = np.arange(0, maxbin, bin_interval)
  hist, _ = np.histogram(data, bins)
  if isrel:
    hist = np.asarray(hist) / len(data)
  # plt.hist(data, bins=bins)
  plt.plot(bins[:-1], hist)
  # plt.legend()
  
  plt.show()

def plot_edit_terms(dfs, labels, bin_interval=10, maxbin=500, isrel=True, target='edit_terms'):
  fig = plt.figure(figsize=(10, 10))
  plotdict = {}
  if target == 'edit_terms':
    for i, df in enumerate(dfs):
      plotdict[f'data{i}'] = get_mean_edit_terms(df)

  bins = np.arange(0, maxbin, bin_interval)


  for i in range(len(dfs)):
    plotdict[f'hist{i}'], _ = np.histogram(plotdict[f'data{i}'], bins)

  if isrel:
    for i in range(len(dfs)):
      plotdict[f'hist{i}'] = np.asarray(plotdict[f'hist{i}']) / len(plotdict[f'data{i}'])

  for i in range(len(dfs)):
    plt.plot(bins[:-1], plotdict[f'hist{i}'], label=labels[i])
  
  plt.xlabel('Mean days for an edit')
  plt.ylabel('Relative frequency')
  plt.legend()
  
  plt.show()
  st.pyplot(fig)

plot_edit_terms([df_academic_aug, df_culture_aug], ['academic', 'culture'], bin_interval=10)


# 추이
st.write('## 2. 편집 추이')
def get_rel_change_means(df, length=100, fromr1=True):
  df['len'] = df.groupby('page')['page'].transform('count')
  df_mod = df[df['len'] >= 100]

  change_lists = get_change_lists(df_mod, length, fromr1)
  change_lists_cumsum = get_change_lists_cumsum(change_lists)
  rel_change_lists = get_rel_change_lists(change_lists_cumsum)

  rel_change_means = [sum(x)/len(x)-1 for x in zip(*rel_change_lists)]
  return rel_change_means

def get_change_lists(df, length, fromr1=True):
  df_mod = df[df['len'] >= length]

  change_lists = []
  if fromr1:
    for item in df_mod.page.unique():
      change_list = list(df[df['page'] == item]['change'].iloc[-length:]) # r{length} ~ r1
      change_lists.append(change_list)
  else:
    for item in df_mod.page.unique():
      change_list = list(df[df['page'] == item]['change'].iloc[:length]) # r_latest ~ r{length}
      change_lists.append(change_list)
  
  change_lists = [list(reversed(change_list)) for change_list in change_lists]
  return change_lists

def get_change_lists_cumsum(change_lists):
  change_lists_cumsum = [np.cumsum(change_list) for change_list in change_lists]
  return change_lists_cumsum

def get_rel_change_lists(change_lists_cumsum):
  rel_change_lists = []

  for change_list in change_lists_cumsum:
    rel_change_list = []
    for i in range(len(change_list)):
      if i==0:
        rel_change_list.append(1)
      try:
        if change_list[i]:
          rel = change_list[i+1] / change_list[i]
          rel_change_list.append(rel)
        else:
          rel_change_list.append(1)
      except IndexError:
        pass

    rel_change_list = remove_outliers(rel_change_list)
    rel_change_lists.append(rel_change_list)

  return rel_change_lists

def remove_outliers(data):
  iqr = stats.iqr(data, axis=0)
  lowerbound = np.quantile(data, 0.25)-1.5*iqr
  upperbound = np.quantile(data, 0.75)+1.5*iqr
  normals = [x if x >= lowerbound else lowerbound for x in data]
  normals = [x if x <= upperbound else upperbound for x in data]
  return normals

def plot_history(dfs, labels, length=100, fromr1=True):
  fig = plt.figure(figsize=(20, 10))
  plotdict = {}

  for i, df in enumerate(dfs):
    plotdict[f'means{i}'] = get_rel_change_means(df, length, fromr1)
    x = range(1, len(plotdict[f'means{i}'])+1)
    y = plotdict[f'means{i}']
    plt.plot(x, y, label=labels[i])

  # plt.plot(range(1, length+1), [0]*length, c='red')

  plt.xlabel('Revision(step)')
  plt.ylabel('Trend')
  plt.legend()
  
  plt.show()
  st.pyplot(fig)

plot_history([df_academic_aug, df_culture_aug], labels=['academic', 'culture'], length=100, fromr1=True)

# wordcloud
st.write('## 3. 코멘트 텍스트 분석: Wordcloud')

# df에서 comments를 얻는 함수
def get_comments(df):
  comments = list(df[df['other'].isna() == False]['other'])

  comments = [comment for comment in comments if re.match(r'[가-힣ㄱ-ㅎ]', comment)]
  comments = [comment for comment in comments if not re.match(r'봇|자동 편집|자동 병합', comment)]
  comments = [re.sub(r'[^가-힣ㄱ-ㅎ]+http[^가-힣ㄱ-ㅎ]+|[^가-힣ㄱ-ㅎ]+www\.[^가-힣ㄱ-ㅎ]+|[^가-힣ㄱ-ㅎ]+\.com[^가-힣ㄱ-ㅎ]+|[^가-힣ㄱ-ㅎ]+\.net[^가-힣ㄱ-ㅎ]+|[^가-힣ㄱ-ㅎ]+\.org[^가-힣ㄱ-ㅎ]+|[^가-힣ㄱ-ㅎ]+\.kr[^가-힣ㄱ-ㅎ]+', '[LINK]', comment) for comment in comments]
  comments = [comment for comment in comments if comment]

  return comments

# comments의 각 comment에 pos를 태깅하는 함수
def get_tagged_comments(comments):
  tagger = Komoran()
  tagged_comments = [tagger.pos(comment) for comment in comments]
  return tagged_comments

# df로부터 lexical words를 얻는 함수
def get_lexical_words(df):
  comments = get_comments(df)
  tagged_comments = get_tagged_comments(comments)

  lexical_words = []
  for tagged_comment in tagged_comments:
    for word, pos in tagged_comment:
      if pos != 'SL' and pos in ['NNP', 'NNG', 'VV', 'VA']:
        lexical_words.append(word)

  return lexical_words

# words로부터 words의 Counter를 얻는 함수
def get_lexical_words_count(words):
  words_count = Counter(words)
  return words_count

# df로부터 wordcloud 그리는 함수
def show_wordcloud(df):
  words = get_lexical_words(df)# words 얻기
  words_count = get_lexical_words_count(words) # words의 빈도수 얻기
  
  ## wordcloud 객체 설정
  cloud = WordCloud(width=1000,
                  height=800, 
                  font_path='08서울남산체B.ttf',
                  background_color='white')

  cloud = cloud.fit_words(words_count)

  ## wordcloud 그리기
  fig = plt.figure(figsize=(15, 20))
  plt.axis('off')
  plt.imshow(cloud)
  plt.show()
  st.pyplot(fig)


show_wordcloud(df_academic_aug)
show_wordcloud(df_culture_aug)

