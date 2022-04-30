from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import TED
import xml.etree.ElementTree as ET 
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'UploadedDocuments'
app.config['MAX_CONTENT_PATH'] = 1024

@app.route("/")
def home():
    return render_template("index.html")

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
        

        treeA = TED.preprocessing(ET.parse(path1).getroot())
        treeB = TED.preprocessing(ET.parse(path2).getroot())
        tedsim = TED.TED(treeA,treeB)
        vsmsim = VSM.VSM_xml(treeA,treeB)
    else:
        return render_template("compare.html", tedsim="")
    return render_template("compare.html",tedsim=tedsim)
    
@app.route("/search.html", methods = ['GET','POST'])
def search():
    if request.method == "POST":
        q = request.form['q']
        print(q)
    return render_template("search.html")
    
if __name__ == '__main__':
    app.run()    