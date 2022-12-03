import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

USER="xe3773xe"
PASS ="mcymenu30!"

session = requests.session()

login_info = {
    "client_id": USER,
    "pwd_dummy": PASS
}


url_login = "https://www.auction1.co.kr/common/login_box.php"
res = session.post(url_login, data=login_info)
res.raise_for_status() # 오류가 발생하면 예외가 발생합니다.



# 마이페이지에 접근하기 
url_mypage = "https://www.auction1.co.kr/member/point_history.php" 
res = session.get(url_mypage)
res.raise_for_status()

# 포인트
soup = BeautifulSoup(url_mypage, "html.parser")

print(soup)