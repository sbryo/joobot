
### This Web-App Created BY SHAKED BRAIMOK ###
####### APP NAME: Dinero #######

import os
import cmd
from pymongo import MongoClient
import flask
import subprocess
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json
import dropbox
import functools
import urllib
import urllib2
import requests

app = flask.Flask(__name__)
app.secret_key = "abcdefghijklmnoppqrstuvwxyz"

def check_login(func):
	def wrapper(*args, **kwargs):
        	if "username" in flask.session:
            		return func(*args, **kwargs)
        	else:
            		return flask.redirect("/")
	return functools.update_wrapper(wrapper, func)

@app.route("/")
def loginPage():
	if "username" in flask.session:
        	email = flask.session['username']
        	client = MongoClient('ds019254.mlab.com', 19254)
        	client.users.authenticate('shakedinero','a57821688')
        	db = client.users
        	collection = db.users
        	cursor = db.users.find()
        	for doc in cursor:
            		if email == doc['email']:
            			return flask.redirect("/dinero")
	else:
		return flask.render_template('dinero-login.html')


@app.route("/signup")
def signup():
	return flask.render_template("signup.html")

@app.route("/signing", methods=['GET','POST'])
def signing():
	if "email" in flask.request.form:
		try:
			x=0
        		client = MongoClient('ds019254.mlab.com', 19254)
        		client.users.authenticate('shakedinero','a57821688')
        		db = client.users
        		collection = db.users
        		cursor = db.users.find()
        		email = flask.request.form['email']
        		password = flask.request.form['password']
        		for doc in cursor:
        			### if user already exists
            			if "password" in flask.request.form and email == doc['email'] and password == doc['password']:
            				x=x+1
            				return flask.redirect("/")
            			### Create user
            		if x==0:
            			j=json.loads('{"email":"'+email+'","password":"'+password+'"}')
            			db.users.insert(j)
            			flask.session['username'] = email
            			return flask.redirect("/dinero")

        	except:
        		return flask.redirect("/")
        else:
        	return flask.redirect("/")







@app.route("/login", methods=['GET','POST'])
def login():
	if "email" in flask.request.form:
		try:
        		client = MongoClient('ds019254.mlab.com', 19254)
        		client.users.authenticate('shakedinero','a57821688')
        		db = client.users
        		collection = db.users
        		cursor = db.users.find()
        		email = flask.request.form['email']
        		password = flask.request.form['password']
        		for doc in cursor:
            			if "password" in flask.request.form and email == doc['email'] and password == doc['password']:
            				flask.session['username'] = doc['email']
            				return flask.redirect("/dinero")
        	except:
        		return flask.redirect("/")
        else:
        	return flask.redirect("/")



@app.route("/dinero")
@check_login
def dinero():
	return flask.render_template('index.html')


@app.route("/loading")
@check_login
def test():
    #while results file is null
	return flask.render_template('loading.html')

#@app.route("/results")
#@check_login
#def results():
 #   file = open("users-folders/shaked/Results.txt",'r')
  #  lines = file.readlines()
   # return flask.render_template('results.html',lines=lines)

@app.route("/my-space")
@check_login
def my_space():
	return flask.render_template('my-space.html')

@app.route("/marketplace")
@check_login
def market():
	return flask.render_template('market.html')

@app.route("/search",methods=['GET', 'POST'])
@check_login
def append():
        email = flask.session['username']
        user = email.split("@")[0]
        domain = ((email.split("@")[1]).split("."))[0]
        username=user+domain
        #app_key='4e3oofj6zqcx5dh'
        #app_secret='vaoz96wg81222c9'
        #flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        #authorize_url = flow.start()
        #client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
        client = MongoClient('ds139425.mlab.com',39425)
        client.search.authenticate('shakedinero','a57821688')
        db = client.search
        client3 = MongoClient('ds019254.mlab.com',19254)
        client3.history.authenticate('shakedinero','a57821688')
        db_history = client3.history
        #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        #(out, err) = proc.communicate()
        #PATH=(out.split('\n'))[0]
        if "add" in flask.request.form:
                try:
                    text = flask.request.form['add']
                    #processed_text = text.upper()
                    #response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    j = json.loads('{"search":"'+text+'"}')
                    command="db.search."+username+".delete_many({})"
                    exec command
                    command="db.search."+username+".insert(j)"
                    exec command
                    command="db_history.history."+username+".insert(j)"
                    exec command
                    return flask.redirect("/results")

                except:
                    text = flask.request.form['add']
                    #processed_text = text.upper()
                    #response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    j = json.loads('{"search":"'+text+'"}')
                    command="db.search."+username+".insert(j)"
                    exec command
                    return flask.render_template("404.html")
        else:
            return flask.render_template("404.html")

