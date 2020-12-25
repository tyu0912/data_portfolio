from twilio.rest import TwilioRestClient
import datetime
import sys

with open("Active.txt", 'r+') as myfile:
    oldstocks = myfile.read().splitlines()
    oldstocklist = list()
    for x in oldstocks:
        y = x.split(',')
        oldstocklist.append(y[0])

with open("Active.txt", 'r+') as myfile:
    curlines = sum(1 for _ in myfile)
    if curlines >= 10:
        print ('Max Number Stocks Allowed')
        sys.exit()
    else:
        NumAdd = 10 - curlines
        print ('Room to add: ' + str(NumAdd) )
        print ('Adding...')

today = datetime.date.today()

with open('2_result.txt', newline='') as file:
    Lines = file.read().splitlines()
    myfile = open("Active.txt", 'a')

    counter = 0

    for items in Lines:
        stocks = items.split(',')
        if "Buy" in stocks[1] and stocks[0] not in oldstocklist and counter != NumAdd:
            print (stocks[0])
            output = (stocks[0] + ',' + stocks[1] + ', ' + str(today) + '\n')
            myfile.write(output)
        else:
            if counter == 0:
                print ('No New Stock to Add')

        counter = counter + 1



accountSID = 
authToken = 

twilioCli = TwilioRestClient(accountSID, authToken)

myTwilioNumber =
myCellPhone = 

#message = twilioCli.messages.create(body='This is a Python test',from_=myTwilioNumber, to=myCellPhone)
