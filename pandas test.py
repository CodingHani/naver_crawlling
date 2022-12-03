import random
import pandas as pd

df=pd.DataFrame(columns=['idx', 'number'])
df = df.append(pd.DataFrame([[1, 2]], columns=['idx', 'number']), ignore_index=True)
'''
for idx in range (1,11) :
    number = random.randint(1,101)
    
df.set_index('idx', inplace=True)
'''


print (df)