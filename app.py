import collections
import time
from unittest import result
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from IR import KNN, IR_with_indexing, IR_without_indexing
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
            if filename1.endswith((".xml",".XML")) and filename2.endswith((".xml",".XML")):
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

    return render_template("compare.html", tedsim="-", vsmsim="-",vsmtime="-",tedtime="-")
    # return render_template("compare.html",tedsim=tedsim, vsmsim=vsmsim,vsmtime=vsmtime)

 # Search Engine   
@app.route("/search.html", methods = ['GET','POST'])
def search():
    if request.method == "POST":
        q = request.form['q']
        print(q)
        indexing = request.form.getlist("indexing")
        if(indexing):
            # !!! TODO CHANGE 1 TO INPUT FROM Front
            # method = int(request.form["options"])
            # print("METHOD: ",method)
            start = time.time()
            results = IR_with_indexing(q,1) or {}
            end = time.time()
            delay = end-start
            
            Knn = request.form['K']
            lenresults = len(results)
            nb = lenresults
            if Knn != "All":
                nb = int(Knn)

            lenresults = nb

            afterKNN = KNN(nb,results)
            keys = list(afterKNN.keys())
            filenames = [key.split("\\")[1] for key in keys]
            descriptions = [ET.parse(key).getroot().find(".//Description").text for key in keys]

            tr = dict(zip(filenames,descriptions))

           
            # tr = collections.OrderedDict(tr)
            return render_template("search.html",query=q,lenresults=lenresults,results=tr,time=delay,initial=results,directory="Documents\\",K=Knn)
        else:

            start = time.time()
            results = IR_without_indexing(q,1) or {}
            end = time.time()
            delay = end-start
            
            Knn = request.form['K']
            lenresults = len(results)
            nb = lenresults
            if Knn != "All":
                nb = int(Knn)

            lenresults = nb

            afterKNN = KNN(nb,results)
            keys = list(afterKNN.keys())
            filenames = [key.split("\\")[1] for key in keys]
            descriptions = []
            for key in keys:
                try:
                    descriptions.append(ET.parse(key).getroot().find(".//Description").text)
                except:
                    descriptions.append("No Description")

            tr = dict(zip(filenames,descriptions))

            
            return render_template("search.html", query=q,lenresults=lenresults,results=tr,time=delay,initial=results,directory="Documents\\")
    else:
        return render_template("search.html",query="",lenresults=0,results={},time="")
    

@app.route("/Documents/<filename>")
def getfile(filename):
    return send_file(os.path.join("Documents",filename))

@app.route("/Speak",methods=["GET","POST"])
def speak():
    if request.method == "POST":
        print("WORKINGGGG")
    return "Clicked"

if __name__ == '__main__':
    app.run()    