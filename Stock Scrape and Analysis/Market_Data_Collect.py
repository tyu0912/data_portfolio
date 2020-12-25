import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import mechanicalsoup
from datetime import date
from datetime import datetime
import sys
import os

today = str(date.today())

url = "http://finviz.com/login.ashx"
email = os.getenv("finvizEmail")
password = os.getenv("finvizPass")

browser = mechanicalsoup.Browser()
login_page = browser.get(url)
login_form = login_page.soup.find("form", {"name":"login"})

login_form.find("input", {"name": "email"})["value"] = email
login_form.find("input", {"name": "password"})["value"] = password

response = browser.submit(login_form, login_page.url)

screenPage = browser.get("https://finviz.com/groups.ashx?g=sector&v=152&o=name&c=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26")

dataPage = browser.get("https://finviz.com/grp_export.ashx?g=sector&v=152&o=name")

stocklist = dataPage.content.decode()

print (stocklist)

stocklist = stocklist.splitlines()

header = stocklist[0]
header = header.replace('"','`')
header = header.replace('.','')
header = header.replace('/','')
header = header.replace('(','')
header = header.replace(')','')
header = header.replace(" ","_")
header = header.replace("-","_")
header = header.replace("200","Twohundred")
header = header.replace("20","Twenty")
header = header.replace("50","Fifty")
header = header.replace("52","Fiftytwo")

#Extra stuff goes here
header2 = header + ', DateAdded'

header = header.replace(","," TEXT,")

# Extra stuff goes here
header = header + ' TEXT, ' + 'DateAdded TEXT'


conn = sqlite3.connect('stockmarketdata.sqlite')
cur = conn.cursor()

#sys.exit("Error message")

cur.executescript('''

    -- DROP TABLE IF EXISTS `market_master`;

    CREATE TABLE IF NOT EXISTS `market_master` (

        ''' + header + '''

    );

''')

header2 = header2.replace('`','')

for item in stocklist[1:]:
    item = item.replace('"','')
    item = item.replace(", ",".")
    item = item.replace("'","")
    item = item.replace(",","','")
    #Extra Stuff goes here
    item = "'" + item + "'" + ", '" + today + "'"

    cur.executescript("INSERT OR IGNORE INTO `market_master` (" + header2+ ") VALUES (" + item +")")

print ('finished')
