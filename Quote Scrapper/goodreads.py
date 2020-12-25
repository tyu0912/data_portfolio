import urllib.request
from bs4 import BeautifulSoup

count = 1 
fh = open('quotes.txt','w')

while True:

    url = "https://www.goodreads.com/quotes/tag/optimism?page=" + str(count)

    try:
        html = urllib.request.urlopen(url).read()
        
    except:
        print ('Done')
        break
    
    soup = BeautifulSoup(html, "html.parser")

    #mydivs = soup.find_all("div", class_="quoteText")

    test = soup.find_all('div', {"class": "quoteText"})

    for item in test:
        quote1 = str(item)
        quote2 = quote1[quote1.find('>')+1:quote1.find('<br>')]
        
        finalquote = quote2.strip()
        
        source = item.find_all('a')
        
        for idx,origin in enumerate(source):        
            if idx == 0:
                finalauthor = str(origin.contents[0])
                finalwork = ''
            else:
                finalwork = str(origin.contents[0])
        
        quotes = finalquote + '\t' + finalauthor + '\t' + finalwork
        quotes.strip()
        quotes = quotes + '\n'
        
        print (quotes)
        
        fh.write(quotes)
    
    count = count + 1 
            
    
    

