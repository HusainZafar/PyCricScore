#BeautifulSoup, re, urllib, pynotify
from bs4 import BeautifulSoup
import urllib, re

html = urllib.urlopen('http://www.cricbuzz.com/live-cricket-scores/17687/uae-vs-afg-3rd-t20i-afghanistan-tour-of-united-arab-emirates-2016').read()
soup = BeautifulSoup(html, 'html.parser')
texts = soup.findAll(text=True)

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', ' '.join(element).encode('utf-8')):
		return False
	return True

almost = filter(visible, texts)

for i in range(len(almost)):
	if 'Bowler' in almost[i]:
		index = i

almost = almost[:index]

for i in range(len(almost)):
	if 'Photos' in almost[i]:
		index = i

almost = almost[index+5:]

almost[-1] = u''
almost[-2] = u''
almost[-3] = u''
almost[-7] = u''
almost[-8] = u''
almost[-9] = u''

new = []
for i in almost:
	new.append(i)
	new.append(' ')

almost = ''.join(new)


q = ''
for i in range(len(almost)):
	if ord(almost[i]) > 127:
		q+=' '	
	else:
		q+=str(almost[i])

q = q.strip()

f1 = q.find('Batsman')
f2 = q.find('SR')
q = q[:f1] + '\n' + q[f2+2:]

q = re.sub("Day", "\nDay",q)

import pynotify
pynotify.init("app-name")
pynotify.Notification("Score Update", q, "").show()

'''
import subprocess

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

sendmessage(q)
'''
