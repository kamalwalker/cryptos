import urllib, json, pandas as pd, datetime, numpy as np, smtplib, locale, os.path as osp


def urlToDataFrame(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    df = pd.DataFrame(data)
    return df

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
    print message


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
    nbr_str = locale.format("%d",nbr,grouping=True)
    return nbr_str