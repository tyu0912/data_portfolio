import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import mechanicalsoup
from datetime import date
from datetime import datetime
import sys

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

screenPage = browser.get("http://elite.finviz.com/screener.ashx?v=152&f=fa_fpe_profitable,fa_pe_profitable,fa_pfcf_0to,geo_usa&ft=4&c=0,1,2,3,4,5,6,7,8,9,10,13,32,33,43,44,45,49,52,53,54,55,57,65,66,67http://finviz.com/screener.ashx?v=152&f=fa_fpe_profitable,fa_pe_profitable,fa_pfcf_0to,geo_usa&ft=4&c=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70")

dataPage = browser.get("http://elite.finviz.com/export.ashx?v=151&f=fa_fpe_profitable,fa_pe_profitable,fa_pfcf_0to,geo_usa&ft=4")

stocklist = dataPage.content.decode()


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


conn = sqlite3.connect('stockdata.sqlite')
cur = conn.cursor()

#sys.exit("Error message")

cur.executescript('''

    -- DROP TABLE IF EXISTS `stock_master`;

    CREATE TABLE IF NOT EXISTS `stock_master` (

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

    cur.executescript("INSERT OR IGNORE INTO `stock_master` (" + header2+ ") VALUES (" + item +")")

print ('finished')
