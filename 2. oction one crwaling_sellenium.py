import re
import time
import warnings
import xml.etree.ElementTree as ET
from datetime import datetime
import openpyxl
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



## 검색정보 입력 ##
kind = input('물건 종류를 입력하세요 : ')
judge=input('감정가 시작가 입력(드랍다운 메뉴에 있는 것으로) : ')
sido=input('시도명을 입력하세요 : 서울부산대구인천충남충북 : ')
gugun=input('시군구 명을 입력하세요 : ')
dong=input('읍면동을 입력하세요 : ')

period_start_text=input("시작기간을 입력하세요 : ")
period_end_text=input("끝기간을 입력하세요 : ")

bunji1_text=input('번지수를 입력하세요 (앞부분만) : ')
bunji2_text=input('번지수를 입력하세요 (뒤 부분만) : ')



browser = webdriver.Chrome()

browser.get('https://www.auction1.co.kr/')
elem = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/a[1]/div')
elem.click()
time.sleep(2)

## 아이디 , 암호 입력 ##
browser.find_element(By.ID, 'client_id').send_keys('xe3773xe')
time.sleep(1)
browser.find_element(By.ID,'client_id').send_keys(Keys.TAB , 'mcymenu30!', Keys.TAB,Keys.TAB,Keys.TAB,Keys.ENTER)
time.sleep(1)

'''
##팝업이 있을 경우 활성화
browser.switch_to.window(browser.window_handles[1])
browser.close()

browser.switch_to.window(browser.window_handles[0])
'''

## 홈 -> 경매검색 -> 매각사례 클릭##
browser.find_element(By.CSS_SELECTOR, 'body > div.width_guide > div > div > ul > li:nth-child(1) > a > span').click()
time.sleep(2)
browser.find_element(By.XPATH, '//*[@id="snb"]/div/div[2]/ul/a[10]/li').click()
time.sleep(2)

## 검색 조건 설정 ##
period_start=browser.find_element(By.XPATH, '//*[@id="next_biddate1"]')
period_end=browser.find_element(By.XPATH, '//*[@id="next_biddate2"]')
bunji1=browser.find_element(By.XPATH, '//*[@id="bunji1"]')
bunji2=browser.find_element(By.XPATH, '//*[@id="bunji2"]')

drop_kind=browser.find_element(By.XPATH, '//*[@id="s_class"]')
drop_judge=browser.find_element(By.XPATH, '//*[@id="ser_frm"]/form/table/tbody/tr[1]/td[3]/select[1]')
drop_sido=browser.find_element(By.XPATH, '//*[@id="sido"]')
drop_gugun=browser.find_element(By.XPATH, '//*[@id="gugun"]')
drop_dong=browser.find_element(By.XPATH, '//*[@id="dong"]')

period_start.click()
period_start.send_keys(period_start_text)
period_end.click()
period_end.send_keys(period_end_text)
bunji1.send_keys(bunji1_text)
bunji2.send_keys(bunji2_text)

try :
    drop=Select(drop_kind)
    drop.select_by_visible_text(kind)
    drop=Select(drop_judge)
    drop.select_by_visible_text(judge)
    drop=Select(drop_sido)
    drop.select_by_visible_text(sido)
    time.sleep(1)
    drop=Select(drop_gugun)
    drop.select_by_visible_text(gugun)
    drop=Select(drop_dong)
    drop.select_by_visible_text(dong)

except : 
    '빈칸이 있을 경우 나오는 멘트'


## 결과 검색 ##
browser.find_element(By.XPATH, '//*[@id="ser_frm"]/form/table/tbody/tr[6]/td[3]/input[6]').click()
while_exit = True

def PageCrawling() :
    ### 페이지 크롤링 ###
   
    elem_number=browser.find_elements(By.CSS_SELECTOR,'div.no.bold')
    elem_address=browser.find_elements(By.CSS_SELECTOR,'div.addr.black')
    elem_land=browser.find_elements(By.CSS_SELECTOR,'div.view_gray')
    elem_jprice=browser.find_elements(By.CSS_SELECTOR,'td.money.bold.f12')
    elem_date=browser.find_elements(By.CSS_SELECTOR, 'td.center')[12:]
                
    for elem in elem_number :
        dic['CaseNumber'].append(elem.text)
    for elem in elem_address :
        dic['Adress'].append(elem.text)
    for elem in elem_land :
        dic['Size'].append(elem.text)
    
    '''
    try : 
        for elem in elem_land :
            landsize=elem.text.split(',')[0].replace('[', '').replace('대지권 ','').replace('㎡','')
            housesize=elem.text.split(',')[1].replace(']', '').strip().replace('건물 ','').replace('㎡','')
            dic['LandSize'].append(landsize)
            dic['HouseSize'].append(housesize)
    except :
        dic['LandSize'].append('error T_T')
        dic['HouseSize'].append('error T_T')
    '''    
        
    for elem in elem_jprice :
        dic['JudgePrice'].append(elem.text.split()[0].strip())
        dic['SellingPrice'].append(elem.text.split()[2].lstrip())
    for elem in elem_date :
        elem_date_text=re.search(r'\d{4}.\d{2}.\d{2}', elem.text)
        if elem_date_text != None :
            dic['Date'].append(elem_date_text.group())

    return None       
    ### 페이지 크롤링 끌 ###

dic= {
            'CaseNumber' : [],
            'Adress' : [],
            'Size' : [],
            'JudgePrice' : [],
            'SellingPrice' : [],
            'Date' : []
        }

## 페이지바 넘기기 ##
while True :
    page_bar=browser.find_element(By.XPATH, '//*[@id="auct_list"]/div[4]/div')
    pages=page_bar.find_elements(By.CSS_SELECTOR, 'a')
    page_now=page_bar.find_element(By.CSS_SELECTOR, 'strong')
    page_now_text=page_now.get_attribute('innerText')
    

    for page in pages :
        
        ### 페이지 넘기기 ###
        page_num=page.get_attribute('innerText') 
        if page_num in ['처음', '이전'] :
           pass
        elif int(page_num) > int(page_now_text) :

            ### 페이지 크롤링 ###
            PageCrawling()
           
        ### 페이지 크롤링 끌 ###

            page.click()
            break 
        if page_num == '다음' : 
            page.click()
            break
    
    if pages[-1] in ['다음', '끝'] :
        pass
    elif int(page_now_text)-1==len(pages) :
        PageCrawling()
        break
    elif len(pages)==pages.index(pages[-1])+2 :
        PageCrawling()
        break

df=pd.DataFrame(dic)
df.set_index('CaseNumber')

'''
way="D:/Coding/Python/test/test.xlsx"
with pd.ExcelWriter(way, mode='a') as writer :
    df.to_excel(writer, sheet_name='옥션원 크롤링')
'''

file_name="("+period_start_text+"~"+period_end_text+")"+sido+"_"+gugun+"_"+dong
way="D:/Coding/Python/test/"+file_name+".csv"
df.to_csv(way)
print("크롤링 완료")
browser.close()
     

    