import bs4
import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import xml.etree.ElementTree as ET
import warnings

incoding = "5REH0kgwFds%2BWiR%2BeuIxSSvzdYWCKYnPaGxct9f2jrTJN8frwUO3CvFnKMyILeJXbSoavirh6EQi7x9GJGyfUg%3D%3D"
decoding = "5REH0kgwFds+WiR+euIxSSvzdYWCKYnPaGxct9f2jrTJN8frwUO3CvFnKMyILeJXbSoavirh6EQi7x9GJGyfUg=="

url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?_wadl&type=xml"
service_key="5REH0kgwFds%2BWiR%2BeuIxSSvzdYWCKYnPaGxct9f2jrTJN8frwUO3CvFnKMyILeJXbSoavirh6EQi7x9GJGyfUg%3D%3D"

areacode='44210'

# 조회기간 설정 변수
month_digit = ['01','02','03','04','05','06','07','08','09','10','11','12'] 
search_year = '2021'

# 총 거래내역
count = []

## 내가 건든거 ##
df=pd.DataFrame(columns=['Date', 'Size', 'Floor', 'Amount', 'Name', 'Dong', 'Jibun'])
warnings.filterwarnings(action='ignore')
## 여기 까지 ##

# 추출 모듈
for each in month_digit:
    yearmonth = search_year + each

    # url 입력
    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
    params ={'serviceKey' : decoding, 'pageNo' : '1', 'numOfRows' : '10000', 'LAWD_CD' : areacode, 'DEAL_YMD' : yearmonth }

    response = requests.get(url, params=params).text
    xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
    rows = xmlobj.findAll('item')

    j = 0
    count.append(len(rows)) # 해당 기간의 거래내역 개수 저장

    # 거래별 세부 항목 정리
    while j <= len(rows)-1:
        columns = rows[j].find_all()

        # 세부 항목(값) 추출
        for item in columns:
            if item.name == "아파트":
                complex = item.text
            if item.name == "거래유형":
                type = item.text
            if item.name == "년":
                year = item.text    
            if item.name == "월":
                month = item.text
            if item.name == "일":
                day = item.text
            if item.name == "전용면적":
                size = item.text
            if item.name == "층":
                floor = item.text
            if item.name == "거래금액":
                amount = item.text.strip()
            if item.name == "지번":
                jibun = item.text
            if item.name == "법정동" :
                dong = item.text

            ## 여긴 내가 건든거 ##

            
        df = df.append(pd.DataFrame([[year+"."+month+"."+day, size, floor, amount*1000, complex,dong, jibun]], columns=['Date', 'Size', 'Floor', 'Amount', 'Name', 'Dong','Jibun']), ignore_index=True)
        

        j += 1

print(f'총 {sum(count)}개의 거래내역이 확인되었습니다.')

print(df)

df.to_excel('D:/Coding/Python/test/excel_test.xlsx')