from bs4 import BeautifulSoup
import requests
import re

class Counseling():
    def __init__(self, ID, Date, Name, Author, URL):
        self.N_ID = ID
        self.N_Date = Date
        self.N_Name = Name
        self.N_Author = Author
        self.N_URL = URL


def get_All_Data():
    All_Data = []

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
            
            print(TEMP)

            All_Data.append(TEMP)

        except:
            print()

    return All_Data

print(get_All_Data())