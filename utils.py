import urllib, json, pandas as pd, datetime, numpy as np, smtplib, locale, os.path as osp, requests, lxml

class DataRequester:
    def __init__(self):
        self.session = getSession()

    def getUrlResponse(self, url, parameters):
        response = self.session.get(url, params=parameters)
        data = json.loads(response.text)
        return data

    def getAllData(self, limit=200, start=1, convert='USD'):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': start,
            'limit': limit,
            'convert': convert
            }
        return getUrlResponse(url, parameters)




def getSession():
    from requests import Request, Session
    from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
    import json

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



def urlToDataFrame(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    df = pd.DataFrame(data)
    return df




#################################################

def getMarkets(ticker):
    url  = "https://coinmarketcap.com/currencies/{}/#markets".format(ticker)
    df = urlToDataFrame(url)
    return df

def getActualData(ticker='',limit=0):
    url = "https://api.coinmarketcap.com/v1/ticker/{}/?limit={}".format(ticker,limit)
    df = urlToDataFrame(url)
    return df

def getAllTickers(limit):
    df = getActualData(ticker='',limit=limit)
    return df.id.values

def getAllMarkets(ticker):
    url = "https://coinmarketcap.com/currencies/{}/#markets".format(ticker)
    df = urlToDataFrame(url)
    return df

def getHistoricalData(ticker,startDate,endDate):

    url = "https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}".format(ticker,startDate,endDate)
    import ipdb; ipdb.set_trace()
    result = pd.read_html(url)
    df = result[0]
    return df

def getNowStr():
    return datetime.datetime.now().strftime('%Y:%m:%d:%H.%M.%S')


def getToday(deltaTime):
    today = datetime.datetime.today()
    date = today + datetime.timedelta(days=deltaTime)
    todayStr = date.strftime('%Y%m%d')
    return todayStr

def jlog(message):
    print(message)


def sendMail(message,df_file):
    fromMail = "pythonalertkf@gmail.com"
    password = "jamila111"
    for toMail in ["kamalfaik@gmail.com","mohamedfaik@gmail.com"]:
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
   # url, params = getAllDataUrlAndParams()
   # response = getUrlResponse(url, params)
    response = getHistoricalData("BTC","20200101", "20200103")