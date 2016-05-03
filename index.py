
### This Web-App Created BY SHAKED BRAIMOK ###
####### APP NAME: Dinero #######

import os
import flask
import subprocess

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
	proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    	(out, err) = proc.communicate()
	PATH=(out.split('\n'))[0]
	if "add" in flask.request.form:
		#data = str(flask.request.data)
		text = flask.request.form['add']
    		processed_text = text.upper()
		file = open(PATH+"/users-folders/shaked/SearchFile.txt",'w')
		file.write(processed_text)
		file.close()

	if "add2" in flask.request.form:
		text = flask.request.form['add2']
                processed_text = text.upper()
                file = open(PATH+"/users-folders/shaked/SearchFile.txt",'a')
                file.write(";"+processed_text)
                file.close()
	os.system("python "+PATH+"/Dinero-System-Scripts/ebay.py")
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
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    PATH=(out.split('\n'))[0]
    list = []
    file = open(PATH+"/users-folders/shaked/History.txt",'r')
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
    F_FILE = open(PATH+"/users-folders/shaked/Favorites.txt",'r')
    lines = F_FILE.readlines()	
    F_FILE.close()
    for line in lines:
        if '=' in line:
		x = line.split("=")
                list.append(x)
    return flask.render_template('my-favorites.html',list=list)


@app.route("/results")
def my_archive_page2():
    proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    PATH=(out.split('\n'))[0]
    list = []
    F_FILE = open(PATH+"/users-folders/shaked/Results.txt",'r')
    lines = F_FILE.readlines()
    F_FILE.close()
    for line in lines:
        if '=' in line:
                x = line.split("=")
                list.append(x)
    return flask.render_template('results.html',list=list)



@app.route("/favorites/delete/<LINE>",methods=['GET','POST'])
def favorite_delete(LINE):
	proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        PATH=(out.split('\n'))[0]
        #if "Remove" in flask.request.form:
        #LINE = flask.request.form['name']
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


if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=8090, host="0.0.0.0", debug=True)

