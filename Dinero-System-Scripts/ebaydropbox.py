#DropBox Login
import dropbox
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json
import subprocess
import os
import urllib
import urllib2
import requests


#Dropbox Connection
app_key='4e3oofj6zqcx5dh'
app_secret='vaoz96wg81222c9'
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')

### FILES
#proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#PATH=(out.split('\n'))[0]

SEARCH_FILE, metadata = client.get_file_and_metadata('/Shaked/SearchFile.txt')
KEYWORDS = SEARCH_FILE.read()
SEARCH_FILE.close()

HISTORY_FILE, metadata = client.get_file_and_metadata('/Shaked/History.txt')
R = HISTORY_FILE.read()
HISTORY_FILE = open('/tmp/History.txt','w')
HISTORY_FILE.write(R)
HISTORY_FILE.close()

RESULTS_FILE = open('/tmp/Results.txt','w')
HISTORY_FILE = open('/tmp/History.txt','a')

########################################################### EBAY ########################################################
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

            #if SHIPPING_PRICE == 'Free':
            #    S = 0
            #    TOTAL = float(PRICE)+float(S)
            #else:
            #    TOTAL = float(PRICE)+float(SHIPPING_PRICE)


            RESULTS_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')
            HISTORY_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')

        except:
            continue


except ConnectionError as e:
    print(e)
    print(e.response.dict())

################################################ DX ######################################################
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

for product in products_list:
    if product == products_list[0]:
        continue
    after_split = product.split('href=')[1]
    link = after_split.split(' ')[0]
    item_url = link[1:-1]
    print item_url

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
        RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')

    except:
        continue

########################################################### Amazon ##############################3
url = 'http://www.amazon.com/s/field-keywords='+KEYWORDS
values = {'name': 'Dinero',
          'location': 'Northampton',
          'language': 'Python' }
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

data = urllib.urlencode(values)
req = urllib2.Request(url,data,headers)
response = urllib2.urlopen(req)
the_page = response.read()
#products_list=the_page.split('id="atfResults')[1]
products_list = the_page.split('result_')

for i in products_list:
    try:
        item_url = ((i.split('normal" href="')[1]).split('"'))[0]
        title = ((i.split('title="')[1]).split('"')[0])
        img = ((i.split('img src="')[1]).split('"')[0])
        price = ((i.split('class="a-size-base a-color-price s-price a-text-bold">')[1].split('<')[0]))
        shipping = "-"
        RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
    except:
        continue

############################################################ Close files & Sync #################################################################

RESULTS_FILE.close()
HISTORY_FILE.close()

r_file=open("/tmp/Results.txt",'r')
r = r_file.read()
response = client.put_file('/shaked/Results.txt', r,overwrite=True)

h_file=open("/tmp/History.txt",'r')
h=h_file.read()
response = client.put_file('/shaked/History.txt', h,overwrite=True)

