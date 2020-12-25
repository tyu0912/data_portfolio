import mechanicalsoup
import csv
import itertools
import statistics

url = "http://finviz.com/login.ashx"
email = "dodozf@gmail.com"
password = "game1234"

browser = mechanicalsoup.Browser()
login_page = browser.get(url)
login_form = login_page.soup.find("form", {"name":"login"})

login_form.find("input", {"name": "email"})["value"] = email
login_form.find("input", {"name": "password"})["value"] = password

response = browser.submit(login_form, login_page.url)

screenPage = browser.get("http://elite.finviz.com/screener.ashx?v=152&f=fa_fpe_profitable,fa_pe_profitable,fa_pfcf_0to,geo_usa&ft=4&c=0,1,2,3,4,5,6,7,8,9,10,13,32,33,43,44,45,49,52,53,54,55,57,65,66,67")

dataPage = browser.get("http://elite.finviz.com/export.ashx?v=151&f=fa_fpe_profitable,fa_pe_profitable,fa_pfcf_0to,geo_usa&ft=4")



stocklist = dataPage.content.decode()

stocklist = stocklist.splitlines()

finalreport = list()
finalreport2 = list()

header = stocklist[0].replace("\"","")
header = header.split(",")

header.append("MOA50-MOA20")
header.append("MOA50-MOA20NORM")

finalreport.append(header)

PEcol = header.index("P/E")
pricecol  = header.index("Price")
ROEcol = header.index("Return on Equity")
ROAcol = header.index("Return on Assets")
MOA20col = header.index("20-Day Simple Moving Average")
MOA50col = header.index("50-Day Simple Moving Average")
MOA200col = header.index("200-Day Simple Moving Average")
MOA50MOA20DIF = header.index("MOA50-MOA20")
MOA50MOA20NORMDIF = header.index("MOA50-MOA20NORM")

UpTrended = list()
UpTrendedNorm = list()

# Step 1 of analysis
for stock in stocklist:
    stock = stock.replace("\"","")
    stock = stock.split(",")
    try:
        PE = float(stock[PEcol])
        price = float(stock[pricecol])
        ROE = float(stock[ROEcol].replace("%",""))
        ROA = float(stock[ROAcol].replace("%",""))
        MOA20 = float(stock[MOA20col].replace("%",""))
        MOA50 = float(stock[MOA50col].replace("%",""))
        MOA200 = float(stock[MOA200col].replace("%",""))

    except:
        # print MOA20
        continue

    if PE < 25 and price < 100 and ROE > 15 and ROA > 7.5:
        #print stock
        stock = stock + [round(MOA50-MOA20,2)]
        UpTrended.append(round(MOA50-MOA20,2))
        stock = stock + [round((MOA50/50)-(MOA20/20),2)]
        UpTrendedNorm.append(round((MOA50/50)-(MOA20/20),2))

        finalreport.append(stock)

#print stdev(UpTrendedNorm)

for stock in finalreport[1:]:
    if stock[MOA50MOA20DIF] > statistics.mean(UpTrended) and ((0-statistics.stdev(UpTrendedNorm))/2 < stock[MOA50MOA20NORMDIF] < (0+statistics.stdev(UpTrendedNorm))/2):
        print (stock)
        finalreport2.append(stock)

# Step 2 of analysis




# print ("There were %d lines printed.") % Counter

print (finalreport)

myfile = open("finalreporttest.csv", 'w', newline='')
wr = csv.writer(myfile)
wr.writerows(finalreport2)


#outFile = open("finalreport.csv", 'wb')
#outFile.write(finalreport)
#outFile.close()

#for stock in range(len(stocklist)):
#    print stocklist[stock][7]


# outFile = open("stocks.csv", 'wb')
#outFile.write(dataPage.content)
# outFile.close()
