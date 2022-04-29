from __future__ import print_function # In python 2.7
from flask import Flask, render_template , request
from reviews import find_amazon_data_ruku,ruku_likn_de
import sys


app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template ("home.html")


@app.route("/result" , methods= ["POST" ,"GET"])
def ruku():
    if request.method=="POST":
        
        a = request.form["link"]
        if a != "":
            a   = ruku_likn_de(a)
            matas = 0
            
            return render_template("results.html", a = a , matas = matas , )
        else:
            matas = 100   
            return render_template("results.html" , matas = matas)
    matas = 100 
    return render_template("results.html" , matas = matas)
    

    


if __name__ == "__main__":
    app.run( use_reloader = True, debug=True)