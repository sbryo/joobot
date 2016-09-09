
### This Web-App Created BY SHAKED BRAIMOK ###
####### APP NAME: Joobot #######

import os
import cmd
from pymongo import MongoClient
import flask
from flask import url_for,request,session,redirect
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
from flask_oauth import OAuth
from flask.ext.compress import Compress
import random
from bson.objectid import ObjectId

app = flask.Flask(__name__)
#compress = Compress()
Compress(app)
#compress.init_app(app)
app.secret_key = "abcdefghijklmnoppqrstuvwxyz"


FACEBOOK_APP_ID = '1407152752632423'
FACEBOOK_APP_SECRET = '3eae4ca9c231852bb9deb352c80059b5'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('joobot')
    if resp is None or 'access_token' not in resp:
        return redirect('/')

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect('/joobot')


def check_login(func):
	def wrapper(*args, **kwargs):
		try:
			if ("username" in flask.session) or (session['logged_in']==True):
				return func(*args, **kwargs)
			else:
				return flask.redirect("/")
		except:
			return flask.redirect("/")
	return functools.update_wrapper(wrapper, func)

@app.route("/")
def loginPage():
	if ("username" in flask.session):
		email = flask.session['username']
		client = MongoClient('ds019254.mlab.com', 19254)
		client.users.authenticate('shakedinero','a57821688')
		db = client.users
		collection = db.users
		cursor = db.users.find()
		for doc in cursor:
			if str(str(email).lower()) == doc['email']:
				return flask.redirect("/joobot")
	try:
		if (session['logged_in']==True):
			return flask.redirect("/joobot")
		else:
			return flask.render_template("joobot-login.html")
	except:
		return flask.render_template("joobot-login.html")
	return flask.render_template("joobot-login.html")


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
            			if "password" in flask.request.form and str(email.lower()) == doc['email'] and password == doc['password']:
					x=x+1
            				return flask.redirect("/")
            			### Create user
            		if x==0:
            			j=json.loads('{"email":"'+email+'","password":"'+password+'"}')
            			db.users.insert(j)
            			flask.session['username'] = email
            			return flask.redirect("/joobot")

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
					if "password" in flask.request.form and str(email.lower()) == doc['email'] and password == doc['password']:
						flask.session['username'] = doc['email']
						session['logged_in']=False
						return flask.redirect("/joobot")
		except:
			return flask.redirect("/")
        else:
        	return flask.redirect("/")



@app.route("/joobot")
@check_login
def joobot():
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
	if ("username" in flask.session):
		username = (str(flask.session['username'])).split('@')[0]
	try:
		if (session['logged_in']==True):
			data = facebook.get('/me').data
			username = (data['name'])
	except:
		print "Exception in my-space | logged_in == true not exists"
	return flask.render_template('my-space.html',username=username)

@app.route("/marketplace")
@check_login
def market():
	return flask.render_template('market.html')

@app.route("/search",methods=['GET', 'POST'])
@check_login
def append():
	try:
		if (session['logged_in']==True):
			data = facebook.get('/me').data
			if 'id' in data and 'name' in data:
    				user_id = data['id']
    				username = (data['name']).replace(' ','')+str(user_id)
    	except:
    		print "Exception in Search on session['logged-in']"
        if ("username" in flask.session):
        	email = flask.session['username']
        	user = email.split("@")[0]
        	domain = ((email.split("@")[1]).split("."))[0]
        	username=user+domain
        print "############################  "+username+"  #########################"
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
        print "######################## Connected to DB ####################"
        #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        #(out, err) = proc.communicate()
        #PATH=(out.split('\n'))[0]
        if "add" in flask.request.form:
        	try:
                	text = flask.request.form['add']
                    #processed_text = text.upper()
                    #response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    	j = json.loads('{"search":"'+text+'"}')
                    	time=str(datetime.datetime.now()).split('.')[0]
                    	hj = json.loads('{"search":"'+text+'","time":"'+time+'"}')
                    	command="db.search."+username+".delete_many({})"
                    	exec command
                    	command="db.search."+username+".insert(j)"
                    	exec command
                    	command="db_history.history."+username+".insert(hj)"
                    	exec command
                    	print "######################## added to dbs ##########################"
                    	return flask.redirect("/results")

                except:
                    	text = flask.request.form['add']
                    	#processed_text = text.upper()
                    	#response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    	j = json.loads('{"search":"'+text+'"}')
                    	command="db.search."+username+".insert(j)"
                    	exec command
                    	command="db_history.history."+username+".insert(j)"
                    	exec command
                    	return flask.render_template("404.html")
        else:
        	return flask.render_template("404.html")

