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

from konlpy.tag import Komoran
from wordcloud import WordCloud
from collections import Counter
import string
import re
from scipy import stats

#data loading
# st.cache를 이용하여 데이터 로딩을 하는 함수
@st.cache #데이터를 불러와서 메모리에 가지고 있는 것 (매번 불러오기 번거롭기 때문)
def load_data(filename):
    data = pd.read_csv(filename)
    return data

#df0 = load_data("")
df_culture0 = load_data('dataculture.csv')
df_academic0 = load_data('dataacademic.csv')

df_culture = df_culture0.copy()
df_academic = df_academic0.copy()

# 3개의 csv 파일에 대해 date, time 칼럼 합치고 데이터타입 datetime으로 변경
df_culture['datetime'] = df_culture['date'] + " " + df_culture['time']
df_culture = df_culture.drop(['date', 'time'], axis=1)
df_culture['datetime'] = pd.to_datetime(df_culture['datetime'])

df_academic['datetime'] = df_academic['date'] + " " + df_academic['time']
df_academic = df_academic.drop(['date', 'time'], axis=1)
df_academic['datetime'] = pd.to_datetime(df_academic['datetime'])

#title styling
def title(text):
     st.markdown(f'<h2 style="background-color:#64a88d;color:#ffffff;padding:20px;border-radius:14px;">{text}</h2>', unsafe_allow_html=True)
def result(text):
    st.markdown(f'<div style="background-color:#ebf2ee;padding:20px;border-radius:14px;">{text}</div>', unsafe_allow_html=True)

st.subheader("2022-2 데이터 저널리즘 과제전")
st.title("나무위키 활용 학습의 가능성과 한계")
st.write("10조: 서정빈, 신부경, 정민제")

#1. 문제의식 서술
st.markdown("<hr>", unsafe_allow_html=True)
title("문제의식")
with st.expander("문제의식 설명"):
    st.markdown("""**1. 나무위키의 활용**""")
    st.markdown("""현재 나무위키, 위키피디아와 같은 '위키'들은 우리에게 너무나도 친숙한 존재가 되었습니다. 특히, 나무위키는 한국어 중심으로 구성된 플랫폼이라는 점에서 더 가깝게 느껴지기도 합니다. 구글과 같은 서치엔진에서 검색을 할 때도, 나무위키 문서가 검색 1페이지에 등장하는 모습을 자주 확인할 수 있습니다.  2022년 12월 기준 4,763,273개 가량의 문서가 나무위키에 작성되어 있으며, 이 문서들은 실시간으로 수정되기도 하고, 새로 만들어지고 있기도 합니다.""")
    st.markdown("""**2. 나무위키의 신뢰성 문제**""")
    st.markdown("""우리가 이렇게 일상적으로 사용하는 나무위키는 의도적으로든, 비의도적으로든 학습의 장이 되기도 합니다. 위키는 모르는 정보를 검색할 때, 인터넷 서핑을 하다가 새로운 정보가 눈에 띄었을 때 등 우발적이고 무의식적으로 학습이 쉽게 일어날 수 있는 장입니다. 그러나 누구나 글을 작성하고 수정할 수 있기 때문에, 신뢰성 측면에서 비판을 받기도 합니다. 믿을 수 없는 정보, 편향된 정보가 작성될 가능성이 높기 때문입니다. 실제로 나무위키 내에서도 '나무위키/비판 및 문제점'이라는 페이지에 이러한 측면이 서술될 만큼, 편향과 주관적 의견 서술의 측면이 문제시되고 있기도 합니다.""")
    st.markdown("""**3. 나무위키의 가능성과 한계**""")
    st.markdown("""그렇지만 동시에, 나무위키가 의견 교류 및 축적의 플랫폼이 된다는 점에서 긍정적인 **집단지성(collective intelligence)**의 사례가 될 수 있는 가능성도 지닌다고 볼 수 있습니다. 나무위키 페이지에서는 '다른 위키와의 차이점'에서 개인적인 견해를 서술하는 것이 완전히 금지되지는 않는다는 점, 각주가 출처 제시보다는 부연 설명 용도로 자주 사용된다는 점 등을 꼽고 있습니다. 또한, 누구나 위키를 활용할 수 있다는 점, 자유롭게 의견을 나눌 수 있다는 점을 기본 방침에서도 강조하고 있습니다. 이러한 나무위키의 특성은 효과적인 의견 축적을 통한 집단지성의 발현 및 집단 학습으로 이어질 가능성이 있습니다.""")
    st.markdown("""지금까지 집단지성의 개념적 모형, 집단지성을 활용한 협력학습의 가능성 등에 대한 연구는 다수 이루어졌지만, 일상적으로 사용되는 위키에서 이루어지고 있는 협력학습과 집단지성의 형성에 대한 연구는 부족해보입니다. 특히, 많은 사용자들이 활용하고 있는 나무위키의 경우, 특정 사건이나 이슈에 대한 편향된 시각을 지적하는 논문은 있었지만, 여기에서 이루어질 수 있는 학습과 공유된 의사소통 및 지식기반 형성의 과정을 탐색한 경우는 부족했습니다. 
따라서 이번 프로젝트에서는 **나무위키의 '문서 역사' 데이터**를 분석해 봄으로써 나무위키에서 어떻게 지식이 형성되고 축적되는지를 대주제별로 확인하였습니다. 이를 통해 나무위키를 통해 학습하게 되는 양상을 확인하고, 나무위키 활용의 시사점을 얻을 수 있다고 생각합니다.
""")
    st.markdown("""**핵심 질문: 나무위키에서 어떻게, 어떠한 집단지성이 구성될까?**""")
    st.markdown("""참고문헌\n
    이유나, 이상수. (2009). 집단지성의 교육적 적용을 위한 개념모형과 설계 원리. 교육공학연구, 25(4), 213-239.\n
    Das, S., & Magdon-Ismail, M. (2010, June). Collective wisdom: Information growth in wikis and blogs. In Proceedings of the 11th ACM conference on Electronic commerce (pp. 231-240).\n
    Hu, M., Lim, E. P., Sun, A., Lauw, H. W., & Vuong, B. Q. (2007, November). Measuring article quality in wikipedia: models and evaluation. In Proceedings of the sixteenth ACM conference on Conference on information and knowledge management (pp. 243-252).\n
    Joo, J., & Normatov, I. (2013). Determinants of collective intelligence quality: comparison between Wiki and Q&A services in English and Korean users. Service Business, 7(4), 687-711.""")

