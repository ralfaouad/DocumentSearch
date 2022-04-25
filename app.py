from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search.html", methods = ['GET','POST'])
def search():
    if request.method == "POST":
        q = request.form['q']
        print(q)
    return render_template("search.html")
    
if __name__ == '__main__':
    app.run()    