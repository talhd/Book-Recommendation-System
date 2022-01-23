"""
Part one-scraping data from https://www.goodreads.com/
and building data frame
Because of the server's unexpected behavior (sometimes returns 504) we will use loops that try to submit the request again.
The attempts number is limited so we don't enter infinity loop.
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
def returnTheHtmlFile(url):
    numOfAttemptsToPullOnePage=0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'cache-control': 'private, max-age=0, no-cache'
    }
    ##The server of goodreads.com,limits the number of requests it allows,so if necessary we will try more than once
    while numOfAttemptsToPullOnePage < 100:
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            htmlFile = request.text
            return htmlFile
        numOfAttemptsToPullOnePage += 1
    return None
def loadSoupObject(htmlFile):
    sou = BeautifulSoup(htmlFile, "html.parser")
    return sou
def scrapeBookNameAndUrl(url):
    bookUriDictionary = {}#The dictionary contains the title of the book and the corresponding link on the site
    numOfPage=0
    while numOfPage < 4500:#4500=the number of pages we want to process
        file=returnTheHtmlFile(url+str(numOfPage+1))
        soupObject = loadSoupObject(file)
        booksInPage = soupObject.findAll(class_="bookTitle")
        for book in booksInPage:
            if book is not None:
                bookName = book.get_text(strip=True)
                bookUriDictionary[bookName] = book['href']
        numOfPage+=1
    return bookUriDictionary
def returnBookInfo(bookUrlFromdict, bookName):
    listOfCategories=[]
    BookSummary=None
    releaseDate=None
    BookRating=None
    itemUrl = "https://www.goodreads.com" + bookUrlFromdict[bookName]
    file = returnTheHtmlFile(itemUrl)
    soupObject = loadSoupObject(file)
    #Case 1
    data=soupObject.find('nobr', {'class': 'greyText'})
    if data is not None:
        data=data.get_text(strip=True)
        temp = re.findall(r'\d+', data)
        res = list(map(int, temp))
        if len(res) != 0:
            if len(str(res[0]))<4 and len(res) >1:
                releaseDate=str(res[1])
            else:
                releaseDate = str(res[0])
    else:
        # Case 2
        data = soupObject.find('p', {'data-testid': 'publicationInfo'})
        if data is not None:
            data = data.get_text(strip=True)
            temp = re.findall(r'\d+', data)
            res = list(map(int, temp))
            if len(res) != 0:
                if len(str(res[0])) < 4 and len(res) >1:
                    releaseDate = str(res[1])
                else:
                    releaseDate = str(res[0])
    # Case 3
    if data is None:
        data = soupObject.findAll(class_='row')
        if data is not None and len(data) > 1:
            STRING = data[1].get_text(strip=True)
            temp = re.findall(r'\d+', STRING)
            res = list(map(int, temp))
            if len(res) != 0:
                if len(str(res[0])) < 4 and len(res) >1:
                    releaseDate = str(res[1])
                else:
                    releaseDate = str(res[0])
    booksOBJ = soupObject.find(id='descriptionContainer')
    if booksOBJ is None:
        booksOBJ=soupObject.find('span', {'class': 'Formatted'})
    if booksOBJ is not None:
        BookSummary = booksOBJ.get_text(strip=True).replace("...more", '')
    BookRating = soupObject.find('span', {'itemprop': 'ratingValue'})
    if BookRating is None:
        BookRating = soupObject.find(class_='RatingStatistics__rating')
    if BookRating is not None:
        BookRating=BookRating.get_text(strip=True)
    bookCategory=soupObject.findAll("script")
    TextToProcessed=str(bookCategory[9])
    AllBookCategories=TextToProcessed[TextToProcessed.find('shelf')+8:TextToProcessed.find('"]);')+2].replace('"]',"").replace('","'," ").replace('["',"")
    i=0
    j=0
    while i<len(AllBookCategories) and j < 4:
        listOfCategories.append(AllBookCategories[0:AllBookCategories.find(' ')])
        AllBookCategories=AllBookCategories[AllBookCategories.find(' ')+1:len(AllBookCategories)]
        i+=AllBookCategories.find(' ')+1
        j+=1
    if len(listOfCategories)==0:
        BookCategories = soupObject.findAll('span', {'class': 'BookPageMetadataSection__genre'})
        for Categori in BookCategories:
            catString=Categori.find(class_='Button Button--tag-inline Button--medium')['href']
            catString.find('genres/')
            catString=catString[catString.find('es/')+3:len(catString)]
            listOfCategories.append(catString)
    return BookSummary,BookRating,listOfCategories,releaseDate
def returnFinalDF():
    bookList=[[]]
    url = "https://www.goodreads.com/shelf/show/"
    allBooks = scrapeBookNameAndUrl(url)
    for key, value in allBooks.items():
        BookSummary,BookRating,listOfCategories,releaseDate = returnBookInfo(allBooks, key)
        bookList.append([key,BookSummary,BookRating,listOfCategories,releaseDate])
        newtxt=BookSummary[0:30]+"..."
        print(key+",",newtxt+",",BookRating+",",str(listOfCategories)+",",releaseDate)
    df = pd.DataFrame(bookList, columns=['Book title', 'Summary','Book rating', 'Categories','Date of publication'])
    return df
df=returnFinalDF()
#the file data collected is *not* the final DF,he is protect the final DF in case of running this file
df.to_csv("data_collected.csv")
