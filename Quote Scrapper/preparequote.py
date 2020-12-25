#This is a test

import sys
sys.path.insert(0, 'C:\\Users\\ss\\Desktop\\Python_Learning\\ftpupload')

import upload2
from random import randint
import datetime 

date = datetime.date.today()

fh = open('quotes.txt').read()

quotes = fh.splitlines()

count = len(quotes)

choice = quotes[randint(0,count)]

items = choice.split('\t')

phrase = items[0] + ' by ' + items[1] + ' - as seen on www.goodreads.com' 
title = 'Positive quote of the week - ' + str(date)

upload2.wordpressupload(title, phrase)