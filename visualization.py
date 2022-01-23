import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv("booksDF.csv")
fig, ax = plt.subplots()
df['Book rating'].plot.kde(ax=ax, legend=False, title='Probability of getting a book by rating',color='#000000')
df['Book rating'].plot.hist(density=True, ax=ax,rwidth=0.9, color='#0071dc')
ax.set_ylabel('Probability')
ax.grid(axis='y')
ax.set_facecolor('#ffffff')
plt.xlim(xmin=0)
plt.show()
data=df['Date of publication'].sort_values(ascending=True).tolist()
dict = {i:data.count(i) for i in data}
keys = dict.keys()
values = dict.values()
plt.plot(keys,values,color='#0071dc')
plt.fill_between(keys, values, color='#0071dc')
plt.ylim(ymin=0)
plt.xlim(xmin=1564,xmax=2021)
plt.show()
i=0
catData=df['Categories'][0:1000].tolist()
catdict=[]
replacers = {"'":'','[':'',']':'',',':''}
for word in catData:
    while i<len(word.split()):
        res = ''.join([replacers.get(i, i) for i in word.split()[i]])
        catdict.append(res)
        i+=1
    i=0
dict = {i:catdict.count(i) for i in catdict}
for data in list(dict):
    if dict[data] < 20:
        dict.pop(data)
keys = dict.keys()
values = dict.values()
plt.bar(keys,values)
plt.xticks(rotation=30, ha='right')
plt.show()