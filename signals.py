import datetime
import numpy as np
import os.path as osp
import pandas as pd

import utils



def checkVolumeSpike(ticker ,hist,actual):

    stdParam = 3
    minVolumeParam = 5e6
    recentIncreasingPeriod = 3
    historyDays = 20

    volumes = hist.Volume.values[::-1]

    volumes20 = volumes[-historyDays:]
    recentIncrease = np.diff(volumes[recentIncreasingPeriod:])

    average = np.percentile(volumes20, [50])[0]
    stdDev = np.std(volumes20)
    lastVolume = float(actual["24h_volume_usd"].values[0])

    #conditions definitions
    lastVolumeSpike  =  lastVolume > average + stdParam*stdDev
    #recentIncreasingVolume  = np.all(recentIncrease> 0)
    minVolumeTraded = lastVolume > minVolumeParam

    whatToCheck  = lastVolumeSpike and minVolumeTraded #and recentIncreasingVolume
    if whatToCheck :

        perf_1h = actual.get('percent_change_1h').values[0]
        if not perf_1h:
            perf_1h = 0
        perf_24h = actual.get('percent_change_24h').values[0]
        if not perf_24h:
            perf_24h = 0
        perf_7d = actual.get('percent_change_7d').values[0]
        if not perf_7d:
            perf_7d = 0

        utils.jlog('spotted {}'.format(ticker.upper()))
        message  = "Ticker:  {}  ".format(ticker.upper())
        message += "\n * market Cap {} ".format(utils.formatMillions(float(actual['market_cap_usd'].values[0])))
        message += "\n * Volume last 24 h {}".format(utils.formatMillions(lastVolume))
        message += "\n * average {}".format(utils.formatMillions(average))
        message += "\n * stdDev {}".format(utils.formatMillions(stdDev))
        message += "\n * ratio  volume / marketCap  {}".format(float(lastVolume/float(actual['market_cap_usd'].values[0])*100.))
        message += "\n"
        message += "\n * return last  1 h {} %".format(float(perf_1h))
        message += "\n * return last 24 h {} %".format(float(perf_24h))
        message += "\n * return last  7 d {} %".format(float(perf_7d))
        message += "\n"

        message += "\n * volume exploding on {}  last 24 h Volume {}  while average was {}".format(ticker, utils.formatMillions(lastVolume),
                                                                                                   utils.formatMillions(average))
        message += "\n * historical volumes and last volume  : \n *** {}".format(" -- ".join([utils.formatMillions(vv) for vv in volumes20]))
        message += "\n * conditions triggered are: "
        message += "\n **** volume 24h > avg(20 days volume) + {} * stdDev  ".format(stdParam)
        message += "\n **** and volume_last_24h  > {}".format(utils.formatMillions(minVolumeParam))
        #message += "\n **** and last {} days saw increasing volume".format(recentIncreasingPeriod)
        message += "\n\n\n"
        actual['ticker'] = ticker
        return {'ticker': ticker, 'message': message, 'dataFrame': actual}
    else:
        return None


def checkTicker(ticker,startDate,endDate):
    hist = utils.getHistoricalData(ticker, startDate, endDate)
    actual = utils.getActualData(ticker)
    result      = checkVolumeSpike(ticker, hist, actual)
    return   result

#
####### SIGNALS ########

def getHighestVolumeChanges(limit=200):
    # get all listings now 
    # get all the ones that have the biggest volume increase
    # with marketCap > minMarketCap
    # with volume > minVolume
    dr = utils.DataRequester()
    data = dr.getAllData(limit=limit)
    dfRows = []
    for uData in data:
    
        ticker = uData['symbol']
        qData = uData['quote']['USD']
        items = qData.items()
        items.sort(key = lambda item: item[0])
        keys = [it[0] for it in items]
        values = [ticker] + [it[1] for it in items]
        dfRows.append(values)

    df = pd.DataFrame(dfRows, columns= ['ticker'] + keys)
    return df         

def getAllTimeWinners(limit=200):
    # return tickers that were positive for all percentage returns in coinmarketCap quotes data
    df = getHighestVolumeChanges(limit=limit)
    retCols = [col for col in df.columns if 'percent' in col]
    mask = np.all(np.array([df[col] >0 for col in retCols]), axis=0)
    return df[mask]

def getSpikeVolumeTickersAndSendMail():

    allTickers = utils.getAllTickers(limit=200)
    startDate = utils.getToday(-20)
    endDate = utils.getToday(0)
    results = []
    for ticker in allTickers:
        result = checkTicker(ticker,startDate,endDate)
        if result:
            results += [result]
    dataFrames = []
    newTickers = []
    spottedTickers = [result['ticker'] for result in results]

    dataFrames += [result['dataFrame'] for result in results]

    df = pd.concat(dataFrames)
    now = datetime.datetime.now().strftime('%Y:%m:%d:%H.%M.%S')
    df['timeStr'] = now
#    df_file = '/Users/kamalfaik/pyCharmProjects/coinMarketCap/df_file_test.csv'
    df_file = "/Users/kamalfaik/Google Drive/Business/bitcoin/coinmarketcap/df_file.csv"
    if osp.exists(df_file):
        df_history = pd.read_csv(df_file)
        newTickers = [ticker for ticker in spottedTickers if ticker not in df_history.ticker.values]
        df_all = pd.concat([df_history,df])
    else:
        df_all = df
    df_all.to_csv(df_file,index=False)

    header = ['NEW SPOTTED CRYPTOS']
    message = []
    newResults = [result for result in results if result['ticker'] in newTickers]
    if len(newResults) > 0:
        for result in newResults:
            header += [result['ticker']]
            message += [result['ticker']]
            message += [result['message']]
        messageToSend = " ".join(header) + '\n' + '\n'.join(message)
        utils.sendMail(messageToSend, df_file)
    else:
        print('nothing to send {}'.format(now))



if __name__ == "__main__":
    pass