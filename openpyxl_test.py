## 데이터 프레임 만들기 ##
import openpyxl
import requests
from bs4 import BeautifulSoup

way='D:/Coding/Python/test/excel.xlsx'
wb=openpyxl.load_workbook(way)

wb.create_sheet(index=1, title='옥션원 크롤링')
sheet=wb.active
wb['옥션원 크롤링'].append(['사건번호','주소','대지권','전용면적','감정가','매각가','매각기일'])

url=requests.get(browser.current_url)
bs_obj=BeautifulSoup(url, "html.parser")
 
bs_obj.find_all("div", {"class" : "no bold"})

bs_obj.find_all("div", {"class" : "addr black"})





wb.save(way)