# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import threading
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import redis

sem = threading.Semaphore(32)

# 네이버 api 요청에 필요한 key값들
client_id = "UbnTvKWo8Yy8yYceCH5c"
client_secret = "lvimNp879q"

# 검색어
searchText = "성장 자유 이해 정신 희망 지혜 영혼 문화 시설 봉사 종교 여가 환경"
#            "보험 연금 의료 돈 은퇴 사람 가족 관계 일 사회 교육 복지 지원 정책"
#            "계획 설계 준비 건강 성격 암 스포츠 운동 치매 질병 행복 사랑 꿈"
#            "성장 자유 이해 정신 희망 지혜 영혼 문화 시설 봉사 종교 여가 환경"

r = redis.StrictRedis(host='ec2-13-124-148-252.ap-northeast-2.compute.amazonaws.com', port=6379, db=12)


def search_by_naver(start, query):
    encText = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/blog?display=100&start=" + str(
        start) + "&sort=sim&query=" + encText  # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, timeout=30)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        return response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)
        return ''



class ReadContents(threading.Thread):
    def __init__(self, link, postdate, search_engine):
        super(ReadContents, self).__init__()
        self.link = link
        self.postdate = postdate
        self.search_engine = search_engine

    def run(self):
        sem.acquire()
        read_contents(self.link, self.postdate, self.search_engine)
        sem.release()


def read_contents(link, postdate, search_engine):
    driver = webdriver.PhantomJS(r'C:/sdk/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    ret = ''
    try:
        driver.get(link)
        print(driver.page_source)
        driver.switch_to.default_content()
        # 블로그
        if not link.find('blog.naver.com') == -1:
            driver.switch_to.frame("mainFrame")
            page = driver.page_source
            # print(page)
            soup = BeautifulSoup(page, 'html.parser')
            contents = soup.select_one('#postViewArea')
            if not contents:
                contents = soup.select_one('.se_doc_viewer')
            for string in contents.stripped_strings:
                ret += repr(string)
            ret = ret.replace('\\xa0', ' ').replace('\\r\\n', ' ').replace('\'', '').replace('esports', '이스포츠')
            if not ret == '':
                print(ret)
                if postdate is not None:
                    create_item(link, search_engine, postdate, ret)
       
    except Exception as e:
        print(e)
    driver.quit()


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y%m%d')
        return True
    except ValueError:
        return False


def create_item(site_link, from_search_engine, publish_date, contents):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    if not validate_date(publish_date):
        news_pub_day = datetime.datetime.strptime(publish_date, '%a, %d %b %Y %H:%M:%S %z').timestamp()
        publish_date = datetime.datetime.fromtimestamp(news_pub_day).strftime('%Y%m%d')

    r.set(site_link, {
        'site_link': site_link,
        'search_text': searchText,
        'from_search_engine': from_search_engine,
        'publish_date': publish_date,
        'contents': contents,
        'reg_date': st
    })


for start in range(0, 11):
    print(start * 100)
    if start == 0:
        start = 1
    else:
        start = start * 100

    resp = search_by_naver(start, searchText)
    if resp:
        j = json.loads(resp)
        for item in j["items"]:
            redirect = str(item["link"]).replace("?Redirect=Log&amp;logNo=", "/")
            if not redirect.find('blog.naver.com') == -1:
                print(redirect)
                t = ReadContents(redirect, item["postdate"], 'naver-blog')
                t.start()

 