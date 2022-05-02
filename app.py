# from isort import file
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import TED, VSM
import xml.etree.ElementTree as ET 
import os

# Configurations
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'UploadedDocuments'
app.config['MAX_CONTENT_PATH'] = 1024

# Main Page
@app.route("/")
def home():
    return render_template("index.html")


# TED and VSM Comparison Tool
@app.route("/compare.html", methods = ["GET","POST"])
def compare():
    if request.method == "POST":
        file1 = request.files['in1']
        if file1:
            filename1 = secure_filename(file1.filename)
            path1 = os.path.join(app.config['UPLOAD_FOLDER'],filename1)
            file1.save(path1)
        file2 = request.files['in2']
        if file2:
            filename2 = secure_filename(file2.filename)
            path2 = os.path.join(app.config['UPLOAD_FOLDER'],filename2)
            file2.save(path2)

        # Text Comparison
        if filename1.endswith(".txt") and filename2.endswith(".txt"):
            with open(path1,"r") as f1:
               str1 =  f1.read()
            with open(path2,"r") as f2:
               str2 =  f2.read()
            weight = int(request.form['i'])
            sim = int(request.form['m'])
            start = time.time()
            vsmsim = VSM.VSM_txt(str1,str2,[path1,path2],weight,sim)
            end = time.time()
            vsmtime = end-start
            return render_template("compare.html", tedsim="",vsmsim=vsmsim,vsmtime=vsmtime)

        # XML Comparison
        else:
            if filename1.endswith(".xml") and filename2.endswith(".xml"):
                with open(path1,"r") as f1:
                    str1 =  f1.read()
                with open(path2,"r") as f2:
                    str2 =  f2.read()
                weight = int(request.form['i'])
                sim = int(request.form['m'])
                # TED Approach
                startTED = time.time()
                treeA = TED.preprocessing(ET.parse(path1).getroot())
                treeB = TED.preprocessing(ET.parse(path2).getroot())
                tedsim = TED.TED(treeA,treeB)
                endTED=time.time()
                tedtime = endTED-startTED

                # VSM Approach
                startvsm = time.time()
                vsmsim = VSM.VSM_xml(treeA, treeB, [path1,path2], weight, sim)
                endvsm = time.time()
                vsmtime = endvsm-startvsm
                return render_template("compare.html", tedsim=tedsim,vsmsim=vsmsim,vsmtime=vsmtime,tedtime=tedtime)
    else:
        return render_template("compare.html", tedsim="", vsmsim="",vsmtime="",tedtime="")
    return render_template("compare.html",tedsim=tedsim, vsmsim=vsmsim,vsmtime=vsmtime)

 # Search Engine   
@app.route("/search.html", methods = ['GET','POST'])
def search():
    if request.method == "POST":
        q = request.form['q']
        print(q)
    return render_template("search.html")
    
if __name__ == '__main__':
    app.run()    