@app.route("/history")
@check_login
def my_history_page():
    try:
        email = flask.session['username']
        user = email.split("@")[0]
        domain = ((email.split("@")[1]).split("."))[0]
        username=user+domain
        list = []
        client3 = MongoClient('ds019254.mlab.com',19254)
        client3.history.authenticate('shakedinero','a57821688')
        db_history = client3.history
        #cursor = db_history.history.shaked.find()
        command="cursor = db_history.history."+username+".find()"
        exec command
    # Make list for html page
        for document in cursor:
            x = []
            x.append(document['title'])
            x.append(document['price'])
            x.append(document['shipping'])
            x.append(document['url'])
            x.append(document['image'])
            list.append(x)
        return flask.render_template('my-history.html',list=list)
    except:
        return flask.render_template('404.html')


@app.route("/results/add_to_favorites/<LINE>",methods=['GET','POST'])
@check_login
def addtofavorites(LINE):
    email = flask.session['username']
    user = email.split("@")[0]
    domain = ((email.split("@")[1]).split("."))[0]
    username=user+domain
    client4 = MongoClient('ds019254.mlab.com',19254)
    client4.favorites.authenticate('shakedinero','a57821688')
    db_favorites = client4.favorites

    client = MongoClient('ds019254.mlab.com',19254)
    client.results.authenticate('shakedinero','a57821688')
    db_results = client.results
    command="cursor = db_results.results."+username+".find()"
    exec command
    #cursor = db_results.results.shaked.find()
    for doc in cursor:
        STR=LINE.replace("%20"," ")
        if STR in doc['title']:
            #db_favorites.favorites.shaked.insert(doc)
            command="db_favorites.favorites."+username+".insert(doc)"
            exec command
        else:
            continue
    return flask.redirect("/results")

@app.route("/favorites")
@check_login
def my_archive_page():
    try:
        email = flask.session['username']
        user = email.split("@")[0]
        domain = ((email.split("@")[1]).split("."))[0]
        username=user+domain
    	list=[]
        client4 = MongoClient('ds019254.mlab.com',19254)
        client4.favorites.authenticate('shakedinero','a57821688')
        db_favorites = client4.favorites
        command="cursor = db_favorites.favorites."+username+".find()"
        exec command
        # Make list for html page
        for document in cursor:
            x = []
            x.append(document['title'])
            x.append(document['price'])
            x.append(document['shipping'])
            x.append(document['url'])
            x.append(document['image'])
            list.append(x)
        return flask.render_template('my-favorites.html',list=list)
    except:
        return flask.render_template('404.html')


@app.route("/results")
@check_login
def get_results():
        try:
                email = flask.session['username']
                user = email.split("@")[0]
                domain = ((email.split("@")[1]).split("."))[0]
                username=user+domain
                #subprocess.call("Dinero-System-Scripts/ebaydropbox.py")
                #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
                #(out, err) = proc.communicate()
                #PATH=(out.split('\n'))[0]
                list = []
                #os.system("python "+PATH+"/Dinero-System-Scripts/Dinero2Mongo.py")
                Dinero2Mongo(username)
                x = []  ### This is the list for html
                client = MongoClient('ds019254.mlab.com',19254)
                client.results.authenticate('shakedinero','a57821688')
                db = client.results
                command="cursor = db.results."+username+".find()"
                exec command
#Make list for html page
                for document in cursor:
                    x = []
                    x.append(document['title'])
                    x.append(document['price'])
                    x.append(document['shipping'])
                    x.append(document['url'])
                    x.append(document['image'])
                    list.append(x)
                return flask.render_template('results.html',list=list)
        except:
                return flask.render_template('404.html')

@app.route("/favorites/delete/<LINE>",methods=['GET','POST'])
@check_login
def favorite_delete(LINE):
    email = flask.session['username']
    user = email.split("@")[0]
    domain = ((email.split("@")[1]).split("."))[0]
    username=user+domain
    list=[]
    STR = LINE.replace('%20',' ')
    client4 = MongoClient('ds019254.mlab.com',19254)
    client4.favorites.authenticate('shakedinero','a57821688')
    db_favorites = client4.favorites
    command="cursor = db_favorites.favorites."+username+".find()"
    exec command
    for doc in cursor:
        if STR not in doc['title']:
            list.append(doc)
        else:
            continue
    command="favorite = db_favorites.favorites."+username+".delete_many({})"
    exec command
    for doc in list:
    	command="db_favorites.favorites."+username+".insert(doc)"
        exec command
    #db_favorites.favorites.shaked.insert(list)
    return flask.redirect("/favorites")


@app.route("/history/delete/<LINE>",methods=['GET','POST'])
@check_login
def history_delete(LINE):
    email = flask.session['username']
    user = email.split("@")[0]
    domain = ((email.split("@")[1]).split("."))[0]
    username=user+domain
    list=[]
    STR = LINE.replace('%20',' ')
    client4 = MongoClient('ds019254.mlab.com',19254)
    client4.history.authenticate('shakedinero','a57821688')
    db_history = client4.history
    command="cursor = db_history.history."+username+".find()"
    exec command
    for doc in cursor:
        if STR not in doc['title']:
            list.append(doc)
        else:
            continue
    command="history = db_history.history."+username+".delete_many({})"
    exec command
    for doc in list:
    	command="db_history.history."+username+".insert(doc)"
        exec command
    #db_history.history.shaked.insert(list)
    return flask.redirect("/history")


