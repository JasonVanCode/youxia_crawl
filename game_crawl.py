import re
import queue
import random
import requests

from time import sleep
from threading import Thread
from bs4 import BeautifulSoup


class GameCrawl():

    def __init__(self):
        self.url = "https://0day.ali213.net/listhtml/topn200_{}.html";
        self.crawl_data = []


    def html_parse(self,num):
        pattern = re.compile(r'<.+?>(.+)<.+?>(.+)<.+?><.+?>')
        pattern2 = re.compile(r'<span>(.+)</span>')
        try:
            url_make = self.url.format(num)
            html = requests.get(url_make, timeout=10)
            soup = BeautifulSoup(html.content,'lxml')
            html_result = soup.find_all("div",class_="ol_one")
            for key,val in enumerate(html_result):
                g_score = ''
                g_avgscore = ''
                g_avgscore_obj = ()
                g_time = val.find(class_="pc").string
                g_name = val.find(class_="ol_one_c_etit").string
                g_type = val.find(class_="ps4").string
                g_score_obj = re.search(pattern, str(val.find(class_="ol_one_r_pf")));
                if g_score_obj:
                    g_score_obj = g_score_obj.groups()
                    g_score = str(g_score_obj[0]) + str(g_score_obj[1])
           
                g_avgscore_obj = re.search(pattern2, str(val.find(class_="ol_one_r_tit")))
                if g_avgscore_obj:
                    g_avgscore_obj = g_avgscore_obj.groups()
                    g_avgscore = g_avgscore_obj[0]
              
                g_iamges = val.img["src"]
                self.crawl_data.insert(key, [g_time,g_name,g_type,g_score,g_avgscore,g_iamges])

        except requests.ConnectionError:
            print('连接失败')

    def pic_download(self):
        try:
            for key,val in enumerate(self.crawl_data):
                if key == 0:
                    print(val)
        except requests.ConnectionError:
            pass

    def main(self):
        page_num = 7
        threads_0 = []
        for i in range(1, page_num):
            t = Thread(target=self.html_parse, args=(i,), name='Thread-0')
            threads_0.append(t)

        for i in range(len(threads_0)):
            threads_0[i].start()
        for i in range(len(threads_0)):
            threads_0[i].join()

        self.pic_download()

if __name__ == "__main__":
    obj = GameCrawl()
    obj.main()


