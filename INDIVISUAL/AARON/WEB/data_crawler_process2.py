# -*- coding: utf-8 -*-
from __future__ import division
import time, requests
from multiprocessing import Process , Queue, current_process
import Queue as kueue
import pandas as pd
from bs4 import BeautifulSoup

from data_handler2 import DataHandler
from data_utils import ClsCommon


class DataCrawler(Process):
    '''
        0. multi process로 작동되는 데이터크롤러임, 웹페이지의 많은 값을 데이터베이스화 하기위해서 시도
        1. 크롤링 하고자 하는 주식코드 리스트를 파라미터로 받음
        2. 웹페이지의 url을 파싱해서 해당 코드의 전체기간의 주식가격 정보를 dataframe으로 만듬
        3. stock dataframe -> insert database , code의 수많큼 만복
    '''
    def __init__(self, codes, wait_sec=5):
        super(DataCrawler, self).__init__()
        self.wait_sec = wait_sec
        self.codes = codes
        self.dbhandler = DataHandler()
        self.clscommon = ClsCommon()
        self.procname = None


    def run(self):

        stock_code = None
        self.procname = current_process().name

        while True:
            try:
                stock_code = self.codes.get_nowait()
                print stock_code, ' is processing by ', self.procname
                if stock_code:
                    data_count, last_date = self.dbhandler.getdatacount2(stock_code)
                    df_data = self.downloadfromdaum(stock_code, last_date)
                    #df_data = None
                    if df_data is not None:
                        df_data_indexed = df_data.reset_index()
                        self.dbhandler.updatepricetodb(stock_code, df_data_indexed)

            except kueue.Empty:
                print ">>> there is no job in queue by %s <<<" % self.procname
                break
            except Exception as error:
                print ">>> while do_job, error happen !! %s " % self.procname
                print error
                self.codes.put(stock_code)
                continue
            else:
                print stock_code, ' is done by ', self.procname
        return True


    def downloadfromdaum(self, stock_code, last_date):
        pageno = 1
        _date = []
        _open = []
        _high = []
        _low = []
        _close = []
        _adj_Close = []
        _volume = []
        go = True
        _count = 1
        if last_date == 0:
            last_date = pd.to_datetime('1900.01.01', format='%Y.%m.%d')
        while go:
            try:
                print 'page : ', pageno
                url = "http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page=%s&code=%s&modify=1" % (
                pageno, stock_code)
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                if len(soup) == 0:
                    return None
                table = soup.find("table", {"id": "bbsList"})
                if len(table.select('tr')) <= 2:
                    break
                for tr in table.select('tr'):
                    try:
                        if (tr["onmouseout"] == None):
                            continue
                        cols = tr.select('td')
                        datefromwebsite = cols[0].get_text("|", strip=True)
                        trandatefromwebsite = pd.to_datetime(datefromwebsite, format='%y.%m.%d')
                        # trandatefromwebsite = pd.to_datetime(datefromwebsite).isoformat()
                        print _count, trandatefromwebsite, last_date
                        if trandatefromwebsite <= last_date:
                            print 'trandatefromwebsite is ', trandatefromwebsite
                            print ''
                            print 'last_date is ', last_date
                            go = False
                            break
                        _date.append(datefromwebsite)
                        _open.append(self.clscommon.fNormalNumberText(cols[1].get_text("|", strip=True)))
                        _high.append(self.clscommon.fNormalNumberText(cols[2].get_text("|", strip=True)))
                        _low.append(self.clscommon.fNormalNumberText(cols[3].get_text("|", strip=True)))
                        _close.append(self.clscommon.fNormalNumberText(cols[4].get_text("|", strip=True)))
                        _adj_Close.append(self.clscommon.fNormalNumberText(cols[4].get_text("|", strip=True)))
                        _volume.append(self.clscommon.fNormalNumberText(cols[7].get_text("|", strip=True)))
                        _count += 1
                    except Exception as error:
                        continue
            except Exception as error:
                print "while downloadfromdaum error: >>> ", error
                return None
            pageno += 1
            time.sleep(0.6)
        data = {"Date": _date, "Open": _open, "High": _high, "Low": _low, "Close": _close, "Adj Close": _adj_Close,
                "Volume": _volume}
        df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'], format='%y.%m.%d')
        df = df.dropna(subset=['Close'])
        df = df.set_index('Date')

        print df.shape

        return df


def makesplitlist(seq, size):
    avg = len(seq) / float(size)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


def updateastockpriceall(code):
    start_time = time.time()
    dbhandler = DataHandler()
    rows = dbhandler.deletestockdata(code)
    tasks_to_accomplish = Queue()
    tasks_to_accomplish.put(code)
    process = DataCrawler(tasks_to_accomplish)
    process.start()
    process.join()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time, 'seconds has been elasped')
    print('Processing is done !')

def updateallstockprices():
    start_time = time.time()

    processes = []

    number_of_processes = 4
    dbhandler = DataHandler()
    rows = dbhandler.getstockdata()
    tasks_to_accomplish = Queue()
    # tasks_to_accomplish.put('005930')
    for a_row in rows:
        stock_code = a_row[0]
        tasks_to_accomplish.put(stock_code)

    # split_stock_codes = makesplitlist(codes, nsplit_stock)
    # split_count = len(split_stock_codes)
    for _ in range(number_of_processes):
        process = DataCrawler(tasks_to_accomplish)
        processes.append(process)
        process.start()

    for mp in processes:
        mp.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time, 'seconds has been elasped')
    print('Processing is done !')


if __name__ == '__main__':
    updateallstockprices()
    # updateastockpriceall('220180')
