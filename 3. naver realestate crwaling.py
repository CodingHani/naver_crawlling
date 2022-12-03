import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import math
import time




AreaNumber=input("검색을 원하는 지역의 법정동 코드를 입력하세요 : ")

### 해당 지역의 아파트 단지들의 고유 번호 구하기 ##

url="https://new.land.naver.com/api/regions/complexes?cortarNo="+str(AreaNumber)+"&realEstateType=APT&order="

r=requests.get(url, data={"sameAddressGroup":"false"}, headers={
    'Accept-Encoding' : 'gzip',
    'Host': 'new.land.naver.com',
    'Referer' : 'https://new.land.naver.com/complexes/115708?ms=37.2526808,127.0185555,15&a=APT&b=A1&e=RETAIL&h=99&i=132&ad=true',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
})

r.encoding = "utf-8-sig"
temp_apartnumber=json.loads(r.text)

dic_ApartNumber = { 
    'MarkerId' : [],
    'ApartName' : [],
    'Completion' : [],
    'CountDong' : [],
    'TotalHouse' : [],
    'DealCount' : [],
    'LeaseCount' : [],
    'RentCount' : [],
}

for i in (temp_apartnumber['complexList']) :
    dic_ApartNumber['MarkerId'].append(i['complexNo'])
    dic_ApartNumber['ApartName'].append(i['complexName'])
    dic_ApartNumber['Completion'].append(i['useApproveYmd'])
    dic_ApartNumber['CountDong'].append(i['totalBuildingCount'])
    dic_ApartNumber['TotalHouse'].append(i['totalHouseholdCount'])
    dic_ApartNumber['DealCount'].append(i['dealCount'])
    dic_ApartNumber['LeaseCount'].append(i['leaseCount'])
    dic_ApartNumber['RentCount'].append(i['rentCount'])
    
df=pd.DataFrame(dic_ApartNumber)

idx_drop=df[df['CountDong'] == 1].index # 동 갯수가 1개인 아파트는 제외하기

df_ApartNumber=df.drop(idx_drop)
print(len(df_ApartNumber))
pass_or_not=input("최대 예상 소요 시간은 " + str(len(df_ApartNumber)*8) + "초 입니다.  : ")
'''
if pass_or_not == "N" or "n" :
    exit()
    print('여기까지 옴?')
    
else : pass
'''


### 총 페이지 수 구하기 ###
dic_Selling= {
                'SellNumber' : [],
                'ApartName' : [],
                'ApartDong' : [],
                'ApartFloor' : [],
                'CommonSize' : [],
                'ExclusiveSize' : [],
                'Price' : [],
            }

for i in (dic_ApartNumber['MarkerId']) : 
    # 20개씩 밖에 검색이 안되기 때문에 아파트별 물건수에 따른 페이지수 부터 검색 # 
    count_url= 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo='+str(i)+'&cortarNo='+str(AreaNumber)+'&tradTpCd=A1'

    r = requests.get(count_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    r.encoding = "utf-8-sig"
    temp_pagecount=json.loads(r.text)
    page_count=math.ceil(temp_pagecount['result']['totAtclCnt']/20)
    
    time.sleep(3) # 봇 탐지 방지

    ### 아파트별 물건 가져오기 ###
    for t in range (page_count) :
        
        down_url='https://m.land.naver.com/complex/getComplexArticleList?hscpNo='+str(i)+'&cortarNo='+str(AreaNumber)+ '&tradTpCd=A1&order=prc&showR0=N&page=' + str(int(t)+1)


        r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
            "Accept-Encoding": "gzip",
            "Host": "new.land.naver.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
            })
        r.encoding = "utf-8-sig"
        temp_selling=json.loads(r.text)
        
        
        for j in temp_selling['result']['list'] :
            dic_Selling["SellNumber"].append(j['atclNo'])
            dic_Selling["ApartName"].append(j['atclNm'])
            dic_Selling["ApartDong"].append(j['bildNm'])
            dic_Selling["ApartFloor"].append(j['flrInfo'])
            dic_Selling["CommonSize"].append(j['spc1'])
            dic_Selling["ExclusiveSize"].append(j['spc2'])
            dic_Selling['Price'].append(j['prcInfo'])
        time.sleep(5)   # 봇 탐지 방지
        print('페이지 크롤링이 진행중입니다...')
    
df=pd.DataFrame(dic_Selling)
df_Selling=df.set_index('SellNumber')



## 데이터 후 처리 ##


df_Selling=df_Selling.stack().str.replace(',','').unstack()
df_Selling=df_Selling.astype({"ExclusiveSize" : float})


Last_drop=df_Selling[(df_Selling['ExclusiveSize']<50)&(df_Selling['ExclusiveSize']>55)].index # 전용 84 미만 제외
df_Selling=df_Selling.drop(Last_drop)


print(df_Selling)

way="D:/Coding/Python/test/naver_test.csv"
df_Selling.to_csv(way)
## 억 왼쪽 숫자 곱하기 1억 + 억 오른쪽 숫자 하면 숫자로 나올듯## 
n=0
#pd.set_option('mode.chained_assignment',  None) # <==== 경고를 끈다

for i in (df_Selling['Price']) :
    if i.find('억') == -1 :
        i=int(i)*10000
        i=format(i,',')
        df_Selling['Price'][n]=i
        n=n+1
    else :
        try :
            print((int(i.split('억')[0]))*100000000)
            print((int((i.split('억')[1]).strip().replace(',','')))*10000)

            i=(int(i.split('억')[0]))*100000000 + (int((i.split('억')[1]).strip().replace(',','')))*10000
            i=format(i,',')
            df_Selling['Price'][n]=i
            n=n+1
        except :
            i=(int(i.split('억')[0]))*100000000
            i=format(i,',')
            df_Selling['Price'][n]=i
            n=n+1

way="D:/Coding/Python/test/naver_test.csv"
df_Selling.to_csv(way)

