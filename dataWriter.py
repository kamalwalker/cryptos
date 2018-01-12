import datetime
import os.path as osp
import pandas as pd
import time

import utils


def main(fileName):
    ## get actual data on all coinMarketCap
    ## apppend the dataFrame to existing historical dataFrame
    timeStr = datetime.datetime.now().strftime('%Y:%m:%d:%H.%M.%S')
    timeUnix = time.time()
    df = utils.getActualData(ticker='', limit=200)
    df['timeStr']   = timeStr
    df['timeUnix']  = timeUnix

    if osp.exists(fileName):
        df_histo = pd.read_csv(fileName)
        df_all = pd.concat([df_histo,df])
    else:
        df_all = df
    df_all.to_csv(fileName)



if __name__ == '__main__':
    fileName = "/Users/kamalfaik/Google Drive/Business/bitcoin/coinmarketcap/historicalData_coins_200_snap_300.csv"
    main(fileName)
