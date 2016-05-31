import dropbox
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json
import subprocess
import os

#Dropbox Connection
app_key='4e3oofj6zqcx5dh'
app_secret='vaoz96wg81222c9'
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')

SEARCH_FILE, metadata = client.get_file_and_metadata('/Shaked/SearchFile.txt')
KEYWORDS = SEARCH_FILE.read()
SEARCH_FILE.close()


### Ebay API ###
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

        STR = TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n'

        response = client.put_file('/shaked/Results.txt',STR,overwrite=True)

    except:
        continue

