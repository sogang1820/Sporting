
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains



from pymongo import MongoClient
# import pyperclip

# #import pyautogui


# #import chromedriver_autoinstaller

# import urllib
# from bs4 import BeautifulSoup
# import cfscrape
import re, time
import datetime 
# from multiprocessing import Lock
# from storage_handler import StorageHandler
# from scraper import Scraper

# import requests, argparse, json
import lxml.html
# import io


# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser


# ####youtube live 스트리밍 
# import sys
# import pyperclip

# import random


# import uuid
# import rsa
# import lzstring
# from urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter
# from file_handler import FileHandler







from bs4 import BeautifulSoup
# import cfscrape
# import re, time
# import datetime 
# from multiprocessing import Lock
# from storage_handler import StorageHandler
# from scraper import scraper

import requests, argparse, json
# import lxml.html
# import io


# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser

import os
from pymongo import MongoClient
from dotenv import load_dotenv


# collection.remove({})
class DB:
    def initialize(self):
        load_dotenv()
        MONGODB_URL = os.getenv("MONGODB_URL")
        DATABASE_NAME = os.getenv("DATABASE_NAME")

        client = MongoClient(MONGODB_URL)

        print(client.list_database_names())

        db = client['SportingDB']

        print(db)
        collection = db['stadiums']
        print(collection)
        return collection