with st.expander("이론적 배경: 집단지성"):
    st.markdown("**집단지성의 개념**")
    st.markdown("""
    집단지성(collective intelligence)은 여러 사람들이 공동의 관심사나 목적을 바탕으로 형성된 지식 또는 능력을 의미하며, 개인의 합 이상의 결과물임을 함축하는 표현입니다.
    집단지성을 과정적 측면에서 서술하는 경우에는 '어디에나 분포하며, 지속적으로 가치 부여되고, 실시간으로 조정되며, 역량의 실제적 동원에 이르는 지성'(Levy, 1994)이라 표현하기도 합니다.
    또한 집단지성을 공유된 지적 결과 자체를 드러내는 표현으로 활용하기도 합니다. 이유나와 이상수(2009)는 여러 연구에서 드러나는 집단지성의 공통적 특성을 다음과 같이 여섯 가지로 정리하고 있습니다:
    \n
    1. 네트워크화된 테크놀로지를 통해 상호연결되어 있다.
    2. 분산된 인지 자원들을 공유한다.
    3. 각 개인들 간 협력과 참여를 통해 역동적인 상호작용이 일어난다.
    4. 공유된 마음이나 비전을 갖고 있다.
    5. 구성원들에 의해 생성된 맥락 내에서 하나의 살아있는 유기체처럼 움직인다.
    6. 분산된 인지의 합 이상의 긍정적 시너지를 발휘한다.
    \n
    이들은 집단지성의 교육적 적용을 위한 개념모형 또한 제시하고 있는데, 이 개념 모형의 여섯 가지 요인은 다음과 같습니다. \n
    1. **공유된 멘탈 모델**: 집단의 정체성이자 공유된 목적성, 방향성을 의미합니다.
    2. **협력지성**: 저자들은 이를 '집단작동기억'의 한 요소라고 설명하는데, 집단 내 개인들이 정보를 공유하고 협력을 할 수 있는 능력입니다.
    3. **사회적 네트워킹**: 이것 또한 '집단작동기억'의 한 요소로, 개인들 간 연결이 얼마나 활발하게, 다채롭게 형성되어 있는지를 의미합니다.
    4. **다양성**: 집단을 구성하는 개인들이 얼마나 다양한지를 말합니다. 다양한 경험과 지식을 갖춘 개인들이 모일 때, 더 창의적인 결과물이 나올 수 있습니다.
    5. **집단(장기)기억체제**: 여러 개인들의 활동을 통해 형성된 정보와 결과물, 즉 지식이 저장될 수 있는 방법입니다.
    6. **통합수행**: 통합수행은 집단지성의 과정을 통해, 즉 여러 사람이 지식을 형성해 나가는 과정을 통해 만들어진 결과물을 의미합니다.
    \n이유나, 이상수(2009)는 다양한 구성원들이 사회적 네트워킹을 바탕으로 협력지성을 발휘하면서, 집단기억체제에 지식을 저장한다고 봅니다. 
    이때 집단기억체제에 이미 있는 지식을 적극 활용하기도 합니다. 이러한 일련의 과정을 통해 공유된 멘탈모델이 형성되며, 결과적으로 통합수행이 나타나게 된다고 합니다. 
    이와 같은 과정이 곧 집단지성이 형성되는 과정이라 볼 수 있습니다. 저희는 이론적 모형을 기반으로 나무위키에서는 어떤 과정을 통해 집단지성이 구성되는지를 확인해 보았습니다.
    \n
    """)
    st.markdown("**집단지성의 질**")
    st.markdown("""
    질 높은 집단지성이 형성되는 과정에서, 점점 많은 사용자들이 참여하게 되면서 추가의 방향으로 수정이 이루어지고, 그러다가 점차 합의에 이르면서 수정이 줄어들고 문서가 안정화된다고 합니다(Das & Magdon-Ismail, 2010). 
    또한, 많은 사용자들이 문서 편집에 참여할 때 더 신뢰할 수 있는 집단지성이 형성될 가능성이 높습니다(Joo & Normatov, 2013). 
    더 다양한 참여자들이 함께 협력지성을 발휘할 수 있는 상황이 만들어지기 때문입니다. 
    따라서, 나무위키에서 높은 질의 집단지성이 만들어지고 있는지 확인하기 위해, 각 페이지에 몇 명이 편집에 참여하고 있는지, 
    (전체적으로 그리고 참여자별로) 얼만큼씩 어떻게 수정을 하고 있는지, 수정 양상이 시간에 따라 어떻게 변하는지를 확인할 필요가 있어 보입니다.
    """)
    
