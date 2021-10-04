import requests
from bs4 import BeautifulSoup
import csv



def scrap():
    #listofurls=["https://www.carwale.com/upcoming-cars/"]
    #for loop for urls
    URL = "https://carsshowroom.herokuapp.com/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    quotes = []  # a list to store quotes
    #if URL==https://carsshowroom.herokuapp.com/
    table = soup.find('div', attrs={'class': 'main-content'})
    print(table)
    for row in table.findAll('img',
                         attrs={'class': 'car_image'}):
        print("TTTTTt",row)
        quote = {}
        quote['img'] = row['src']
        '''quote['theme'] = row.text
        print("I'm here",row.text)'''
        '''quote['url'] = row.a['href']
        quote['img'] = row.img['src']
        quote['lines'] = row.img['alt'].split(" #")[0]
        quote['author'] = row.img['alt'].split(" #")[1]'''
        quotes.append(quote)

    filename = 'inspirational_quotes.csv'
    #if statement for file name
    with open(filename, 'w', newline='') as f:
         w = csv.DictWriter(f, ['img'])
         w.writeheader()
         for quote in quotes:
             w.writerow(quote)
