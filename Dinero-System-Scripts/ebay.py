import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json

try:
    api = Connection(appid='Shaked-B-976d-45bc-a23a-71ab251884fb',config_file=None)
#response details:
    response = api.execute('findItemsAdvanced',{'keywords':'Armani Watch'})

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

            LIST = str(ITEM).split("'title':")
            TITLE = (LIST[1].split("'"))[1]

            LIST = str(ITEM).split("'viewItemURL':")
            URL = (LIST[1].split("'"))[1]

            LIST = str(ITEM).split("'galleryURL':")
            IMG = (LIST[1].split("'"))[1]

            LIST = (str(ITEM).split("'currentPrice':"))[1].split("'value':")
            PRICE = (LIST[1].split("'"))[1]


            print "TITLE = "+TITLE
            print "PRICE = "+PRICE
            print "SHIPPING_PRICE = "+SHIPPING_PRICE
            print "URL = "+URL
            print "IMG = "+IMG
            #FIELDS = str(ITEM).split(',')
           # TITLE = ((FIELDS[4].split(':'))[1])[2:-1]
           # SHIPPING = ((FIELDS[10].split(':'))[1])[2:-1]
           # URL = ((FIELDS[10].split(':'))[1])[2:-1]
            #print TITLE+" = "+SHIPPING
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



