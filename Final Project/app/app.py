# coding=utf-8
from GetAllData import get_All_Data, write_All_Data_CSV
from MoodAnalysis import Load, Jieba_Analysis, Remove_Sapce, WriteNewCsv, Get_segment_ordered
from flask import Flask, request, make_response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import json, re, random, jieba

app = Flask(__name__)

global segment_ordered
segment_ordered = Get_segment_ordered()

@app.route("/", methods=['GET'])
def index():
    return  render_template('./index.html')

def get_keyword(keyword):
    Url_list = ""

    for j in keyword:
        print(j)
        for i in segment_ordered:
            if j in i[5]:
                Url_list += i[2] + ' ' +  i[4]
                print(Url_list)

    if Url_list == "":
        print("ERROR")
        msg = '或許你可以去找諮商中心老師談談'
    else:
        msg = '或許 你可以看看這些文章：' + Url_list
    
    print(msg)
    
    return msg

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    # print(req)



    if req['queryResult']['parameters']['any'] != '':
        keyword = req['queryResult']['parameters']['any']
        
        print(keyword)
        
        jieba.load_userdict('dict.txt.big.txt')
        keyword = list(jieba.cut(keyword))
        print(keyword)

    res_message = {"fulfillmentText": get_keyword(keyword)}

    
    print(res_message)
    
    return make_response(jsonify(res_message))

@app.route("/update", methods=['GET'])
def update():
    get_All_Data()
    write_All_Data_CSV()
    Title = Load()
    segment_ordered = Jieba_Analysis(Title)
    WriteNewCsv(segment_ordered)
    return "Success!"

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True, port=8000)