#2. 데이터 소개
st.markdown("<hr>", unsafe_allow_html=True)
title("데이터 소개")
st.write("먼저, 나무위키의 데이터 형태와 이번 프로젝트에서 데이터를 수집한 방식, 데이터 양상을 소개해보겠습니다.")
st.markdown('## 나무위키 소개')
col0_1, col0_2 = st.columns(2)
with col0_1:
    st.write("""나무위키는 2015년에 만들어진 위키입니다. 나무위키 문서들은 표제어를 중심으로 구성되며, 누구나 계정을 만들면 편집할 수 있습니다. 특히, 다른 위키들에 비해 개인의 의견 서술이 비교적 자유로운 편이며, 토론 기능을 통해 의견을 교류하고 합의에 도달할 수도 있습니다.
    나무위키 표제어별로 문서 한 페이지가 만들어지고, 그 문서에 대해 수정과 편집의 역사를 확인할 수 있는 '문서 역사' 페이지도 제공됩니다.""")
    
with col0_2:
    from PIL import Image
    image = Image.open('data_namuwiki.png')
    st.image(image, caption='나무위키 문서역사 화면 예시 (표제어: "데이터")')

st.markdown('''
> "나무위키는 2015년 4월 17일에 설립된, 이용자의 자유와 권리를 평등하게 보장하고 지식과 정보의 공유에 힘쓰기 위해 개설된 위키이다. 위키 사이트로서 나무위키는 특정 영역에 편중되지 않은, 학문·서브컬처 등 다양한 분야를 포용하여 진흥시키는 것을 목표로 하며, 경직되고 건조한 서술이 아닌 어느 정도 재미도 갖춘 서술을 지향한다. 나무위키는 토론을 통해 중립적이고 사실적인 서술과, 특정한 관점·세력에 종속되지 않는 서술을 지향하며, 보편적인 인권과 윤리에 어긋나는 사상과 집단을 배격한다."\n 
- 나무위키 기본 방침 중
''')
    
st.markdown("## 데이터 분석 방법")
st.markdown("**데이터 수집**")
st.markdown("""
저희 프로젝트에서는 문서 역사 데이터를 수집하여, 나무위키에서 지식이 축적되는 양상을 확인해보아, 이것이 학습에 용이할 수 있는지 탐구했습니다. 
나무위키에서는 '주요 키워드'를 정리하여 전체적인 문서들의 분류를 제시하고 있습니다. 
저희는 특히 내용적으로 대조될 수 있는 '대중문화 및 서브컬처'라는 대분류와, '학문'이라는 대분류에 초점을 두어 데이터를 수집했습니다. 
또한, 먼저 각 대분류별로 랜덤으로 10개씩 페이지를 추출하여 자세히 분석하고, 전체적인 경향성을 파악하기 위해 각 대분류별로 더 많은 데이터를 수집하여 추가적으로 분석해보았습니다.
""")
st.markdown("**데이터 분석**")
st.markdown("""
기존 선행연구에 기초하여, 다음과 같은 측면을 중점적으로 분석했습니다. \n
1. 각 페이지의 편집에 참여한 사용자의 수 및 사용자별 편집 횟수 (얼마나 다양한 참여자들이, 얼마나 활발하게 참여하는지)
2. 각 페이지별 편집 총 횟수 (전체적으로 논의가 얼마나 활발히 일어나는지)
3. 페이지별 수정의 양상: 추가와 삭제의 양상 및 시간에 따른 수정의 추이 (문서가 안정화되는지 확인)
\n이러한 데이터를 바탕으로, 나무위키에서 집단지성이 어떻게 구성되는지를 확인하고 이에 의거하여 나무위키 활용 학습에 대한 시사점을 도출해 보았습니다. 
""")
    
st.markdown('## 데이터 1')

st.write("""
데이터는 나무위키의 대분류 중 '대중문화 및 서브컬처', '학문'을 중심으로 Selenium을 활용하여 '문서 역사' 정보를 크롤링했습니다. 
각 분야에서 랜덤으로 키워드 10개씩 뽑아서 먼저 분석했습니다. 그 후, 더 많은 데이터를 수집하여 전체적인 경향성을 확인했습니다. 
각 분류별 뽑은 10개의 키워드와 데이터의 모습을 데이터프레임으로 정리한 것은 아래와 같습니다.""")

# 대분류별 키워드 리스트
culture_list = ['angrybird', 'crashlandingonyou', 'gameserver', 'itzy', 'maplephantom', 'myname', 'readymadelife', 'skycastle', 'ssglanders', 'transformer']
academic_list = ['aesthetic', 'call', 'epidemic', 'greekromanmyth', 'hungarianrevolution', 'imjin', 'montyhall', 'officiallanguage', 'pascaltriangle', 'spotlight']
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

#전체 데이터
with st.expander("대중문화 및 서브컬처"):
    st.write("대중문화 및 서브컬처 분야 키워드: '앵그리버드 시리즈', '사랑의 불시착', '게임 서버', 'ITZY', '팬텀(메이플스토리)', '마이 네임', '레디메이드 인생', 'SKY 캐슬', 'SSG 랜더스/2021년/5월', '트랜스포머: 사라진 시대'")
    st.write(df_culture)

