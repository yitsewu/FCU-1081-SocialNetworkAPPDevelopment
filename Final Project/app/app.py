from GetAllData import get_All_Data, write_All_Data_CSV
from flask import Flask, request, make_response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

import json, re, random

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return  render_template('./index.html')

def get_keyword(keyword):    
    if keyword == '難過' or keyword == '傷心' or keyword == '壓力' or keyword == '自殺':
        print("success")
        rand = random.randrange(426)
        msg = '看看由' + All_Data[rand].N_Author + '\n推薦的' + All_Data[rand].N_Name + '\n' + All_Data[rand].N_URL
    else:
        print("ERROR")
        msg = '或許你可以去找諮商中心老師談談'
    
    return msg

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print(req)

    if req['queryResult']['parameters']['any'] != '':
        keyword = req['queryResult']['parameters']['any']
        print(keyword)

    res_message = {"fulfillmentText": get_keyword(keyword)}

    print(res_message)
    
    return make_response(jsonify(res_message))

@app.route("/update", methods=['GET'])
def update():
    get_All_Data()
    write_All_Data_CSV()
    return "Success!"

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True, port=8000)