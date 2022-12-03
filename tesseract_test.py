import pandas as pd

df = pd.DataFrame({'name': ['동남1단지','동남2차','동남3차'],
                   'price': ['2억 5,500','1억 5,500','3억 5,000']}
                  )


df=df.stack().str.replace(',','').unstack()

n=0
for i in df['price'] :
    if i.find('억') == -1 :
        i=int(i)*10000
        i=format(i,',')
        print(i)
    else :
        i=int(i.split('억')[0])*100000000 + int(i.split('억')[1].strip().replace(',',''))*10000
        i=format(i,',')
        df['price'][n]=i
        n=n+1

print(df)    