#라디오
culture_radio = ['앵그리버드 시리즈', '사랑의 불시착', '게임 서버', 'ITZY', '팬텀(메이플스토리)', '마이 네임', '레디메이드 인생', 'SKY 캐슬', 'SSG 랜더스/2021년/5월', '트랜스포머: 사라진 시대']
#culture_status = st.radio('대중문화 및 서브컬처 분야', culture_radio)

#for i in range(len(culture_radio)):
#    if culture_status == culture_radio[i]:
#        st.write(df_culture[df_culture['page'] == culture_list[i]])

#전체 데이터
with st.expander("학문"):
    st.write("학문 분야 키워드: '미학', '통화', '전염병', '그리스 로마 신화', '1956년 헝가리 혁명', '임진왜란', '몬티 홀 문제', '공용어', '파스칼의 삼각형', '조명 효과'")
    st.write(df_academic)

#라디오
academic_radio = ['미학', '통화', '전염병', '그리스 로마 신화', '1956년 헝가리 혁명', '임진왜란', '몬티 홀 문제', '공용어', '파스칼의 삼각형', '조명 효과']
#acadamic_status = st.radio('학문 분야', academic_radio)

# 위 코드랑 똑같은데 학문 분야도 라디오 기능 쓰려니까 오류 나네요.. 일단 각주처리해놓겠습니다!
#for i in range(len(academic_radio)):
#    if acadamic_status == acadamic_radio[i]:
#        st.write(df_acadamic[df_acadamic['page'] == acadamic_list[i]])

with st.expander("칼럼명 소개"):
    st.write('이번 데이터 분석에 쓰인 데이터의 변수(칼럼)명은 다음과 같습니다.')
    st.markdown('''
    - code: 일련 번호 (숫자가 클수록 최신)
    - change: 수정 양상 (+: 글자수 추가, -: 글자수 삭제)
    - uname: 편집자 닉네임/아이피
    - other: 편집자 코멘트
    - page: 페이지 키워드 (영어로 표기)
    - category: 대분류(대중문화 및 서브컬처/학문)
    - datetime: 수정 날짜 및 시간
    ''')

st.markdown('## 데이터 2')
st.write('''조금 더 큰 규모의 데이터를 모으기 위해 2차적으로 데이터를 수집했습니다. 수집 방식과 데이터 구성은 기본적으로 데이터 1을 수집할 때와 유사하게 진행했습니다.
\n우선 학문 분야에서는 분류:수학 용어, 분류:물리학, 분류:생물학에 속하는 모든 문서의 역사를 크롤링했습니다.
\n대중문화 분야에서는 우선 영화와 드라마 문서를 수집하기 위해 "분류:2016년 영화"부터 "분류:2019년 영화"의 모든 문서와, "분류:넷플릭스 오리지널 드라마" 문서를 모두 수집한 뒤 랜덤으로 45개를 뽑았습니다. 
다음으로 스포츠 관련 문서도 대중문화에 포함하기 위해 "분류:축구 용어"와 "분류:야구 용어"의 모든 문서를 크롤링했습니다. 
또 아이돌 관련 문서를 크롤링하기 위해 "걸그룹/목록" 문서에서 2011년 ~ 2016년까지의 걸그룹과 "보이그룹/목록" 문서에서 역시 같은 연도의 보이그룹 문서를 크롤링했습니다. 
\n수집된 학문 분야 문서의 수가 대중문화 분야 문서 수의 2배가 넘었기에 학문 분야 문서는 랜덤으로 500개만 사용했습니다. 대중문화 분야 문서는 총 379개를 사용했습니다.''')

#3. 데이터 분석 1: 10개씩 페이지 대조
st.markdown("<hr>", unsafe_allow_html=True)
title("데이터 분석 결과 1: 페이지 10개씩")

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
    culture_u_list = []
    for i in range(len(culture_list)):
        df_temp = df_culture[df_culture['page'] == culture_list[i]]
        val_count = df_temp['uname'].nunique()
        page = culture_list[i]
        culture_u_list.append([page, val_count])
    culture_u = pd.DataFrame(culture_u_list, columns = ['page', 'count'])
    fig1 = plt.figure(figsize=(10,5))
    sb.barplot(data=culture_u, x='page', y='count',alpha=0.8)
    plt.xticks(rotation=90)
    st.pyplot(fig1)
    for i in range(len(culture_list)):
        st.write(culture_radio[i], len(globals()[culture_list[i]].groupby('uname'))) #한글 키워드 출력

with col1_2:
    st.markdown('***학문 분야***')
    academic_u_list = []
    for i in range(len(academic_list)):
        df_temp2 = df_academic[df_academic['page'] == academic_list[i]]
        val_count = df_temp2['uname'].nunique()
        page = academic_list[i]
        academic_u_list.append([page, val_count])
    academic_u = pd.DataFrame(academic_u_list, columns = ['page', 'count'])
    fig2 = plt.figure(figsize=(10,5))
    sb.barplot(data=academic_u, x='page', y='count',alpha=0.8)
    plt.xticks(rotation=90)
    st.pyplot(fig2)
    for i in range(len(academic_list)):
        st.write(academic_radio[i], len(globals()[academic_list[i]].groupby('uname'))) #한글 키워드 출력

