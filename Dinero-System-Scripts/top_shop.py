DropBox Login

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

#################################################### ALIEXPRESS ########################################
def joo_ali():
    items_list1=[]
    C=0
    APP_KEY='28880'
    #C=0
    url = 'http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.listHotProducts/'+APP_KEY+'?localCurrency=USD&categoryId=3&language=en'
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
        if C==20:
            break
        title=product['productTitle']
        item_url=product['productUrl']
        price=product['salePrice']
        img=product['imageUrl']
        shipping='-'
        x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"AliExpress"}'
        j=json.loads(x)
        items_list1.append(j)
        C=C+1


    command="db.top_shop.insert_many(items_list1)"
    exec command
    return items_list1

def joo_ali6():
    items_list6=[]
    C=0
    APP_KEY='21503'
    #C=0
    url = 'http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.listHotProducts/'+APP_KEY+'?localCurrency=USD&categoryId=509&language=en'
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
        if C==20:
            break
        title=product['productTitle']
        item_url=product['productUrl']
        price=product['salePrice']
        img=product['imageUrl']
        shipping='-'
        x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"AliExpress"}'
        j=json.loads(x)
        items_list6.append(j)
        C=C+1


    command="db.top_shop.insert_many(items_list6)"
    exec command
    return items_list6

########################################################### EBAY ########################################################
def joo_ebay():
    items_list2 = []
    C=0
    try:
        api = Connection(appid='Shaked-B-976d-45bc-a23a-71ab251884fb',config_file=None)
    #response details:
        response = api.execute('getTopSellingProducts')

        assert(response.reply.ack == 'Success')
        assert(type(response.reply.timestamp) == datetime.datetime)
        assert(type(response.reply.searchResult.item) == list)

        item = response.reply.searchResult.item[0]
        assert(type(item.listingInfo.endTime) == datetime.datetime)
        assert(type(response.dict()) == dict)

        for ITEM in response.reply.searchResult.item:
            try:
                if C==20:
                    break
                #LIST = str(ITEM).split("'value':")
                #SHIPPING_PRICE = (LIST[1].split("'"))[1]
                SHIPPING_PRICE = str(str(ITEM).split("'shippingServiceCost':")[1]).split('value')[1].split("'")[2]
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

                #if SHIPPING_PRICE == 'Free':
                #    S = 0
                #    TOTAL = float(PRICE)+float(S)
                #else:
                #    TOTAL = float(PRICE)+float(SHIPPING_PRICE)

                x='{"title":"'+TITLE+'","url":"'+URL+'","image":"'+IMG+'","price":"'+PRICE+'","shipping":"'+SHIPPING_PRICE+'","web":"Ebay"}'
                j=json.loads(x)
                items_list2.append(j)
                C=C+1
                #RESULTS_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')
                #HISTORY_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')

            except:
                continue
            #for i in items_list2:
            #    print i
            #    command="db_results.results."+username+".insert_one(i)"
            #    exec command
        command="db_.top_shop.insert_many(items_list2)"
        exec command
        return items_list2


    except ConnectionError as e:
        print(e)
        print(e.response.dict())

################################################ DX ######################################################
def joo_dx():
    items_list3=[]
    C=0
    url = 'http://www.dx.com/s/'+KEYWORDS
    values = {'name': 'Dinero',
              'location': 'Northampton',
              'language': 'Python' }
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    products_list = the_page.split("id='c_list'")
    dx_list = []
    for product in products_list:
        if C==20:
            break
        if product == products_list[0]:
            continue
        after_split = product.split('href=')[1]
        link = after_split.split(' ')[0]
        item_url = link[1:-1]
        try:
            response = requests.get(item_url)
            html_product_page = response.content
            title = str(html_product_page.split('<title>')[1].split('</title>')[0].strip())
            title = title.split('-')[0]
            shipping = str(html_product_page.split('<span class="f_shipping">')[1].split('</span>')[0])
            price = str(html_product_page.split('<span id="price" class="fl" itemprop="price">')[1].split('</span>')[0])
            product_photo = html_product_page.split("product_photo")[1]
            link_href = product_photo.split('href=')[1]
            img = link_href.split(" ")[0]
            img = img[1:-1]
            #RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
            #HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
            x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"DealExtreme"}'
            j=json.loads(x)
            items_list3.append(j)
            C=C+1
        except:
            continue
        #for i in items_list3:
        #    print i
       #     command="db_results.results."+username+".insert_one(i)"
       #     exec command
    command="db.top_shop.insert_many(items_list3)"
    exec command
    return items_list3

########################################################### Amazon ##############################3
def joo_amazon():
    items_list4 = []
    C=0
    client = MongoClient('ds063186.mlab.com',63186)
    client.credentials.authenticate('shakedinero','a/c57821688')
    db = client.credentials
    cursor = db.amazon.find()
    for i in cursor:
        x=i
    config={"access_key":str(x['access_key']),"secret_key":str(x['secret_key']),"associate_tag":str(x['associate_tag']),"locale":str(x['locale'])}
    api = API(cfg=config)
    items = api.item_search('All', Keywords=KEYWORDS,ResponseGroup='Large')
    for i in items:
        try:
            title=i.ItemAttributes.Title
            item_url=i.DetailPageURL
            img=i.MediumImage.URL
            price=i.OfferSummary.LowestNewPrice.FormattedPrice
            shipping='-'
            x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"Amazon"}'
            j=json.loads(x)
            items_list4.append(j)
            C=C+1
        except:
            continue
    command="db.top_shop.insert_many(items_list4)"
    try:
        exec command
    except:
        print "No Amazon Results"
    return items_list4



############################################################ Close files & Sync #################################################################
#results_array = '{"ebay":"'+str(ebay_list)+'","dx":"'+str(dx_list)+'","amazon":"'+str(amazon_list)+'","ali":"'+str(ali_list)+'"}'
#print "ARRAY: "+results_array


######################################
#             MAIN                  #
#####################################

######################### Connect Top_Shop DB ####################################
client = MongoClient('ds063856.mlab.com',63856)
client.top_shop.authenticate('shakedinero','a/c57821688')
db = client.top_shop

command="result = db.top_shop.delete_many({})"
exec command


t_ali=threading.Thread(target=joo_ali,args=(),name="ali")
t_ali6=threading.Thread(target=joo_ali6,args=(),name="ali6")
t_ebay=threading.Thread(target=joo_ebay,args=(),name="ebay")
#t_dx=threading.Thread(target=joo_dx,args=(),name="dx")
t_amazon=threading.Thread(target=joo_amazon,args=(),name="amazon")

try:
    t_ali.start()
except:
    print "t_ali thread error"

try:
    t_ali6.start()
except:
    print "t_ali thread error"
#try:
#    t_ebay.start()
#except:
#    print "t_ebay thread error"
#try:
#    t_dx.start()
#except:
#    print "t_dx thread error"
#try:
#    t_amazon.start()
#except:
#    print "t_amazon thread error"

print "Dinero2Mongo Script is DONE!"
