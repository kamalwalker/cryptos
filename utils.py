import urllib, json, pandas as pd, datetime, numpy as np, smtplib, locale, os.path as osp, requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class DataRequester:
    MAIN_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/{}/latest' 
    def __init__(self):
        self.session = getSession()

    def getUrlResponse(self, url, parameters):
        response = self.session.get(url, params=parameters)
        data = json.loads(response.text)['data']
        return data

    def getAllData(self, limit=200, start=1, convert='USD'):
        url = self.MAIN_URL.format("listings")# quotes and market-pairs instead of listings
        parameters = {
            'start': start,
            'limit': limit,
            'convert': convert
            }
        return self.getUrlResponse(url, parameters)

    def getQuotes(self, tickers):
        #TODO : debug
        url = self.MAIN_URL.format(",".join(tickers)) 
        parameters = {"symbol":tickers}
        return self.getUrlResponse(url ,parameters)


def getSession():

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '627d61db-1eb0-4c3b-a77f-9bf3eb856b32',

    }

    session = Session()
    session.headers.update(headers)
    return session

def getUrlResponse(url, parameters, session=None):
    try:
        session = session or getSession()
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return data


def urlToDataFrame(url, parameters=None):
    data = getUrlResponse(url, parameters=parameters)
    df = pd.DataFrame(data)
    return df


#################################################
## TODO: it seems all those lines below 
def getMarkets(ticker):
    url  = "https://coinmarketcap.com/currencies/{}/#markets".format(ticker)
    return urlToDataFrame(url) 

def getActualData(ticker='',limit=0):
    url = "https://api.coinmarketcap.com/v1/ticker/{}/?limit={}".format(ticker,limit)
    return urlToDataFrame(url)

def getAllTickers(limit):
    df = getActualData(ticker='',limit=limit)
    return df.id.values

def getAllMarkets(ticker):
    url = "https://coinmarketcap.com/currencies/{}/#markets".format(ticker)
    return urlToDataFrame(url) 

def getHistoricalData(ticker,startDate,endDate):

    url = "https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}".format(ticker,startDate,endDate)
    #result = pd.read_html(url)
    #df = result[0]
    #return df
    return urlToDataFrame(url) 

#############

def getNowStr():
    return datetime.datetime.now().strftime('%Y:%m:%d:%H.%M.%S')


def getToday(deltaTime):
    today = datetime.datetime.today()
    date = today + datetime.timedelta(days=deltaTime)
    todayStr = date.strftime('%Y%m%d')
    return todayStr

def jlog(message):
    print(message)


def sendMail(message):
    fromMail = "pythonalertkf@gmail.com"
    password = "jamila111"
    for toMail in ["kamalfaik@gmail.com"]:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromMail, password)
        server.sendmail(fromMail,toMail,message)
        server.quit()

def removeDuplicates(iter):
    return list(set(iter))

def formatMillions(nbr):
    locale.setlocale(locale.LC_ALL,'en_US')
    nbr_str = locale.format_string("%d",nbr,grouping=True)
    return nbr_str

if __name__ == "__main__":
    pass
    #url, params = getAllDataUrlAndParams()
    #response = getUrlResponse(url, params)
    #response = getHistoricalData("BTC","20200101", "20200103")