result("""
<b>결과</b>

- 좀 더 많은 데이터를 살펴보아야겠지만, 대분류(대중매체/학문)에 따라 양상이 구분된다기보다는 1. 인기 있고 최신 동향이 자주 업데이트되는지(e.g. 게임, 드라마)/2. 사람마다 해석이나 의견이 달라 토론이 필요한 분야(e.g. 역사)인지에 따라 나뉘는 것으로 보입니다.
- 일반적인 개념을 서술하거나 이미 내용이 정립된 (내용 보충 외의 별다른 조치가 필요하지 않은/논란이 없는/더 이상 활발히 연구되고 있지 않은) 학술 용어 등은 편집자 수도, 편집 정도도 적은 것 같습니다.
- 편집자 수가 많은 경우, 추가되는 내용도 많기 때문에 문서의 내용도 더 충실할 경향이 있을 것으로 보입니다. 그렇지만 그만큼 몇몇 특정 사용자가 편향된 내용을 방대한 양으로 작성한다든지, 반달리즘이 일어날 위험도 큰 것 같습니다. 
""")
st.write(" ")
        
st.markdown("### 1.2. 사용자별 편집 횟수")  
# 대중문화 분야
#for i in range(len(culture_list)):
#    globals()[culture_list[i]+'_user'] = globals()[culture_list[i]].groupby(['uname']).count()['change']
#    st.write(culture_radio[i], globals()[culture_list[i]+'_user'])

# 학문 분야
#for i in range(len(academic_list)):
#    globals()[academic_list[i]+'_user'] = globals()[academic_list[i]].groupby(['uname']).count()['change']
#    st.write(academic_radio[i], globals()[academic_list[i]+'_user'])

#평균 사용자별 편집 횟수
col1_m, col2_m = st.columns(2)
with col1_m:
    st.markdown("**대중문화 페이지별 유저 당 평균 수정 횟수**")
    culture_m_list = []
    for i in range(len(culture_list)):
        df_temp = df_culture[df_culture['page'] == culture_list[i]]
        val_count = df_temp['uname'].value_counts().mean()
        page = culture_list[i]
        culture_m_list.append([page, val_count])
    culture_m = pd.DataFrame(culture_m_list, columns = ['page', 'count'])
    fig3 = plt.figure(figsize=(10,5))
    sb.barplot(data=culture_m, x='page', y='count',alpha=0.8)
    plt.xticks(rotation=90)
    st.pyplot(fig3)

with col2_m:
    st.markdown("**학문 페이지별 유저 당 평균 수정 횟수**")
    academic_m_list = []
    for i in range(len(academic_list)):
        df_temp = df_academic[df_academic['page'] == academic_list[i]]
        val_count = df_temp['uname'].value_counts().mean()
        page = academic_list[i]
        academic_m_list.append([page, val_count])
    academic_m = pd.DataFrame(academic_m_list, columns = ['page', 'count'])
    fig4 = plt.figure(figsize=(10,5))
    sb.barplot(data=academic_m, x='page', y='count',alpha=0.8)
    plt.xticks(rotation=90)
    st.pyplot(fig4)
    
fig1_2_1 = px.histogram(df_culture, x='uname', color="page", opacity = 0.6)
fig1_2_1.update_layout(title_text='대중문화/서브컬처 분야 사용자별 편집 횟수')
st.plotly_chart(fig1_2_1, use_container_width=True)
fig1_2_2 = px.histogram(df_academic, x='uname', color="page", opacity = 0.6)
fig1_2_2.update_layout(title_text='학문 분야 사용자별 편집 횟수')
st.plotly_chart(fig1_2_2, use_container_width=True)    

result("""
<b>결과</b>

- x축 영역이 넓을수록 편집에 참여한 사용자가 많고, y값이 클수록 한 사용자가 여러 번, 집중적으로 편집했다고 볼 수 있습니다.
- 편집자가 많을수록 다양한 사람이 편집에 고루 참여하는 것이라고 단정짓기는 어려워 보입니다. 예컨대 임진왜란 키워드를 보면 특정 몇 명이 100번 넘게 수정하고 있는 것을 확인할 수 있습니다. 보통 문서 편집이 활발하지 않을수록 편향성이 심할 것이라고 생각하기 쉬운데, 편집이 활발한 문서이더라도 특정 몇몇 편집자들의 편향이 크게 들어갈 우려가 있다고 볼 수 있을 듯합니다.
- 이렇게 요약해볼 수 있을 것 같습니다: 편집자 수와 편집 횟수는 어느 정도 비례하는 것으로 보입니다. 둘 다 적은 경우는 상대적으로 내용이 빈약할 수밖에 없습니다 (소수가 방대한 양을 작성할 수 있으나, 정보가 편향될 우려가 있습니다). // 반면 수정이 빈번하게 이루어지는 키워드는 내용이 상대적으로 충실해질 것이나, 편집자 수가 많아지는 만큼 특정 소수 편집자들에 의한 반달리즘에 취약하다고 볼 수 있을 것입니다 (특히 논란 있는 키워드일 경우 더욱 그러합니다).
""")
st.write(" ")

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
   
result("""
<b>결과</b>

업데이트가 자주 되고, 다양한 의견을 낼 수 있는 키워드가 수정 횟수도 많고 편집에 참여하는 사람 수도 많은 것으로 보입니다. 특히 '학문' 분야에서는 '임진왜란'과 같은 한국사 관련 페이지가 다른 페이지에 비해 월등히 높은 수정 횟수를 보여주고 있습니다. 이는 '임진왜란'이 활발한 토론의 장이 되고 있음을 시사하나, 이 토론이 반달리즘에 가까울지 건설적인 지식 구성에 가까운지는 더 자세히 데이터를 살펴보아야 알 수 있을 듯합니다.
""")

st.write(" ")
st.write(" ")

st.markdown("""
[참고] 임진왜란 키워드의 코멘트는 아래에서 확인할 수 있습니다.
""")

