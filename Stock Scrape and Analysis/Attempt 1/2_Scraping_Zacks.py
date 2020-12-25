import urllib.request
from bs4 import BeautifulSoup
import csv

myfile = open("2_result.txt", 'w')

with open('1_result.txt', newline='') as file:
    counter = 0
    lines = file.read().splitlines()
    for item in lines:
        row = item.split(', ')

        if counter == 0:
            print (row)
            Tickercol = row.index('Ticker')

        else:
            Ticker = row[1]

            url = 'https://www.zacks.com/stock/quote/' + Ticker
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, "html.parser")
            div = soup.findAll('div',{'class':'zr_rankbox'})
            result = []

            for x in div:
                result.extend(x)
                try: Zacksrank = result[3]
                except: continue
                Zacksrank = Zacksrank.strip()

            output = str(Ticker + ', ' + Zacksrank + '\n')
            myfile.write(output)

        counter = counter + 1
