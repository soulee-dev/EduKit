from edukit import *

text = getTextFromURL("http://www.holybible.or.kr/B_GAE/cgi/bibleftxt.php?VR=GAE&VL=1&CN=1&CV=99")
text = removeNewLines(text)
nouns = getNouns(text)
top_nouns = frequnecyNouns(nouns, max_result=10)
labels, frequencies, x_array = freqeuncyToArray(top_nouns)

drawPlot(x=x_array, y=frequencies, labels=labels)