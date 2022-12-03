import requests
import bs4
import json
import pandas as pd

url="https://new.land.naver.com/api/regions/complexes?cortarNo=4111312600&realEstateType=APT&order="


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
temp=json.loads(r.text)

dic = { 
    'MarkerId' : [],
    'ApartName' : [],
    'Completion' : [],
    'CountDong' : [],
    'TotalHouse' : [],
    'DealCount' : [],
    'LeaseCount' : [],
    'RentCount' : [],
}

for i in (temp['complexList']) :
    dic['MarkerId'].append(i['complexNo'])
    dic['ApartName'].append(i['complexName'])
    dic['Completion'].append(i['useApproveYmd'])
    dic['CountDong'].append(i['totalBuildingCount'])
    dic['TotalHouse'].append(i['totalHouseholdCount'])
    dic['DealCount'].append(i['dealCount'])
    dic['LeaseCount'].append(i['leaseCount'])
    dic['RentCount'].append(i['rentCount'])
    
df=pd.DataFrame(dic)

## 동 갯수가 1개인 아파트는 대상에서 제외 ##
idx_drop=df[df['CountDong'] == 1].index

df=df.drop(idx_drop)

for i in (df['MarkerId']) :
    print(i)



'''
way="D:/Coding/Python/test/naver_test_name.csv"
df.to_csv(way)
'''