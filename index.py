
### This Web-App Created BY SHAKED BRAIMOK ###
####### APP NAME: Dinero #######

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

app = flask.Flask(__name__)
app.secret_key = "abcdefghijklmnoppqrstuvwxyz"


#FACEBOOK_APP_ID = '275750752809365'
#FACEBOOK_APP_SECRET = 'a6a10a5b3843f53f28f59a1e5a413588'

#oauth = OAuth()

#facebook = oauth.remote_app('facebook',
   # base_url='https://graph.facebook.com/',
    #request_token_url=None,
   # access_token_url='/oauth/access_token',
 #   authorize_url='https://www.facebook.com/dialog/oauth',
  #  consumer_key=FACEBOOK_APP_ID,
  #  consumer_secret=FACEBOOK_APP_SECRET,
  #  request_token_params={'scope': ('email, ')}
#)

#@facebook.tokengetter
#def get_facebook_token():
   # return session.get('facebook_token')

#def pop_login_session():
   # session.pop('logged_in', None)
    #session.pop('facebook_token', None)

#@app.route("/facebook_login")
#def facebook_login():
  #  return facebook.authorize(callback=url_for('facebook_authorized',
     #   next=request.args.get('next'), _external=True))

#@app.route("/facebook_authorized")
#@facebook.authorized_handler
#def facebook_authorized(resp):
    #next_url = request.args.get('next') or url_for('index')
    #if resp is None or 'access_token' not in resp:
       # return redirect('/')

    #session['logged_in'] = True
  #  session['facebook_token'] = (resp['access_token'], '')

   # return redirect('/dinero')


def check_login(func):
	def wrapper(*args, **kwargs):
        	if "username" in flask.session:
            		return func(*args, **kwargs)
        	else:
            		return flask.redirect("/")
	return functools.update_wrapper(wrapper, func)

@app.route("/")
def loginPage():
	if "username" in session:
        	email = session['username']
        	client = MongoClient('ds019254.mlab.com', 19254)
        	client.users.authenticate('shakedinero','a57821688')
        	db = client.users
        	collection = db.users
        	cursor = db.users.find()
        	for doc in cursor:
            		if email == doc['email']:
            			return flask.redirect("/dinero")
	#elif flask.session['logged_in'] == True:
	#	return flask.redirect("/dinero")
	else:
		return flask.render_template("dinero-login.html")

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
	email = flask.session['username']
	return flask.render_template('my-space.html',email=email)

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
                    command="db_history.history."+username+".insert(j)"
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
            x.append(document['search'])
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
            x.append(document['web'])
            list.append(x)
        return flask.render_template('my-favorites.html',list=list)
    except:
        return flask.render_template('404.html')


@app.route("/results")
@check_login
def get_results():
    #try:
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
        list.append(x)
    return flask.render_template('results.html',list=list)
    #except:
     #   return flask.render_template('404.html')

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
        if STR not in doc['search']:
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





if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=1213, host="0.0.0.0", debug=True)

