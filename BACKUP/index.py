
### This Web-App Created BY SHAKED BRAIMOK ###
####### APP NAME: My-News #######

import flask
import os
import functools


app = flask.Flask(__name__)


@app.route("/")
def start():
	return flask.render_template('index.html')

@app.route("/login")
def main():
    if "username" in flask.session:
        return flask.redirect("/my_news")
    return flask.render_template('login-index.html')

@app.route("/loading", methods=['get', 'post'])
def login():
    if "username" in flask.request.form:
        if "password" in flask.request.form and flask.request.form['username'] == "shaked" and flask.request.form['password'] == "1213123":
            flask.session['username'] = "shaked"

            return flask.redirect("/")
        else:
            return "BAD USERNAME OR PASSWROD! PLEASE TRY AGAIN!"
    else:
        return flask.redirect("/login")



def check_login(func):
    def wrapper(*args, **kwargs):
        if "username" in flask.session:
            return func(*args, **kwargs)
        else:
            return flask.redirect("/login")
    return functools.update_wrapper(wrapper, func)


@app.route("/my_dandash")
@check_login
def profile():
	username = flask.session['username']
	return flask.render_template('my-dandash.html')

@app.route("/dandash_world")
@check_login
def world():
	username = flask.session['username']
	return flask.render_template('dandash-world.html')
@app.route("/my_news")
@check_login
def my_news():
    username = flask.session['username']
   # os.mkdir("/app/users-folders/"+username)
   # my_list = open("/app/users-folders/"+username+"/my_list.txt","a")
   # my_list.close()
   # my_history = open("/app/users-folders/"+username+"/my_history.txt","a")
   # my_history.close()
    return "Welcome %s!<br><a href=\"/logout\">Logout</a>" % flask.session['username']

@app.route("/my_list_page")
@check_login
def my_list_page():
    username = flask.session['username']
    file = open("users-folders/"+username+"/my-list",'r')
    lines = file.readlines()
    return flask.render_template('my-list.html',lines=lines)

@app.route("/my_list_page/appending",methods=['GET', 'POST'])
@check_login
def append():
	if "add" in flask.request.form:
		#data = str(flask.request.data)
		text = flask.request.form['add']
    		processed_text = text.upper()
		file = open("users-folders/shaked/my-list",'a')
		file.write(processed_text+'\n')
		file.close()
		return flask.redirect("/my_list_page")
		
@app.route("/my_list_page/remove/<LINE>",methods=['GET','POST'])
@check_login
def remove(LINE):
	#if "Remove" in flask.request.form:
	#LINE = flask.request.form['name']
        username = flask.session['username']
        LIST_FILE = open("users-folders/"+username+"/my-list",'r')
        lines = LIST_FILE.readlines()
	LIST_FILE.close()
	LIST_FILE = open("users-folders/"+username+"/my-list",'w')
        for line in lines:
        	if LINE not in line:
			LIST_FILE.write(line)
		else:
			continue	
	LIST_FILE.close()
        return flask.redirect("/my_list_page")
	



@app.route("/my_news_page")
@check_login
def my_history_page():
    list = []
    username = flask.session['username']
    file = open("users-folders/"+username+"/my-news",'r')
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
    return flask.render_template('my-news.html',list=list)

@app.route("/my_news_page/archive/<LINE>",methods=['GET','POST'])
@check_login
def archive(LINE):
        #if "Remove" in flask.request.form:
        #LINE = flask.request.form['name']
        username = flask.session['username']
        NEWS_FILE = open("users-folders/"+username+"/my-news",'r')
        lines = NEWS_FILE.readlines()
        NEWS_FILE.close()
        NEWS_FILE = open("users-folders/"+username+"/my-news",'w')
	ARCHIVE_FILE = open("users-folders/"+username+"/my-archive",'a')
        for line in lines:
                if LINE not in line:
                        NEWS_FILE.write(line)
                else:
			ARCHIVE_FILE.write(line)
        NEWS_FILE.close()
	ARCHIVE_FILE.close()
        return flask.redirect("/my_news_page")


@app.route("/my_archive_page")
@check_login
def my_archive_page():
    list = []
    username = flask.session['username']
    ARCHIVE_FILE = open("users-folders/"+username+"/my-archive",'r')
    lines = ARCHIVE_FILE.readlines()	
    ARCHIVE_FILE.close()
    for line in lines:
        if '=' in line:
		x = line.split("=")
                list.append(x)
    return flask.render_template('my-archive.html',list=list)

@app.route("/my_archive_page/delete/<LINE>",methods=['GET','POST'])
@check_login
def delete(LINE):
        #if "Remove" in flask.request.form:
        #LINE = flask.request.form['name']
        username = flask.session['username']
        ARCHIVE_FILE = open("users-folders/"+username+"/my-archive",'r')
        lines = ARCHIVE_FILE.readlines()
        ARCHIVE_FILE.close()
        ARCHIVE_FILE = open("users-folders/"+username+"/my-archive",'w')
        for line in lines:
                if LINE not in line:
                        ARCHIVE_FILE.write(line)
                else:
			continue
        ARCHIVE_FILE.close()
        return flask.redirect("/my_archive_page")

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

@app.route("/contact")
def my_contact():
	return flask.render_template('contact.html')

@app.route("/logout")
def logout():
    if "username" in flask.session:
        del flask.session["username"]
    return flask.redirect("/")


if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=8080, host="0.0.0.0", debug=True)