class CrawlingHandler :

    def time_calc(self, start_time, op_hour):
        hour = start_time[:2]
        minute = start_time[4:6]
        start = hour +':'+minute    

        hour = int(hour)
        minute = int(minute)
        if len(op_hour)<=3:
            plus_hour = int(op_hour[0])
            plus_minute = 0
        else:
            plus_hour = int(op_hour[0])
            plus_minute = int(op_hour[3:5])
        
        hour += plus_hour
        minute += plus_minute
        if minute >= 60:
            minute -= 60
            hour+=1
        end = str(hour)+':'+str(minute)

        return start, end
    
    def parse_info(self,info):
        date = info[:12]
        start = info[13:18]
        end = info[19:24]

        return date,start,end
    
    # def db(self):
    #     load_dotenv()
    #     MONGODB_URL = os.getenv("MONGODB_URL")
    #     DATABASE_NAME = os.getenv("DATABASE_NAME")

    #     client = MongoClient(MONGODB_URL)

    #     print(client.list_database_names())

    #     db = client['SportingDB']

    #     print(db)
    #     collection = db['Stadium']
    #     print(collection)
    #     return collection

    def gameone(self,collection):
        search_url = "http://www.gameone.kr/"
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(search_url)
        try:
            Id = driver.find_element(By.NAME,'user_id')
            Id.send_keys("ldk119")
            Password = driver.find_element(By.NAME,'passwd')
            Password.send_keys("zxcvbnm923")
            Password.submit()
        except:
            pass

        all_stadium_info = []
        url=[]
        # query = quote(keyword)
        page = 1
        # had_url = self.sh.loadURL('navernews',keyword)
        # had_contents = self.sh.loadContents('navernews',keyword)
        before_url = ""
        while_flag = True
        urls = []
        while while_flag:
            
            search_url = 'http://www.gameone.kr/booking/stadium/main?lig_idx=0&page='+str(page)
            plus_url = 'http://www.gameone.kr'
            driver.get(search_url)
            response = driver.page_source
            soup = BeautifulSoup(response,"lxml")
            try:
                ul = soup.find("table",{"class":"list_table"})
                
            except:
                #print("error navernews ul")
                pass
            u = ul.find("tbody")
            # print(u)
            ul = u.find_all("tr")
            # print(ul)
            
            for i,u in enumerate(ul):
                xpath = '//*[@id="Container"]/div/div[1]/div/div[3]/div[2]/table/tbody/tr[%d]/td[11]/a' %(i+1)
                btn = driver.find_element(By.XPATH,xpath)
                url = btn.get_attribute('hidden_href')
                urls.append(plus_url+url)
                
            if(len(ul) <20):
                break
            page+=1
        for u in urls:
            driver.get(u)
            name = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div[1]/div/div[2]/ul[1]/li[2]/strong').text
            date = driver.find_element(By.XPATH,'//*[@id="Container"]/div/div[1]/div/div[2]/ul[1]/li[3]/strong').text
            if date[6] != '1':
                if date[10] != '0':
                    date = date[:4] +'-' +date[7:8]+'-'+date[10:12]
                else:
                    date = date[:4] +'-' +date[7:8]+'-'+date[10:11]
            else:
                if date[8] != '0':
                    date = date[:4] +'-' +date[6:8]+'-'+date[10:12]
                else:
                    date = date[:4] +'-' +date[6:8]+'-'+date[10:11]
            address = driver.find_element(By.XPATH,'//*[@id="Container"]/div/div[1]/div/div[2]/ul[2]/li[2]').text
            address = address[5:]
            slice_idx = address.find('n')
            address = address[slice_idx+1:]
            image_url = None
            try:
                info =  driver.find_element(By.XPATH,'//*[@id="Container"]/div/div[1]/div/div[2]/ul[2]/li[3]/div/ul').text
                slice_idx = info.find('n')
                info = info[slice_idx+1:]
            except:
                pass

            try:
                image_url = driver.find_element(By.XPATH,'//*[@id="Container"]/div/div[1]/div/div[2]/ul[3]/li/a/img').get_attribute('src')
                # print(image_url)
            except:
                pass

            time_table = []
            response = driver.page_source
            soup = BeautifulSoup(response,"lxml")
            times = soup.find('table',{'class','game_table'})
            end_idx = int(times.find("tr",{"style":"display:none"}).text[1])
            games = times.find_all('tr')
            # print(end_idx)
            # print(games)
            for idx, g in enumerate(games):
                if idx == 0:
                    continue
                if idx == end_idx:
                    break
                gg = g.find_all('td')
                # print(gg)
                start = gg[0].text
                # print(start)
                hour = gg[1].text
                # print(len(hour))
                price = g.find('span',{'class','price'}).text
                if price[0] == '0':
                    continue
                idx = price.find(',')
                price = price[:idx]+price[idx+1:-2]
                price = int(price)
                print(price)
                
                start, end = self.time_calc(start,hour)
                time_table.append([start,end])
            



            post = {
                    'date' : date,
                    'stadium_name': name,
                    'stadium_location': address,
                    'stadium_price' : price,
                    'stadium_info' : info,
                    'sports_category' : 'baseball',
                    'operating_hours': time_table,
                    'stadium_img' : image_url
                }
            # print(post)
            collection.insert_one(post)
            
    

    def salgot(self,collection):
        search_url ='https://sports.happysd.or.kr/fmcs/158'
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(search_url)
        # try:
        #     Id = driver.find_element(By.NAME,'user_id')
        #     Id.send_keys("ldk119")
        #     Password = driver.find_element(By.NAME,'passwd')
        #     Password.send_keys("zxcvbnm923")
        #     Password.submit()
        # except:
        #     pass

        all_stadium_info = []
        url=[]
        # query = quote(keyword)
        page = 1
        # had_url = self.sh.loadURL('navernews',keyword)
        # had_contents = self.sh.loadContents('navernews',keyword)
        before_url = ""
        while_flag = True
        urls = []


        address = driver.find_element(By.XPATH,'//*[@id="contents"]/article/div/div/div/ul[1]/li[1]').text[5:]
        info = driver.find_element(By.XPATH,'//*[@id="contents"]/article/div/div/div/ul[1]/li[2]').text
        image_url = driver.find_element(By.XPATH,'//*[@id="contents"]/article/div/div/div/div[1]/div/img[1]').get_attribute('src')
        name = '살곶이 야구장'

        search_url = "https://sports.happysd.or.kr/fmcs/192?facilities_type=C&base_date=20230612&rent_type=1001&center=SUNGDONG05&part=01&place=1"
        driver.get(search_url)
        response = driver.page_source
        soup = BeautifulSoup(response,"lxml")
        # table = soup.find('tr',{'data-time=no':"605"})

        t = soup.find_all("td",{"class":"state-N status-예약가능"})
        time_tmp = []
        time_dic = {}
        for s in t:
            date, start, end = self.parse_info(s.find('span').text)
            if date[5] != '1':
                date = date[:4] +'-' +date[6:7]+'-'+date[9:-1]
            else:
                date = date[:4] +'-' +date[6:8]+'-'+date[10:-1]
            print(date)
            time_tmp.append([date,start,end])
            time_dic[date] = []

        for t in time_tmp:
            time_dic[t[0]].append([t[1],t[2]])
        price = 55000

        for t in time_dic:
            post = {
                        'date' : t,
                        'stadium_name': name,
                        'stadium_location': address,
                        'stadium_price' : price,
                        'stadium_info' : info,
                        'sports_category' : 'baseball',
                        'operating_hours': time_dic[t],
                        'stadium_img' : image_url
                    }
            # print(post)
            # print(type(collection))

            collection.insert_one(post)
    def iamground(self,collection):
        item = ['futsal', 'basketball','soccer']

        for sport in item:
            all_stadium_info = []
            # query = quote(keyword)
            page = 1
            # had_url = self.sh.loadURL('navernews',keyword)
            # had_contents = self.sh.loadContents('navernews',keyword)
            before_url = ""
            while_flag = True
            # while while_flag:

            search_url = "https://www.iamground.kr/"+sport+"/search"
            try:
                # chrome_options = webdriver.ChromeOptions()
                # chrome_options.add_argument('--headless')
                # chrome_options.add_argument('--disable-dev-shm-usage')
                # chrome_options.add_argument("--ignore-certificate-error")
                # chrome_options.add_argument("--ignore-ssl-errors")
                # chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
                # driver = webdriver.Chrome('./driver/chromedriver',chrome_options=chrome_options)
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('headless')
                chrome_options.add_argument('window-size=1920x1080')
                chrome_options.add_argument("--disable-gpu")

                # chrome_options.add_argument('--headless')
                # chrome_options.add_argument('--no-sandbox')
                # chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
                driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
                # print(driver)
                driver.get(search_url)
            except Exception as e:
                print(e)
            # title = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div[3]/ul/li[1]/a/div[2]/h4').text
            # print(title)
            last_scrollHeight = driver.execute_script("return document.documentElement.scrollHeight") #맨 아래 스크롤 위치 파악
            driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(2)
            url = []
            cnt = 1
            # /html/body/div[1]/div[2]/div/div[4]/div[1]/div[2]/div[1]/div[1]
            try:
                element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/div[4]/div[1]/div[2]/div[1]/div[1]')))
            except Exception as e:
                print("1st text none")
                print(e)
                continue
            date = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[4]/div[1]/div[2]/div[1]/div[1]').text
            if date[5] != '1':
                if date[8] != '1':
                    date = date[:4] +'-' +date[6:7]+'-'+date[9:-4]
                else:
                    date = date[:4] +'-' +date[6:7]+'-'+date[8:-4]
            else:
                if date[8] != '1':
                    date = date[:4] +'-' +date[5:7]+'-'+date[9:-4]
                else:
                    date = date[:4] +'-' +date[5:7]+'-'+date[8:-4]
            # print(date)
            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2.0)
                cur_scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
                time.sleep(2.0)
                if cur_scrollHeight == last_scrollHeight:
                    break
                last_scrollHeight = cur_scrollHeight
                
            response = driver.page_source
            soup = BeautifulSoup(response,"lxml")
            # print(soup)
            cards = soup.find_all('div',"row cards rCard")
            urls = []
            already = []

            # href = driver.find_element(By.XPATH,'//*[@id="cardHolder"]/div[1]/div[2]/div[3]/div[2]/button')
            # # //*[@id="cardHolder"]/div[2]/div[2]/div[3]/div[2]/button
            # print(href.get_attribute('onclick'))

            for i in range(len(cards)):
                xpath = '//*[@id="cardHolder"]/div[%d]/div[2]/div[3]/div[2]/button' %(i+1)
                href = driver.find_element(By.XPATH,xpath)
                tmp = href.get_attribute('onclick')
                s_idx = tmp.find(',')
                idx = tmp[8:s_idx]
                st_url = "https://www.iamground.kr/"+sport+"/detail/"+idx
                urls.append(st_url)
            for url in urls:
                driver.get(url)
                response = driver.page_source
                soup = BeautifulSoup(response,"lxml")
                stadium_info = []
                try:
                    stadium_info.append({"date": date})
                    name = driver.find_element(By.XPATH,'//*[@id="infoName"]').text
                    # print(name)
                    stadium_info.append({"name" : name})
                    address = driver.find_element(By.XPATH,'//*[@id="infoAddr"]').text[:-3]
                    # print(address)
                    stadium_info.append({"address":address})

                    image = driver.find_element(By.XPATH,'//*[@id="bigSlickContainer"]/div/div/div[2]')
                    image = image.get_attribute('style')
                    first_idx = image.find('"')
                    end_idx = image.rfind('"')
                    image_url = "https://www.iamground.kr"+image[first_idx+1:end_idx]
                    # print(image_url)
                    info = driver.find_element(By.XPATH, '//*[@id="sizeContainerFut"]').text
                    #time table 생성
                    time_table = []
                    start_times = soup.find_all("div", "time-container resv-group-start")
                    end_times = soup.find_all("div", "time-container resv-group-end")
                    if len(start_times) == 0:
                        continue
                    price = end_times[0].text
                    price = price[:-5]
                    idx = price.find(',')
                    price = price[:idx]+price[idx+1:-2]
                    price = int(price)
                    for t in range(len(start_times)):
                        start_end = []
                        start = start_times[t]["offset"]
                        # print(start[:-2]+':'+start[-2:])
                        end = end_times[t]["offset"]
                        start_end.append({"start" :start[:-2]+':'+start[-2:]})
                        start_end.append({"end" : end[:-2]+':'+end[-2:]})
                        # print(start_end)
                        time_table.append(start_end)
                    post = {
                        'date' : date,
                        'stadium_name': name,
                        'stadium_location': address,
                        'stadium_price' : price,
                        'stadium_info' : info,
                        'sports_category' : sport,
                        'operating_hours': time_table,
                        'stadium_img' : image_url
                    }
                    
                    # print(post)
                    collection.insert_one(post)
                except:
                    pass


ch = CrawlingHandler()
db = DB()
collection = db.initialize()

ch.salgot(collection)
ch.iamground(collection)
ch.gameone(collection)