@app.route("/history")
@check_login
def my_history_page():
	if ("username" in flask.session):
		email = flask.session['username']
        	user = email.split("@")[0]
        	domain = ((email.split("@")[1]).split("."))[0]
        	username=user+domain
    	try:
            if (session['logged_in']==True):
                data = facebook.get('/me').data
                if 'id' in data and 'name' in data:
                    user_id = data['id']
                    username = (data['name']).replace(' ','')+str(user_id)
        except:
    		print "exception in /history , logged_in not exist"

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
            x.append(document['search'])
            x.append(document['time'])
            list.append(x)
        return flask.render_template('my-history.html',list=list)



@app.route("/results/add_to_favorites/<LINE>",methods=['GET','POST'])
@check_login
def addtofavorites(LINE):
    if ("username" in flask.session):
        email = flask.session['username']
        user = email.split("@")[0]
        domain = ((email.split("@")[1]).split("."))[0]
        username=user+domain
    try:
        if (session['logged_in']==True):
            data = facebook.get('/me').data
            if 'id' in data and 'name' in data:
                user_id = data['id']
                username = (data['name']).replace(' ','')+str(user_id)
    except:
        print "Exception in add_to_favorite"
    	client4 = MongoClient('ds019254.mlab.com',19254)
    	client4.favorites.authenticate('shakedinero','a57821688')
    	db_favorites = client4.favorites
	client = MongoClient('ds019254.mlab.com',19254)
    	client.results.authenticate('shakedinero','a57821688')
    	db_results = client.results

    	STR=LINE
    	#command="cursor = db_results.results."+username+".find()"
        command = "cursor=db_results.results."+username+".find({'_id': ObjectId('"+STR+"') })"
    	exec command
    	#cursor = db_results.results.shaked.find()
    	for doc in cursor:
#        STR=LINE.replace("%20"," ")
        	#if STR in str(doc['_id']):
            #db_favorites.favorites.shaked.insert(doc)
            command="db_favorites.favorites."+username+".insert(doc)"
            exec command
        	#else:
            #continue
        return flask.redirect("/results")

@app.route("/favorites")
@check_login
def my_archive_page():
    if ("username" in flask.session):
		email = flask.session['username']
        	user = email.split("@")[0]
        	domain = ((email.split("@")[1]).split("."))[0]
        	username=user+domain
    try:
        if (session['logged_in']==True):
			data = facebook.get('/me').data
			if 'id' in data and 'name' in data:
    				user_id = data['id']
    				username = (data['name']).replace(' ','')+str(user_id)
    except:
        print "exception in favorites"
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
        x.append(document['web'])
        x.append(str(document['_id']))
        list.append(x)
    return flask.render_template('my-favorites.html',list=list)



@app.route("/results")
@check_login
def get_results():
    try:
        if (session['logged_in']==True):
            data = facebook.get('/me').data
            if 'id' in data and 'name' in data:
                user_id = data['id']
                username = (data['name']).replace(' ','')+str(user_id)
    except:
        if ("username" in flask.session):
            email = flask.session['username']
            user = email.split("@")[0]
            domain = ((email.split("@")[1]).split("."))[0]
            username=user+domain
    if ("username" in flask.session):
            email = flask.session['username']
            user = email.split("@")[0]
            domain = ((email.split("@")[1]).split("."))[0]
            username=user+domain
    file=open("/tmp/user.txt",'w')
    file.write(username)
    file.close()
            #subprocess.call("Dinero-System-Scripts/ebaydropbox.py")
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    PATH=(out.split('\n'))[0]
    list = []
    os.system("python "+PATH+"/Dinero-System-Scripts/Dinero2Mongo.py")
#Dinero2Mongo(username)
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
        x.append(document['web'])
        x.append(str(document['_id']))
        x.append(str(datetime.datetime.now()).split('.')[0])
        list.append(x)
    random.shuffle(list)
    return flask.render_template('results.html',list=list)
    #except:
     #   return flask.render_template('404.html')

@app.route("/results/freeshipping")
@check_login
def freeShipping():
    try:
        if (session['logged_in']==True):
            data = facebook.get('/me').data
            if 'id' in data and 'name' in data:
                user_id = data['id']
                username = (data['name']).replace(' ','')+str(user_id)
    except:
        if ("username" in flask.session):
            email = flask.session['username']
            user = email.split("@")[0]
            domain = ((email.split("@")[1]).split("."))[0]
            username=user+domain
    if ("username" in flask.session):
            email = flask.session['username']
            user = email.split("@")[0]
            domain = ((email.split("@")[1]).split("."))[0]
            username=user+domain
    client = MongoClient('ds019254.mlab.com',19254)
    client.results.authenticate('shakedinero','a57821688')
    db = client.results

    list=[]
    docs=[]
    command="cursor = db.results."+username+".find()"
    exec command
    for document in cursor:
        if ("Free" in document['shipping']) or ("free" in document['shipping']):
                docs.append(document)