@app.route("/public")
@check_login
def public():
	file = open("PUBLIC/publish-file",'r')
	lines = file.readlines()
	file.close()
	return flask.render_template('public.html',lines=lines)


@app.route("/public/appending")
@check_login
def public_append():
        if "add" in flask.request.form:
                #data = str(flask.request.data)
                text = flask.request.form['add']
                processed_text = text.upper()
                file = open("PUBLIC/publish-file",'a')
                file.write(processed_text+'\n')
                file.close()
                return flask.redirect("/public")

@app.route("/logout")
def logout():
	if "username" in flask.session:
        	del flask.session["username"]
    		return flask.redirect("/")
    	else:
    		return flask.redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404



################################################################################################################################
######################################################### SEARCH FUNCTION ######################################################
################################################################################################################################
def Dinero2Mongo(username):
        ######################### Connect Results DB ####################################
    client = MongoClient('ds019254.mlab.com',19254)
    client.results.authenticate('shakedinero','a57821688')
    db_results = client.results

    ######################## Connect Search DB ################################
    client2 = MongoClient('ds139425.mlab.com',39425)
    client2.search.authenticate('shakedinero','a57821688')
    db_search = client2.search

    ########################## Connect History DB ########################
    client3 = MongoClient('ds019254.mlab.com',19254)
    client3.history.authenticate('shakedinero','a57821688')
    db_history = client3.history

    ############## get KEYWORDS from Search DB #################################
    command="cursor = db_search.search."+username+".find()"
    exec command
    for document in cursor:
        KEYWORDS=document['search']

    ########################################################### EBAY ########################################################
    ebay_list = []
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

                x='{"title":"'+TITLE+'","url":"'+URL+'","image":"'+IMG+'","price":"'+PRICE+'","shipping":"'+SHIPPING_PRICE+'","web":"Ebay"}'
                j=json.loads(x)
                ebay_list.append(j)
                #RESULTS_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')
                #HISTORY_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')

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
    dx_list = []
    for product in products_list:
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
            dx_list.append(j)
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
    data = urllib.urlencode(values)
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    #products_list=the_page.split('id="atfResults')[1]
    products_list = the_page.split('result_')
    amazon_list=[]
    for i in products_list:
        try:
            item_url = ((i.split('normal" href="')[1]).split('"'))[0]
            title = ((i.split('title="')[1]).split('"')[0])
            if KEYWORDS in title:
                img = ((i.split('img src="')[1]).split('"')[0])
                price = ((i.split('class="a-size-base a-color-price s-price a-text-bold">')[1].split('<')[0]))
                shipping = "-"
                x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"Amazon"}'
                j=json.loads(x)
                amazon_list.append(j)
            #RESULTS_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
            #HISTORY_FILE.write(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img+'\n')
        except:
            continue

    ########################################################### AliExpress ###################################33
    url = 'http://aliexpress.com/wholesale?catId=0&initiative_id=AS_20160721045815&SearchText='+KEYWORDS
    values = {'name': 'Dinero',
              'location': 'Northampton',
              'language': 'Python' }
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data,headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    products_list=the_page.split('<a class="history-item product "')
    ali_results = []
    ali_history = []
    ali_list = []

    for i in products_list:
        try:
            item_url = ((i.split('href="')[1]).split('"'))[0]
            title = ((i.split('title="')[1]).split('"'))[0]
            img = ((i.split('image-src="')[1]).split('"'))[0]
            price = (((i.split('<span class="value" itemprop="price">')[1]).split('<'))[0])[3:-1]
            shipping = "-"
            #ali_results.append(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img)
            #ali-history.append(title+" = "+price+" = "+shipping+" = "+item_url+" = "+img)
            x='{"title":"'+title+'","url":"'+item_url+'","image":"'+img+'","price":"'+price+'","shipping":"'+shipping+'","web":"AliExpress"}'
            j=json.loads(x)
            ali_list.append(j)
        except:
            continue

    ############################################################ Close files & Sync #################################################################
    results_array = '{"ebay":"'+str(ebay_list)+'","dx":"'+str(dx_list)+'","amazon":"'+str(amazon_list)+'","ali":"'+str(ali_list)+'"}'
    print "ARRAY: "+results_array

    command1="result = db_results.results."+username+".delete_many({})"
    command2="db_results.results."+username+".insert(ebay_list)"
    command3="db_results.results."+username+".insert(dx_list)"
    command4="db_results.results."+username+".insert(ali_list)"
    command5="db_results.results."+username+".insert(amazon_list)"
    exec command1
    exec command2
    exec command3
    exec command4
    exec command5

    #command1="db_history.history."+email+".insert(ebay_list)"
    #command2="db_history.history."+email+".insert(dx_list)"
    #command3="db_history.history."+email+".insert(ali_list)"
    #command4="db_history.history."+email+".insert(amazon_list)"

if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=1213, host="0.0.0.0", debug=True)

