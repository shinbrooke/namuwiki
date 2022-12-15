import pyautogui
import pyperclip
import time
from selenium import webdriver



url = 'https://namu.wiki/history/팬텀(메이플스토리)' # 수집할 url 링크 입력

def namu(url):
    driver = webdriver.Chrome() # 드라이버 연결
    # 웹사이트 이동
    driver.get(url) 

    # [참고] 역사 페이지 html 코드가 불분명해 pyautogui 사용해 크롤링 진행
    # 창 최대화 (열 때부터 최대화되어 있다면 코드 생략 가능)
    pyautogui.moveTo(426,25) # 커서 위치는 필요에 따라 조정: pyautogui.mouseInfo() 코드로 확인 가능
    time.sleep(1) # 로딩 속도에 따라 시간 조정 가능
    pyautogui.doubleClick()
    time.sleep(2)

    # 페이지 크롤링
    pyautogui.moveTo(166,567) # 배너 O 경우 사용 (리그베다 위키) # 스크롤 가장 위로 올렸을 때 첫 번째로 긁어올 문장 좌측 상단의 커서 위치 입력
    #pyautogui.moveTo(52,367) # 배너 X 경우 사용
    time.sleep(0.1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.moveTo(x=1328, y=757) # 스크롤 가장 아래로 내렸을 때 마지막으로 긁어올 문장 우측 하단의 커서 위치 입력
    time.sleep(0.1)
    pyautogui.scroll(-1000)
    time.sleep(1)
    pyautogui.mouseUp()

    time.sleep(0.1)

    # 페이지 복사-붙여넣기
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    # driver.close()
    global a
    a = pyperclip.paste()

    f = open('namu_c_maplephantom.txt', 'a', encoding='UTF-8') # txt 파일 이름 입력
    f.write(a)
    f.close()

# 다음 페이지 history 이어서 크롤링
namu(url)

b = a[-80:-3].split("| 비교)  r", 1)
c = b[1].split(" (", 1)

if int(c[0]) > 30:
    url2 = url + "?from=" + str(int(c[0]) - 1)
    print(namu(url2))
    i = 30
    while int(c[0]) - 1 - i > 0:
        url3 = url + "?from=" + str(int(c[0]) - 1 - i)
        print(namu(url3))
        i += 30