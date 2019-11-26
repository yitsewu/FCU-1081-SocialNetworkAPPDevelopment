from flask import Flask, request, make_response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup


import requests, json, re, random

app = Flask(__name__)

class Counseling():
    def __init__(self, ID, Date, Name, Author, URL):
        self.N_ID = ID
        self.N_Date = Date
        self.N_Name = Name
        self.N_Author = Author
        self.N_URL = URL

All_Data = []

pagesize = 0

def get_All_Data():
    print('------------開始查詢------------')

    s = requests.Session()
    url = 'http://www.counseling.fcu.edu.tw/wSite/lp?ctNode=45441&mp=228101&idPath='

    # First get
    page = s.get(url)
    bs_page = BeautifulSoup(page.text, 'html.parser')
    pagesize= bs_page.find_all(attrs={"class":"page"})[0].select('em')[0].text

    # Fix url
    url = 'http://www.counseling.fcu.edu.tw/wSite/lp?ctNode=45441&mp=228101&idPath=&nowPage=1&pagesize=' + pagesize
    page = s.get(url)
    bs_page = BeautifulSoup(page.text, 'html.parser')
    table= bs_page.find(attrs={"summary":"諮商心聞報"})
    part = table.find_all('tr')

    for i in range(len(part)):
        try:
            news_name_re = re.compile(r'(\d\d\d)')

            news_name_span = news_name_re.search(part[i].find_all(attrs={"class":"title"})[0].find('a').text).span(0)

            news_date = part[i].find_all(attrs={"class":"date"})[0].text

            news_name_num = news_name_re.search(part[i].find_all(attrs={"class":"title"})[0].find('a').text).group()

            news_name = part[i].find_all(attrs={"class":"title"})[0].find('a').text[news_name_span[1] + 2 :].lstrip()

            news_author = part[i].find_all('td')[2].text[6:].lstrip().replace("　"," ").split(" ")[0].lstrip()
            
            if (part[i].find_all(attrs={"class":"title"})[0].find('a')['href'][0:2] == 'ct'):
                jump_url = 'http://www.counseling.fcu.edu.tw/wSite/' + part[i].find_all(attrs={"class":"title"})[0].find('a')['href']
                jump_page = s.get(jump_url)
                jump_page_bs_page = BeautifulSoup(jump_page.text, 'html.parser')
                news_url = 'http://www.counseling.fcu.edu.tw/wSite/' + jump_page_bs_page.find_all(attrs={"class":"download"})[0].find('a')['href']

            else:
                news_url = 'http://www.counseling.fcu.edu.tw/wSite/' + part[i].find_all(attrs={"class":"title"})[0].find('a')['href']

            TEMP = Counseling(news_name_num, news_date, news_name, news_author, news_url)
            All_Data.append(TEMP)
            
            print(TEMP.N_ID, TEMP)
        
        except:
            print()

    print('------------查詢結束------------')

    return pagesize

@app.route("/", methods=['GET'])
def index():
    return  render_template('index.html')

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
    return "Success!"

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True, port=8000)