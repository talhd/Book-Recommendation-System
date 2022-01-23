"""
Data cleansing
1.remove data we do not need,like the volume number in the series or comments about the cover
2.remove duplication and lines with missing data
3.remove books that have not yet been published
4.Remov books that are too old (before 1564)
5.remove non-English books
"""
import pandas as pd
df=pd.read_csv("booksDF.csv")
##remove all the data inside the parentheses and book number(information we do not need)
df['Book title'] = df['Book title'].str.replace(r" \(.*\)","").replace(r'( #[^# ]+?)+$',"")
##remove all the books with the same name
df=df.drop_duplicates(subset=['Book title'])
##remove empty rows
df.dropna(subset=['Book title','Summary','Book rating','Date of publication'], inplace=True)
df = df[df.Categories != '[]']
df = df[df['Book rating'] >= 1]
df = df[df['Book rating'] <= 5]
df = df[df['Date of publication'] >= 1564]
df = df[df['Date of publication'] <= 2021]
##remove all the non english rows
df=df[df['Book title'].map(lambda x: x.isascii())]
df.drop(df.columns[0], axis=1, inplace=True)

df = df.reset_index(drop=True)
df.to_csv("booksDF.csv")
