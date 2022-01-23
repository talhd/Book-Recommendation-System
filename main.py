import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
"""
returns the 5 recommended books to the user
"""
def retruRecommendedBooks(bookName):
    df=pd.read_csv("booksDF.csv")
    i=0
    if bookName in df['Book title'].tolist():
        bookIndex = df.index[df['Book title'] == bookName].tolist()
        tfidfvec = TfidfVectorizer(stop_words='english')
        wordVectors = tfidfvec.fit_transform(df['Summary'])
        result = cosine_similarity(wordVectors)
        BooksWithHighCorrelation = np.argpartition(result[bookIndex[0]], -6)[-6:]
        for book in BooksWithHighCorrelation:
            if book != bookIndex:
                val = df['Book title'].values[book]
                print(str(i+1)+")"+val)
                i+=1
    else:
        print("The book is not in df\nyou can use Harry Potter and the Sorcerer's Stone or The Alchemist,for example")
book = input("Enter a favorite book you've read before:\n")
retruRecommendedBooks(book)



















