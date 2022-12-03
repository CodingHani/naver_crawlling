
import pandas as pd

data=pd.read_csv("D:/Coding/Python/test/naver_test.csv", encoding='utf=8')


idx_drop=data[data['ExclusiveSize'] < 50].index
data=data.drop(idx_drop)


         


print(data['ExclusiveSize'])
'''
Last_drop=data[str(int(data['ExclusiveSize'])<84)].index 
data=data.drop(Last_drop)


idx_drop=df[df['CountDong'] == 1].index # 동 갯수가 1개인 아파트는 제외하기

df_ApartNumber=df.drop(idx_drop)
print(len(df_ApartNumber))
'''