#Make list for html page
    for document in docs:
        x = []
        x.append(document['title'])
        x.append(document['price'])
        x.append(document['shipping'])
        x.append(document['url'])
        x.append(document['image'])
        x.append(document['web'])
        list.append(x)
    return flask.render_template('results.html',list=list)


@app.route("/results/cheap")
@check_login
def cheap():
    try:
        if (session['logged_in']==True):
            data = facebook.get('/me').data
            if 'id' in data and 'name' in data:
                user_id = data['id']
                username = (data['name']).replace(' ','')+str(user_id)
    except:
        if ("username" in flask.session):
            email = flask.session['username']
            user = email.split("@")[0]
            domain = ((email.split("@")[1]).split("."))[0]
            username=user+domain
    if ("username" in flask.session):
            email = flask.session['username']
            user = email.split("@")[0]
            domain = ((email.split("@")[1]).split("."))[0]
            username=user+domain
    client = MongoClient('ds019254.mlab.com',19254)
    client.results.authenticate('shakedinero','a57821688')
    db = client.results

    LIST=[]
    new_list=[]
    cheap_list=[]
    list=[]

    command="cursor = db.results."+username+".find()"
    exec command
    for document in cursor:
        LIST.append(float(document['price'].replace('$','')))

    while LIST:
        minimum = LIST[0]  # arbitrary number in list
        for x in LIST:
            if x < minimum:
                minimum = x
        new_list.append(minimum)
        LIST.remove(minimum)
    command="cursor = db.results."+username+".find()"
    exec command

    docs_list=[]
    for doc in cursor:
        docs_list.append(doc)

    for i in new_list:
        for doc in docs_list:
            if float(doc['price'].replace('$','')) == float(i):
                cheap_list.append(doc)
            else:
                 continue

#Make list for html page
    for document in cheap_list:
        x = []
        x.append(document['title'])
        x.append(document['price'])
        x.append(document['shipping'])
        x.append(document['url'])
        x.append(document['image'])
        x.append(document['web'])
        list.append(x)
    return flask.render_template('results.html',list=list)



@app.route("/favorites/delete/<LINE>",methods=['GET','POST'])
@check_login
def favorite_delete(LINE):
	if (session['logged_in']==True):
		data = facebook.get('/me').data
		if 'id' in data and 'name' in data:
    			user_id = data['id']
    			username = (data['name']).replace(' ','')+str(user_id)
        if ("username" in flask.session):
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
        	if STR not in str(doc['_id']):
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
	if (session['logged_in']==True):
		data = facebook.get('/me').data
		if 'id' in data and 'name' in data:
    			user_id = data['id']
    			username = (data['name']).replace(' ','')+str(user_id)
        if ("username" in flask.session):
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
        	if STR not in doc['time']:
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

@app.route("/history_results/<LINE>",methods=['GET','POST'])
@check_login
def history_results(LINE):
	if (session['logged_in']==True):
		data = facebook.get('/me').data
		if 'id' in data and 'name' in data:
    			user_id = data['id']
    			username = (data['name']).replace(' ','')+str(user_id)
        if ("username" in flask.session):
        	email = flask.session['username']
        	user = email.split("@")[0]
        	domain = ((email.split("@")[1]).split("."))[0]
        	username=user+domain
    	list=[]
    	STR = LINE.replace('%20',' ')
    #client4 = MongoClient('ds019254.mlab.com',19254)
    #client4.history.authenticate('shakedinero','a57821688')
    #db_history = client4.history
    	client = MongoClient('ds139425.mlab.com',39425)
    	client.search.authenticate('shakedinero','a57821688')
    	db = client.search
        #text = STR
                    #processed_text = text.upper()
                    #response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
        j = json.loads('{"search":"'+STR+'"}')
	command ="db.search."+username+".delete_many({})"
    	exec command
    	command="db.search."+username+".insert(j)"
    	exec command
    	return flask.redirect("/results")



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
    	if (session['logged_in']==True):
    		session['logged_in']=False
        	return flask.redirect("/")
    	else:
    		return flask.redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404





if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=1213, host="0.0.0.0", debug=True)

