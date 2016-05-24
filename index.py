
### This Web-App Created BY SHAKED BRAIMOK ###
####### APP NAME: Dinero #######

import os
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
        #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        #(out, err) = proc.communicate()
        #PATH=(out.split('\n'))[0]
        app_key='4e3oofj6zqcx5dh'
        app_secret='vaoz96wg81222c9'
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()
        client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')

        if "add" in flask.request.form:
                try:
                    text = flask.request.form['add']
                    #processed_text = text.upper()
                    response = client.put_file('/shaked/SearchFile.txt',text,overwrite=True)
                    return flask.redirect("/results")
                except:
                    return flask.redirect("/results")
        else:
            return flask.redirect("/results")


@app.route("/history/remove/<LINE>",methods=['GET','POST'])
def remove(LINE):
	proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        PATH=(out.split('\n'))[0]
	#if "Remove" in flask.request.form:
	#LINE = flask.request.form['name']
        H_FILE = open(PATH+"/users-folders/shaked/History.txt",'r')
        lines = H_FILE.readlines()
	H_FILE.close()
	H_FILE = open(PATH+"/users-folders/shaked/History.txt",'w')
        for line in lines:
        	if LINE not in line:
			H_FILE.write(line)
		else:
			continue
	H_FILE.close()
        return flask.redirect("/history")


@app.route("/history")
def my_history_page():
    #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    #(out, err) = proc.communicate()
    #PATH=(out.split('\n'))[0]
    list = []
    app_key='4e3oofj6zqcx5dh'
    app_secret='vaoz96wg81222c9'
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
    file, metadata = client.get_file_and_metadata('/Shaked/History.txt')
    #file = open(PATH+"/users-folders/shaked/History.txt",'r')
    lines = file.readlines()
    file.close()
    for line in lines:
	if '=' in line:
		x = line.split("=")
                list.append(x)
		#title = x[0]
		#link = x[1]
		#titles.append(title)
		#links.append(link)
    return flask.render_template('my-history.html',list=list)

@app.route("/results/add_to_favorites/<LINE>",methods=['GET','POST'])
def addtofavorites(LINE):
	proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        PATH=(out.split('\n'))[0]
        #if "Remove" in flask.request.form:
        #LINE = flask.request.form['name']
        R_FILE = open(PATH+"/users-folders/shaked/Results.txt",'r')
        lines = NEWS_FILE.readlines()
        R_FILE.close()
	F_FILE = open(PATH+"/users-folders/shaked/Favorites.txt",'a')
        for line in lines:
                if LINE not in line:
                        R_FILE.write(line)
                else:
			F_FILE.write(line)
        R_FILE.close()
	F_FILE.close()
        return flask.redirect("/results")


@app.route("/favorites")
def my_archive_page():
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    PATH=(out.split('\n'))[0]
    list = []
    #F_FILE = open(PATH+"/users-folders/shaked/Favorites.txt",'r')
    app_key='4e3oofj6zqcx5dh'
    app_secret='vaoz96wg81222c9'
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
    F_FILE, metadata = client.get_file_and_metadata('/Shaked/Favorites.txt')
    lines = F_FILE.readlines()
    F_FILE.close()
    for line in lines:
        if '=' in line:
		x = line.split("=")
                list.append(x)
    return flask.render_template('my-favorites.html',list=list)

@app.route("/results")
def get_results():
        try:
                ebay()
                proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
                PATH=(out.split('\n'))[0]
                list = []
                #F_FILE = open(PATH+"/users-folders/shaked/Results.txt",'r')
                app_key='4e3oofj6zqcx5dh'
                app_secret='vaoz96wg81222c9'
                flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
                authorize_url = flow.start()
                client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
                F_FILE, metadata = client.get_file_and_metadata('/Shaked/Results.txt')
                lines = F_FILE.readlines()
                F_FILE.close()
                for line in lines:
                        if '=' in line:
                                x = line.split("=")
                                list.append(x)
                return flask.render_template('results.html',list=list)
        except:
                return flask.render_template('results.html',list=list)



@app.route("/favorites/delete/<LINE>",methods=['GET','POST'])
def favorite_delete(LINE):
        proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        PATH=(out.split('\n'))[0]
        #if "Remove" in flask.request.form:
        #LINE = flask.request.form['name']
        app_key='4e3oofj6zqcx5dh'
        app_secret='vaoz96wg81222c9'
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()
        client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
        file, metadata = client.get_file_and_metadata('/Shaked/History.txt')
        F_FILE = open(PATH+"/users-folders/shaked/Favorites.txt",'r')
        lines = F_FILE.readlines()
        F_FILE.close()
        F_FILE = open(PATH+"/users-folders/shaked/Favorites.txt",'w')
        for line in lines:
                if LINE not in line:
                        F_FILE.write(line)
                else:
                        continue
        F_FILE.close()
        F_FILE = open(PATH+"/users-folders/shaked/Favorites.txt",'r')
        F = F_FILE.read()
        F_FILE.close()
        response = client.put_file('/shaked/Favorites.txt', F,overwrite=True)
        return flask.redirect("/favorites")

@app.route("/history/delete/<LINE>",methods=['GET','POST'])
def history_delete(LINE):
	proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        PATH=(out.split('\n'))[0]
        #if "Remove" in flask.request.form:
        #LINE = flask.request.form['name']
        H_FILE = open(PATH+"/users-folders/shaked/History.txt",'r')
        lines = H_FILE.readlines()
        H_FILE.close()
        H_FILE = open(PATH+"/users-folders/shaked/History.txt",'w')
        for line in lines:
                if LINE not in line:
                        H_FILE.write(line)
                else:
                        continue
        H_FILE.close()
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

def ebay():
#Dropbox Connection
    app_key='4e3oofj6zqcx5dh'
    app_secret='vaoz96wg81222c9'
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')

### FILES
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    PATH=(out.split('\n'))[0]

    SEARCH_FILE, metadata = client.get_file_and_metadata('/Shaked/SearchFile.txt')
    KEYWORDS = SEARCH_FILE.read()
    SEARCH_FILE.close()
    print KEYWORDS
    RESULTS_FILE = open(PATH+'users-folders/shaked/Results.txt','w')
    HISTORY_FILE = open(PATH+'users-folders/shaked/History.txt','a')

### EBAY API
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

                RESULTS_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')
                HISTORY_FILE.write(TITLE+" = "+PRICE+" = "+SHIPPING_PRICE+" = "+URL+" = "+IMG+'\n')

            except:
                continue

        RESULTS_FILE.close()
        HISTORY_FILE.close()

        r_file=open("../users-folders/shaked/Results.txt",'r')
        r = r_file.read()
        response = client.put_file('/shaked/Results.txt', r,overwrite=True)

        h_file=open("../users-folders/shaked/History.txt",'r')
        h=h_file.read()
        response = client.put_file('/shaked/History.txt', h,overwrite=True)


    except ConnectionError as e:
        print(e)
        print(e.response.dict())

if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=1213, host="0.0.0.0", debug=True)

