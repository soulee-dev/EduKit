from edukit import *


urls = getHeadlineNews(crawl_times=11)
# 네이버 헤드라인 기사들의 URL들을 11개 가져온다

text = getTextFromMultipleURL(urls=urls)
# URL에서 데이터를 읽어온다

nouns = getNouns(text)
# 데이터에서 명사들을 불러온다

top_nouns = frequnecyNouns(nouns, max_result=10)
# 가장 많이 나온 명사 상위 10가지를 갖고온다

labels, frequencies, x_array = freqeuncyToArray(top_nouns)
# 명사 데이터를 차트의 각각 축제목, y값, y값 으로 변환해준다.

drawPlot(x=x_array, y=frequencies, labels=labels)
# x값, y값, 축 제목을 이용해 차트를 그린다