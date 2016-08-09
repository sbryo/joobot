
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

app = flask.Flask(__name__)

@app.route("/")
def start():
	return flask.render_template('dinero-login.html')

@app.route("/dinero")
def dinero():
	return flask.render_template('index.html')


@app.route("/loading")
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
def my_space():
	return flask.render_template('my-space.html')

@app.route("/search",methods=['GET', 'POST'])
def append():
        #app_key='4e3oofj6zqcx5dh'
        #app_secret='vaoz96wg81222c9'
        #flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        #authorize_url = flow.start()
        #client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
        client = MongoClient('ds139425.mlab.com',39425)
        client.search.authenticate('shakedinero','a57821688')
        db = client.search
        #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        #(out, err) = proc.communicate()
        #PATH=(out.split('\n'))[0]
        if "add" in flask.request.form:
                try:
                    text = flask.request.form['add']
                    #processed_text = text.upper()
                    #response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    j = json.loads('{"search":"'+text+'"}')
                    db.search.shaked.delete_many({})
                    db.search.shaked.insert(j)
                    return flask.redirect("/results")

                except:
                    text = flask.request.form['add']
                    #processed_text = text.upper()
                    #response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    j = json.loads('{"search":"'+text+'"}')
                    db.search.shaked.insert(j)
                    return flask.render_template("404.html")
        else:
            return flask.render_template("404.html")

@app.route("/history")
def my_history_page():
    try:
        list = []
        client3 = MongoClient('ds019254.mlab.com',19254)
        client3.history.authenticate('shakedinero','a57821688')
        db_history = client3.history
        cursor = db_history.history.shaked.find()
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
def addtofavorites(LINE):
    client4 = MongoClient('ds019254.mlab.com',19254)
    client4.search.authenticate('shakedinero','a57821688')
    db_favorites = client4.favorites

    client = MongoClient('ds019254.mlab.com',19254)
    client.results.authenticate('shakedinero','a57821688')
    db_results = client.results
    cursor = db.results.shaked.find()
    for doc in cursor:
        STR=LINE.replace("%20"," ")
        if STR in doc['title']:
            db_favorites.favorites.shaked.insert(doc)
        else:
            continue
    return flask.redirect("/results")

@app.route("/favorites")
def my_archive_page():
    try:
    	list=[]
        client4 = MongoClient('ds019254.mlab.com',19254)
        client4.favorites.authenticate('shakedinero','a57821688')
        db_favorites = client4.favorites
        cursor = db_favorites.favorites.shaked.find()
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
def get_results():
        try:
                #subprocess.call("Dinero-System-Scripts/ebaydropbox.py")
                proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
                PATH=(out.split('\n'))[0]
                list = []
                os.system("python "+PATH+"/Dinero-System-Scripts/Dinero2Mongo.py")

                x = []  ### This is the list for html
                client = MongoClient('ds019254.mlab.com',19254)
                client.results.authenticate('shakedinero','a57821688')
                db = client.results
                cursor = db.results.shaked.find()

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
def favorite_delete(LINE):
    list=[]
    STR = LINE.replace('%20',' ')
    client4 = MongoClient('ds019254.mlab.com',19254)
    client4.favorites.authenticate('shakedinero','a57821688')
    db_favorites = client4.favorites
    cursor = db_favorites.favorites.shaked.find()
    for doc in cursor:
        if STR not in doc['title']:
            list.append(doc)
        else:
            continue
    favorite = db_favorites.favorites.shaked.delete_many({})
    for doc in list:
    	db_favorites.favorites.shaked.insert(doc)
    #db_favorites.favorites.shaked.insert(list)
    return flask.redirect("/favorites")


@app.route("/history/delete/<LINE>",methods=['GET','POST'])
def history_delete(LINE):
    list=[]
    STR = LINE.replace('%20',' ')
    client4 = MongoClient('ds019254.mlab.com',19254)
    client4.history.authenticate('shakedinero','a57821688')
    db_history = client4.history
    cursor = db_history.history.shaked.find()
    for doc in cursor:
        if STR not in doc['title']:
            list.append(doc)
        else:
            continue
    history = db_history.history.shaked.delete_many({})
    for doc in list:
    	db_history.history.shaked.insert(doc)
    #db_history.history.shaked.insert(list)
    return flask.redirect("/history")


@app.route("/public")
def public():
	file = open("PUBLIC/publish-file",'r')
	lines = file.readlines()
	file.close()
	return flask.render_template('public.html',lines=lines)


@app.route("/public/appending")
def public_append():
        if "add" in flask.request.form:
                #data = str(flask.request.data)
                text = flask.request.form['add']
                processed_text = text.upper()
                file = open("PUBLIC/publish-file",'a')
                file.write(processed_text+'\n')
                file.close()
                return flask.redirect("/public")


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=1213, host="0.0.0.0", debug=True)

