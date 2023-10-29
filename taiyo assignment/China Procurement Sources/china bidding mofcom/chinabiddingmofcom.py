import re
import time
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from dateutil.parser import parse


class Scraping_project:

    def __init__(self, url):
        self.url = url
        self.base_url = r'http://en.chinabidding.mofcom.gov.cn/bidDetail'

    def Scraping_project_data(self):

        """Get Request and return Beautifulsoup"""
        def get_soup(url):
            get_response = requests.get(url)
            print(get_response)
            get_soup_text = BeautifulSoup(get_response.text, 'html.parser')
            return get_soup_text

        """Post Request and return json"""
        def post_request(url):
            post_response = requests.post(post_url, data=payload)
            print(post_response)
            post_text = post_response.json()
            return post_text

        """Date Format Change"""
        def date_stamp_format(date):
            parsed_date = parse(date)
            date = parsed_date.strftime('%Y-%m-%d')
            return date

        pageNumber = 1
        Manual_ID = 1
        while True:
            post_url = r'http://en.chinabidding.mofcom.gov.cn/zbwcms/front/en/bidding/bulletinList'
            payload = {
                'pageNumber': f'{pageNumber}',
                'pageSize': '1000',
                'type': '',
                'industry': '',
                'provinceCode': '',
                'keyword': '',
                'capitalSourceCode': ''
            }
            post_text = requests.post(post_url, data=payload).json()
            if str(post_text['pageNumber']) < str(pageNumber):
                break
            else:
                for single_project_info in post_text['rows']:
                    publishTime = date_stamp_format(single_project_info['publishTime'])
                    createTime = date_stamp_format(single_project_info['createTime'])
                    industryName = single_project_info['industryName']
                    areaName = single_project_info['areaName']
                    project_name = single_project_info['name']
                    capitalSourceName = single_project_info['capitalSourceName']
                    digest = single_project_info['digest']
                    fdid = single_project_info['fdid']
                    Tender_type = ['New Tenders' if x == "1" else 'Tender Changes' if x == "2" else
                    'Evaluation Results' if x == "3" else 'Tender Awards' if x == "4" else ''
                            for x in single_project_info['type']][0]
                    project_url = self.base_url+single_project_info['filePath']
                    print(project_url)
                    project_dictionary = {
                        "Manual_ID": Manual_ID,
                        "project_name": project_name,
                        "createTime": createTime,
                        "publishTime": publishTime,
                        "capitalSourceName": capitalSourceName,
                        "digest": digest,
                        "fdid": fdid,
                        "Tender_type": Tender_type,
                        "project_url": project_url
                    }
                    # print(Tender_dictionary)
                    Manual_ID += 1
                    """Csv Creation"""
                    file_name = 'chinabidding_mofcom_projects'
                    if os.path.isfile(f'{file_name}.csv'):
                        df = pd.DataFrame([project_dictionary])
                        # df.drop_duplicates(subset=['Tender_ID'], inplace=True, keep='first')
                        df.to_csv(f'{file_name}.csv', mode='a', header=False, index=False)
                    else:
                        df = pd.DataFrame([project_dictionary])
                        df.to_csv(f'{file_name}.csv', index=False)
                pageNumber += 1




if __name__ == "__main__":
    given_url = r'http://en.chinabidding.mofcom.gov.cn/channel/EnSearchList.shtml?provinceCodeShow=&capitalSourceCodeShow=&keyword=&tenders=&industry='
    project_datas = Scraping_project(given_url)
    project_datas.Scraping_project_data()