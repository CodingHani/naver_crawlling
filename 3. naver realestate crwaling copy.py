import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

down_url = 'https://new.land.naver.com/api/articles/complex/8087?realEstateType=APT%3AABYG%3AJGC&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=1&complexNo=8087&buildingNos=&areaNos=&type=list&order=rank'
r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
    "Accept-Encoding": "gzip",
    "Host": "new.land.naver.com",
    "Referer" : "https://new.land.naver.com/complexes/8087?ms=37.288821,126.9843025,17&a=APT:ABYG:JGC&e=RETAIL",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
})

r.encoding = "utf-8-sig"
temp=json.loads(r.text)

print(temp)
'''
df=pd.DataFrame(temp)


way="D:/Coding/Python/test/naver_test.csv"
df.to_csv(way)
'''