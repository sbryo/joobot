#!/usr/bin/python2.6

import urllib
import urllib2
import requests
import dropbox


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

#SEARCH_FILE, metadata = client.get_file_and_metadata('/Shaked/SearchFile.txt')
#KEYWORDS = SEARCH_FILE.read()
#SEARCH_FILE.close()

HISTORY_FILE, metadata = client.get_file_and_metadata('/Shaked/History.txt')
R = HISTORY_FILE.read()
HISTORY_FILE = open('/tmp/History.txt','w')
HISTORY_FILE.write(R)
HISTORY_FILE.close()

RESULTS_FILE = open('/tmp/Results.txt','w')
HISTORY_FILE = open('/tmp/History.txt','a')

keywords = raw_input('input:')
url = 'http://www.dx.com/s/'+keywords
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
        print title
        shipping = str(html_product_page.split('<span class="f_shipping">')[1].split('</span>')[0])
        print shipping
        price = str(html_product_page.split('<span id="price" class="fl" itemprop="price">')[1].split('</span>')[0])
        print price
        product_photo = html_product_page.split("product_photo")[1]
        link_href = product_photo.split('href=')[1]
        img = link_href.split(" ")[0]
        img = img[1:-1]
        print img
        RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        RESULTS_FILE.close()
        HISTORY_FILE.close()

        r_file=open("/tmp/Results.txt",'r')
        r = r_file.read()
        response = client.put_file('/shaked/Results.txt', r,overwrite=True)

        h_file=open("/tmp/History.txt",'r')
        h=h_file.read()
        response = client.put_file('/shaked/History.txt', h,overwrite=True)
    except:
        continue

