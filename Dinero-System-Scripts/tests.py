#DropBox Login

import json
from pymongo import MongoClient
import dropbox
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import subprocess
import os
import urllib
import urllib2
import requests
import sys
import threading
from multiprocessing.pool import ThreadPool
from amazonproduct import API


########################################################### EBAY ########################################################
def joo_ebay():
    items_list2 = []
    C=0
    api = Connection(appid='Shaked-B-976d-45bc-a23a-71ab251884fb',config_file=None,debug=True)
    #response details:
    response = api.execute('getTopSellingProducts')

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)

    for ITEM in response.reply.searchResult.item:
        print ITEM



#################################################### ALIEXPRESS ########################################
def joo_ali():
    items_list1=[]
    C=0
    APP_KEY='21503'
    #C=0
    url = 'http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.listHotProducts/'+APP_KEY+'?localCurrency=USD&categoryId=200000297&language=en'
    values = {'name': 'Joo',
              'location': 'Northampton',
              'language': 'Python' }
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    j=json.loads(str(the_page))
    products_list=j['result']['products']
    #print products_list
    for product in products_list:
        title=product['productTitle']
        item_url=product['productUrl']
        price=product['salePrice']
        img=product['imageUrl']
        shipping='-'
        print title
        print item_url
        print price
        print img
      #  if C==20:
      #      break
      #  title=product['productTitle'].split('</font>')[1].split('<font>')[0]
      #  item_url=product['productUrl']
      #  price=product['salePrice']
      #  img=product['imageUrl']
      #  shipping='-'
      #  x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"AliExpress"}'
      #  j=json.loads(x)
      #  items_list1.append(j)
      #  C=C+1


    #command="db_results.results."+username+".insert_many(items_list1)"
    #exec command
    #return items_list1

joo_ebay()
joo_ali()