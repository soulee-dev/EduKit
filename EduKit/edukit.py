import requests
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from collections import Counter
from matplotlib import pyplot as plt
import platform
from matplotlib import font_manager, rc
import numpy as np

plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Windows':
    font_path = "C:/Windows/Fonts/malgun.ttf"
elif platform.system() == 'Linux':
    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf';

font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

kkma = Kkma()

def getTextFromURL(url):
    """특정한 웹 사이트에 있는 모든 문자들을 가져옵니다.

    :param url: 데이터를 가져올 웹사이트의 주소
    :type url: 문자열
    :returns: url에 있는 모든 문자들
    :rtype: 문자열

    >>> getTextFromURL("https://news.naver.com")

    """
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style'
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output

def getTextFromMultipleURL(urls):
    """여러 웹 사이트에 있는 모든 문자들을 가져옵니다.

    :param urls: 데이터를 가져올 웹사이트의 주소
    :type urls: 리스트형
    :returns: url에 있는 모든 문자들
    :rtype: 문자열

    >>> urls = ['https://news.naver.com', 'https://news.daum.net']
    >>> getTextFromMultipleURL(urls)

    """
    text = ""

    for url in urls:
        text += getTextFromURL(url)

    return text

def removeNewLines(text):
    """새줄 문자(엔터키) 를 삭제합니다.

    :param text: 새줄 문자를 삭제할 문자열
    :type text: 문자열
    :returns: 새줄 문자가 제거된 문자열
    :rtype: 문자열

    >>> text = '안녕하세요\\n배가고파요'
    >>> removeNewLines(text)
    안녕하세요 배가고파요

    """

    return text.replace('\n', ' ').replace('\r', '')

def getNouns(text):
    """문장 안에 있는 모든 명사들을 추출합니다.

    :param text: 명사를 추출할 문장
    :type text: 문자열
    :returns: 문장안에 있는 모든 명사
    :rtype: 리스트형

    >>> text = '우리학교는 산에있는 학교이다.'
    >>> getNouns(text)
    ['우리학교', '산', '학교']

    """
    return kkma.nouns(removeNewLines(text))

def frequnecyNouns(nouns, max_result):
    """명사들의 빈도수를 분석합니다.

    :param nouns: 명사들이 담긴 리스트
    :type nouns: 리스트형
    :param max_result: 상위 n개를 추출함
    :type max_result: 정수형
    :returns: 문장안에 있는 모든 명사들의 갯수
    :rtype: Counter형

    >>> text = '우리학교는 산에있는 학교이다.'
    >>> nouns = getNouns(text)
    >>> frequnecyNouns(nouns)
    Counter[('우리학교', 1), ('산', 1), ('학교', 1)]

    """
    return Counter(nouns).most_common(max_result)

def freqeuncyToArray(counter):
    """명사 빈도수 데이터를 차트의 각각 축제목, y값, x값 으로 변환해줍니다.

    :param counter: 명사들이 담긴 리스트
    :type counter: Counter형
    :returns: 축제목, y값, x값
    :rtype: Counter형

    >>> text = '우리학교는 산에있는 학교이다.'
    >>> nouns = getNouns(text)
    >>> top_nouns = frequnecyNouns(nouns)
    >>> freqeuncyToArray(top_nouns)
    ['우리학교, '산', '학교'], [1, 1, 1], [1, 2, 3]

    """
    labels = []
    frequencies = []
    for key in counter:
        labels.append(key[0])
        frequencies.append(key[1])

    x_arry = np.arange(len(labels))

    return labels, frequencies, x_arry

def getHeadlineNews(crawl_times=10):
    """네이버 헤드라인 기사들의 URL을 갖고옵니다.

      :param crawl_times: 최대 몇개의 기사를 갖고올지
      :type crawl_times: 정수형
      :returns: 네이버 헤드라인 기사 URL
      :rtype: 리스트형

      >>> getHeadlineNews(crawl_times=2)
      ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=001&aid=0011794888', 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=025&aid=0003023797']

      """
    res = requests.get('https://news.naver.com')
    html_page = res.text
    soup = BeautifulSoup(html_page, 'html.parser')
    href = soup.select('#today_main_news > div.hdline_news > ul > li:nth-of-type(1) > div.hdline_cluster_more > a')[0]['href']

    urls = []

    res = requests.get('https://news.naver.com' + href)
    html_page = res.text
    soup = BeautifulSoup(html_page, 'html.parser')

    for times in range(1, crawl_times):
        urls.append(soup.select(f"#main_content > div:nth-of-type(2) > ul.type06_headline > li:nth-of-type({times}) > dl > dt:nth-of-type(2) > a")[0]['href'])

    return urls

def drawPlot(x, y, labels):
    """네이버 헤드라인 기사들의 URL을 갖고옵니다.

          :param x: 차트의 x값
          :type x: 리스트형
          :param y: 차트의 y값
          :type y: 리스트형
          :param labels: 차트의 축제목
          :type labels: 리스트형
          :returns: 차트
          :rtype: 차트

          >>> x = [1, 2, 3, 4]
          >>> y = [5, 2, 4, 3]
          >>> labels = ['가', '나', '다', '라']
          차트
   """
    plt.bar(x, y)
    plt.xticks(x, labels)
    plt.yticks(sorted(y))
    plt.show()