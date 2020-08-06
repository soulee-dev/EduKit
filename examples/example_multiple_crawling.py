from EduKit.edukit import *

urls = ["http://www.holybible.or.kr/B_RHV/cgi/bibleftxt.php?VR=RHV&VL=1&CN=1&CV=99",
        "http://www.holybible.or.kr/B_RHV/cgi/bibleftxt.php?VR=0&CI=258&CV=99",
        "http://www.holybible.or.kr/B_RHV/cgi/bibleftxt.php?VR=0&CI=259&CV=99"
        ]
# 데이터를 읽어올 URL들을 배열에 넣어준다.

text = getTextFromMultipleURL(urls=urls)
# URL에서 데이터를 읽어온다

text = removeNewLines(text)
# 데이터에서 새줄(엔터키)를 지워준다

print(text)