for i in range(len(culture_list)): #대중문화
  globals()['comment_'+culture_list[i]] = globals()[culture_list[i]]['other'].values.tolist()
  globals()['comment_'+culture_list[i]] = [x for x in globals()['comment_'+culture_list[i]] if x not in '()'] # 비어 있는 열(괄호만 있는 경우) 삭제
  globals()['comment_'+culture_list[i]] = [x[1:-1] for x in globals()['comment_'+culture_list[i]]] # 앞뒤 괄호 삭제

for i in range(len(academic_list)): #학문
  globals()['comment_'+academic_list[i]] = globals()[academic_list[i]]['other'].values.tolist()
  globals()['comment_'+academic_list[i]] = [x for x in globals()['comment_'+academic_list[i]] if x not in '()'] # 비어 있는 열(괄호만 있는 경우) 삭제
  globals()['comment_'+academic_list[i]] = [x[1:-1] for x in globals()['comment_'+academic_list[i]]] # 앞뒤 괄호 삭제

st.write(comment_imjin)

st.markdown("## 3. 수정 양상")
st.write("수정이 어떻게 이루어지는지를 더 자세히 살펴보기 위해, 문서 역사의 여러 정보를 활용하여 각 페이지의 수정 양상 또한 알아보았습니다. 먼저, 삭제 및 추가된 글자의 수 및 삭제/추가된 횟수를 페이지별로 살펴보았습니다. 다음으로, 시간에 따른 수정 양상의 변화를 cumulative sum 그래프로 나타내었습니다.")
st.markdown("### 3.1. 삭제 vs 추가 횟수")
# change column 숫자로 변환 (대중문화)
df_culture['change2'] = df_culture['change'].map(lambda x: x.lstrip('(').rstrip(')'))
df_culture['change2'] = df_culture.change2.apply(lambda x: float(x))
# change column 숫자로 변환 (학문)
df_academic['change2'] = df_academic['change'].map(lambda x: x.lstrip('(').rstrip(')'))
df_academic['change2'] = df_academic.change2.apply(lambda x: float(x))

def newchange(change):
    if change > 0: 
        return 'plus'
    elif change == 0: 
        return 'same'
    elif change < 0:
        return 'minus'
df_culture['newchange'] = df_culture.change2.apply(lambda x: newchange(x))
df_academic['newchange'] = df_academic.change2.apply(lambda x:newchange(x))

st.markdown("**대중문화/서브컬처 추가/삭제의 페이지별 양상**")
st.markdown("plus는 글자가 추가된 횟수, minus는 글자가 삭제된 횟수, same은 글자수 변화가 없었던 수정 횟수를 의미합니다.")
df_culture2 = df_culture.sort_values(['newchange'], ascending = True)
fig3_c1 = px.histogram(df_culture2, x='page', color="newchange", color_discrete_sequence = {0:'rgb(243, 97, 126)',1:'rgb(97, 97, 243)',2:'rgb(158, 206, 182)'}, barmode='group', opacity = 0.6)
st.plotly_chart(fig3_c1, use_container_width=True)

st.markdown("**학문 추가/삭제의 페이지별 양상**")
df_academic2 = df_academic.sort_values(['newchange'], ascending = True)
fig3_c2 = px.histogram(df_academic2, x='page', color="newchange", color_discrete_sequence = {0:'rgb(243, 97, 126)',1:'rgb(97, 97, 243)',2:'rgb(158, 206, 182)'}, barmode='group', opacity = 0.6)
st.plotly_chart(fig3_c2, use_container_width=True)

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
#selected_item1 = st.radio("대중문화/서브컬처 추가 vs 삭제", culture_list)	

#for i in range(len(culture_list)):
#    if selected_item1 == culture_list[i]:
#        st.write("추가: {}번, 삭제: {}번".format(len(c_plist[i]),len(c_mlist[i])))

a_plist = [aesthetic_plus_list, call_plus_list, epidemic_plus_list, greekromanmyth_plus_list, hungarianrevolution_plus_list, imjin_plus_list, montyhall_plus_list, officiallanguage_plus_list, pascaltriangle_plus_list, spotlight_plus_list]
a_mlist = [aesthetic_minus_list, call_minus_list, epidemic_minus_list, greekromanmyth_minus_list, hungarianrevolution_minus_list, imjin_minus_list, montyhall_minus_list, officiallanguage_minus_list, pascaltriangle_minus_list, spotlight_minus_list]
#selected_item2 = st.radio("학문 추가 vs 삭제", academic_list)	

#for i in range(len(academic_list)):
#    if selected_item2 == academic_list[i]:
#        st.write("추가: {}번, 삭제: {}번".format(len(a_plist[i]),len(a_mlist[i])))
        
        
st.markdown("### 3.2. 시간에 따른 수정 양상 변화")

# [필요하면 코드 사용하기] 키워드(페이지)별 편집 기간
# (추가) max, min 값도 제시해서 얼마나 오래되었는지, 얼마나 최근까지 수정되었는지 파악할 수 있을 것
#for i in range(len(culture_list)): #대중문화
#  st.write(globals()[culture_list[i]]['datetime'].max() - globals()[culture_list[i]]['datetime'].min())
#for i in range(len(academic_list)): #학문
#  st.write(globals()[academic_list[i]]['datetime'].max() - globals()[academic_list[i]]['datetime'].min())

st.markdown("***3.2.1. 키워드(페이지)별 편집 글자수 추이 (파랑: 추가/빨강색: 삭제)***")
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
        
