#Import Libraries
from flask import Flask, request, render_template, send_file
from mongo import *
import pandas as pd
from datetime import datetime

app = Flask(__name__)
  
@app.route('/')
def load_homescreen():
    return render_template('home.html')

#When form is submitted
@app.route('/', methods=["POST"])

def fetch_price():
    #When "fetch" button is clicked to search some product ids
    if request.form["submit-btn"] == "fetch":

        #if input was blank then reload homescreen
        if request.form["pid"] == "":
            return render_template('home.html')
        
        #convert comma separated product ids into array
        #remove any spaces from input
        product_ids = request.form["pid"].replace(" ", "").split(",")
        results = fetchProductInfo(product_ids)
        
        #if any record for given input is present
        if len(list(results)):
            df = pd.DataFrame(list(results)) 
            del df["_id"]
            df = df.sort_values(['product_id', 'timestamp'], ascending=[True, False])
            print(df)
            return render_template('home.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
        
        #else reload home screen
        else:
            return render_template('home.html')

    #Fetch All info for all product ids
    elif request.form["submit-btn"] == "fetchAll" or request.form["submit-btn"] == "downloadCSV":
        results = fetchAll()

        if len(list(results)):
            df = pd.DataFrame(list(results)) 
            del df["_id"]
            df = df.sort_values(['product_id', 'timestamp'], ascending=[True, False])
            #display on app if "FETCH ALL" was selected
            if request.form["submit-btn"] == "fetchAll":
                return render_template('home.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
        
            #download csv
            elif request.form["submit-btn"] == "downloadCSV":
                filename = "scrapper_data.csv"
                df.to_csv(filename, header=True, index=False)
                return send_file(filename, as_attachment=True)
        else:
            return render_template('home.html')

#initialize app
if __name__ == '__main__':
   app.run()