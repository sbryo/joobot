import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json
import subprocess
import os

### FILES
proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
PATH=(out.split('\n'))[0]

SEARCH_FILE = open('../users-folders/shaked/SearchFile.txt','r')
KEYWORDS = SEARCH_FILE.read()
SEARCH_FILE.close()
RESULTS_FILE = open('../users-folders/shaked/Results.txt','w')
HISTORY_FILE = open('../users-folders/shaked/History.txt','a')

### EBAY API
try:
    api = Connection(appid='Shaked-B-976d-45bc-a23a-71ab251884fb',config_file=None)
#response details:
    response = api.execute('findItemsAdvanced',{'keywords':KEYWORDS})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)
    #print (((str(item).split(','))[10]).split(':')).split(',')
    #print (str(item).split(','))


    for ITEM in response.reply.searchResult.item:
        try:
            LIST = str(ITEM).split("'value':")
            SHIPPING_PRICE = (LIST[1].split("'"))[1]
            if SHIPPING_PRICE == '0.0':
                SHIPPING_PRICE = 'Free'

            LIST = str(ITEM).split("'title':")
            TITLE = (LIST[1].split("'"))[1]

            LIST = str(ITEM).split("'viewItemURL':")
            URL = (LIST[1].split("'"))[1]

            LIST = str(ITEM).split("'galleryURL':")
            IMG = (LIST[1].split("'"))[1]
            LIST = (str(ITEM).split("'currentPrice':"))[1].split("'value':")
            PRICE = (LIST[1].split("'"))[1]

            #print "TITLE = "+TITLE
            #print "PRICE = "+PRICE
            #print "SHIPPING_PRICE = "+SHIPPING_PRICE
            #print "URL = "+URL
            #print "IMG = "+IMG

            RESULTS_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')
            HISTORY_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')

        except:
            continue



    #list = (str(response.reply.searchResult.item[0])).split(',')

    #print (list[4].split(':'))[4]

 #   for i in list:
 #       field=i.split(':')
 #       print field[0]

#        TITLE = (i.split(':'))





    #for item in response.reply.searchResult.item:
     #   print item



except ConnectionError as e:
    print(e)
    print(e.response.dict())



