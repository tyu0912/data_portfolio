import urllib.request
from bs4 import BeautifulSoup
import os


#os.chdir('C:\\Users\\tyu\\Google_Drive\\DATA_PROJECTS\\NHL\\Rotogrind_Scrape\\')

filehandle = open('active_players.txt', 'w')

#url = "https://www.rosterresource.com/nhl-roster-grid/"
url = 'https://docs.google.com/spreadsheets/d/1XJKA5CcFku8XFJSV2N3bpWUBDHQJyIyOjAvhutkt1kA/pubhtml?gid=1189242863&single=true&chrome=false&widget=false&headers=false'


html = urllib.request.urlopen(url).read()
 
soup = BeautifulSoup(html, "html.parser")

for EachPart in soup.select('td[class*="s"]'):
    if len(EachPart.get_text()) > 4 and not EachPart.get_text().isupper():
        name = EachPart.get_text()
        name = name.strip()
        name = name.replace('(A)','')
        name = name.replace('(C)','')
        output = name + '\n'
        filehandle.write(output)
    else:
        continue
