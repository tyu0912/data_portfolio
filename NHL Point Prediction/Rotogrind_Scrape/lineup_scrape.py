import urllib.request
from bs4 import BeautifulSoup
from datetime import date
import os

today = date.today()
scrape_date = today.strftime("%Y-%m-%d")

#os.chdir('C:\\Users\\tyu\\Google_Drive\\DATA_PROJECTS\\NHL\\Rotogrind_Scrape\\')

filehandle = open('active_players.txt', 'w')

url = "https://rotogrinders.com/lineups/nhl?date=" + scrape_date + "&site=draftkings"

#print(url)

html = urllib.request.urlopen(url).read()
 
soup = BeautifulSoup(html, "html.parser")

games = soup.findAll("a", { "class" : "player-popup"})

for items in games:
	try:
		a = items['title']
		filehandle.write(a + '\n')
	except:
		b = items.text
		filehandle.write(b + '\n')

	#a = items['href']
	#p1 = a[a.rfind('/')+1:]
	#p2 = p1[:p1.rfind('-')]
	#p3 = p2.replace("-", ' ')
	
	#if p3.count(' ') >= 2:
	#	p4 = p3.replace(' ','', 1)
	#else:
	#	p4 = p3
	
	