result("""
<b>결과</b>

대중문화/서브컬처 편집 글자수 추이: 페이지별로 시간에 따른 수정과 삭제를 확인할 수 있습니다. 시간이 최근으로 갈수록(원점과 가까워질수록) 삭제가 더 우세한 것으로 보입니다.
""")

st.write(" ")

st.markdown("***3.2.2. 페이지별 수정 양상 추이***")
st.write("변화한 글자수의 cumulative sum이 페이지별로 시간에 따라 어떻게 변화했는지를 확인한 그래프입니다.")
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

result("""
<b>결과</b>

- 키워드(페이지)별 시기에 따른 수정 양상 추이로, 추가/삭제된 글자수의 총합(즉, 당시 문서의 총 글자수)을 파악할 수 있는 그래프입니다. 각각의 페이지는 다른 색상으로 표현되어 있습니다.
- 기울기가 수평에 가까울수록 거의 문서가 수정되지 않았다(글자수가 변화하지 않았다)고 해석할 수 있습니다. (e.g. 게임서버의 경우 문서의 큰 변화가 없는 것으로 보입니다.)
- y=0에 가까울수록 문서 글자수가 적으므로, 문서 내용이 충실하지 못하다고도 해석할 수 있을 것 같습니다. (키워드가 지엽적이라서 설명할 내용 자체가 상대적으로 적을 수도 있고, 글자수가 많다고 충실한 문서라 해석할 순 없겠지만, 글자수 또한 문서 내용의 질에 기여하는 한 가지 지표이므로, 이러한 해석을 해볼 수 있습니다.)
- 수직으로 선이 그어지는 경우, 그리고 이런 수직선이 많이 보이는 경우, 급속한 문서의 변화가 지속되는 것으로 반달리즘 등을 의심해 볼 수 있습니다.
- 어느 정도 지점이 되면 기울기가 완만해지는 모습을 보일 때, 충실하고 질이 높은 문서라고 볼 수 있습니다. 문서 내용이 축적되고, 어느 정도 합의에 이르렀다는 것을 의미하기 때문입니다.
""")


#4. 데이터 분석 결과 2
st.markdown("<hr>", unsafe_allow_html=True)
title('데이터 분석 결과 2')
st.markdown("# 학문 분야 500개, 대중문화 분야 397개 데이터 비교")

st.write('이제 조금 더 큰 규모의 데이터를 분석해보겠습니다. 학문 분야 500개, 대중문화 분야 397개의 데이터를 수집하여 분석에 활용했습니다.')

df_culture_aug0 = load_data('dataculture_aug.csv')
df_academic_aug0 = load_data('dataacademic_aug.csv')

df_culture_aug = df_culture_aug0.copy()
df_academic_aug = df_academic_aug0.copy()

# wordcloud
st.markdown('## 1. 코멘트 텍스트 분석: Wordcloud')
st.write('나무위키의 편집 기록에는 편집한 유저가 코멘트를 남길 수 있습니다.\n해당 편집이 왜 이루어졌는지, 어떤 부분을 편집했는지 등을 자유롭게 작성할 수 있습니다.\n다만 의무적으로 남겨야 하는 것은 아니고 유저가 원할 때만 남기는 것입니다.\n우선 코멘트를 분석하여, 분야별로 지식의 수정이 어떻게 이루어지고 있는지 알아보려고 합니다.')

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

st.markdown('### 1.1. 학문 분야의 편집 코멘트 워드클라우드')
show_wordcloud(df_academic_aug)

st.markdown('### 1.2. 대중문화 분야의 편집 코멘트 워드클라우드')
show_wordcloud(df_culture_aug)

result('''
<b>결과</b>

- 코멘트만 보았을 때는 두 분야 모두 지식을 단조적으로 축적하기보다는 삭제 역시 활발히 이루어지는 것으로 보입니다.
- 그런데 '삭제'라는 키워드가 등장했다고 해서 반드시 지식의 축적이 덜하다고 볼 수는 없습니다.
- 대표적으로 맞춤법이나 문법을 지적하는 코멘트같은 경우, '삭제'를 언급한다고 해서 지식을 삭제한다고 보기 어렵습니다.
- 또 코멘트 작성은 의무가 아니기 때문에 코멘트가 없는 경우도 많습니다.
- 지식이 어떻게 형성되고 있는지 더 정확한 모습을 알아보기 위해서는 구체적인 편집 기록을 볼 필요가 있습니다.
''')
st.write(" ")

# 편집 텀
st.markdown('## 2. 편집 텀')
st.write('편집이 얼마나 자주 이루어지는지도 지식의 형성 과정과 관련이 있는 중요한 요소입니다.\n이를테면 편집이 평균 한 달 간격으로 이루어지는 문서와 평균 하루 간격으로 이루어지는 문서가 있다고 생각해 봅시다.\n물론 각 문서가 다루는 대상의 성격에 따라 다르겠지만 전자는 잘못된 정보가 있어도 쉽게 수정되지 않고 많은 이용자에게 무방비하게 노출됩니다.\n편집이 자주 이루어지는 문서는 (어디까지나 상대적으로) 오정보에 강건합니다.\n그렇다면 학문 분야와 대중문화 분야는 어느 쪽에 더 가까울까요?')

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

result('''
<b>결과</b>

- 위 그래프의 x축은 각 분야별 한 문서의 평균 편집 간격(일)을, y축은 각 분야 문서 전체에서 특정 편집 간격인 문서의 비율이 얼마나 되는지를 나타냅니다.
- 즉 편집 간격이 0일에 가까운 문서가 많으면, 다시 말해 편집이 활발하게 이루어지면 차트의 좌상단이 높은 형태의 그래프가 됩니다.
- 그래프에서 확연히 드러나듯 대중문화 분야의 문서는 편집 간격이 0일에 가까운 문서가 많고, 0일에서 멀어질수록 점점 상대빈도가 작아집니다.
- 학문 분야도 편집 간격이 그렇게 긴 것은 아니지만 대중문화와는 달리 일주일 이내의 편집 간격을 가진 문서가 많다고는 보기 힘듭니다.
- 다시 말해 학문 분야의 문서는 한번 잘못된 내용이 있으면 계속 노출될 가능성이 대중문화 분야에 비해서는 조금 더 높다고 할 수 있습니다.
- 그러나 편집 간격이 짧다고 무조건 좋은 것은 아닙니다. 의견이 다른 사용자끼리 대립이 일어나서 비슷한 내용이 계속해서 썼다가 지워지는 이른바 '수정 전쟁'이 일어나고 있을 가능성이 있기 때문입니다.
- 결국 지식이 어떤 방식으로 축적되는지 알아보려면 편집 기록의 전체적인 추이를 볼 필요가 있습니다.
''')
st.write(" ")

# 추이
st.markdown('## 3. 편집 추이')
st.write('각 분야별로 편집이 어떻게 이뤄지는지 추이를 살펴볼 차례입니다.\n추이를 살펴보면 어떤 식으로 지식이 형성되고 있는지 살펴볼 수 있습니다.')
st.markdown('''
- 그런데 각 문서는 편집 기록의 양상이 다릅니다. 어떤 문서는 150번 수정되었을 수 있고 어떤 문서는 500번 수정되었을 수 있습니다.
- 이를 보정하기 위해 문서가 처음 생성되었을 때부터 특정 스텝까지의 기록을 볼 겁니다.
- 스텝이 100이라고 하면, (편집 횟수가 100회 이상인 문서에 한해) 첫번째 편집부터 100번째 편집까지만 고려하겠다는 것입니다.
- 또한 분석을 할 때는 t번째 편집 버전의 글자 수와, 그 다음 t+1번째 편집 버전의 글자 수를 비교합니다.
- 첫번째 편집에서 글자 수가 100이었고, 두번째 편집을 통해 글자 수가 200이 되었다면 양적으로 2배 증가한 것이 됩니다. 이런 식으로 문서의 글자 수, 다시 말해 지식의 양이 어떻게 변화해 나가는지 그 추이를 분석할 수 있습니다.
- 조건을 만족하는 모든 문서에 대해 각각 위와 같은 방식으로 추이를 구하고, 분야별로 그 추이들의 평균을 구하여 그래프로 나타냈습니다.
''')

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

plot_history([df_academic_aug, df_culture_aug], labels=['academic', 'culture'], length=50, fromr1=True)
plot_history([df_academic_aug, df_culture_aug], labels=['academic', 'culture'], length=100, fromr1=True)

result('''
<b>결과</b>

- 총 스텝을 50으로 했을 때와 100으로 했을 때의 그래프입니다.
- 그래프에서 0은 문서의 글자 수에 아무런 변화가 없었다는 것이고, 0보다 큰 것은 글자 수가 늘어났음을, 작은 것은 글자 수가 줄어들었음을 나타냅니다.
- 즉 0을 기준으로 그래프를 통해 지식이 전반적으로 추가되고 있는지 삭제되고 있는지 볼 수 있다는 것입니다.
- 대중문화 관련 문서는 그래프가 전반적으로 0 위에 있습니다. 즉 편집이 전반적으로 양의 방향으로 일어나고 있다는 것입니다.
- 학문 관련 문서는 그래프가 0 아래에 있는 경우도 적지 않습니다. 누군가가 추가한 지식을 (어떤 이유든지 간에) 다른 사람이 삭제하는 양상이 상대적으로 자주 관찰된다고 볼 수 있습니다.
- 그래프가 똑같이 0 위를 지나갈 때도, 대중문화 관련 문서는 학문 관련 문서보다 상대적으로 위쪽에 그래프가 그려집니다.
- 이는 지식이 추가되는 편집 양상일 때 대중문화 관련 문서가 학문 관련 문서보다 더 많은 양의 정보가 추가된다는 뜻입니다.
''')

st.write(" ")

#결론
st.markdown("<hr>", unsafe_allow_html=True)
title("결론")
with st.expander("시사점 및 제언"):
    st.markdown("""1. 나무위키를 통해 효과적인 집단지성의 구축이 가능합니다. 다만, 활발한 축적 방식의 토론을 기반으로 할 때 질 높은 집단지성을 형성할 수 있을 것으로 보입니다.""")
    st.markdown("""2. 학문 분야의 글은 대중문화 분야에 비해 대체로 편집도 적고 의견이 빠르게 수렴되지만, 토론이 가능한 주제의 경우 더 다채로운 축적과 수정의 양상이 드러났습니다. 이를 통해 토론에 대한 홍보와 커뮤니티 수칙 형성의 필요성을 언급해볼 수 있습니다.""")
    st.markdown("""3. 교육에서의 활용: 교육에서 나무위키와 같은 위키를 활용하여(올바른 활용 예시를 모델링하여), 개별적.우발적 학습 시의  가이드라인을 제공할 수 있을 것으로 보입니다.""")
