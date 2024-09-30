import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup

Product_Name = []
Prices = []
Description = []
Reviews = []

strs = input("Enter the product reviews you want: ")

for i in range(2,12):

    url = "https://www.flipkart.com/search?q="+strs+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(i)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.flipkart.com/'
    }

    r = requests.get(url, headers=headers)

    soup= BeautifulSoup(r.text, 'lxml')

    box = soup.find("div", class_ = "DOjaWF gdgoEp")

    names = box.find_all('div',class_ = "KzDlHZ")
    for i in names:
        name = i.text
        Product_Name.append(name)

    prices = box.find_all('div',class_ = "Nx9bqj _4b5DiR")
    for i in prices:
        price = i.text
        Prices.append(price)

    desc = box.find_all('ul',class_ = "G4BRas")
    for i in desc:
        description = i.text
        Description.append(description)


    reviews = box.find_all('div',class_ = "XQDdHH")
    for i in reviews:
        review = i.text
        if(review):
            Reviews.append(review)
        else:
            Reviews.append(np.nan)


print(len(Product_Name),len(Prices),len(Description),len(Reviews))

minLength = min(len(Product_Name),len(Prices),len(Description),len(Reviews))

Product_Name = Product_Name[:len(Product_Name)-(len(Product_Name)-minLength)]
Prices = Prices[:len(Prices)-(len(Prices)-minLength)]
Description = Description[:len(Description)-(len(Description)-minLength)]
Reviews = Reviews[:len(Reviews)-(len(Reviews)-minLength)]



df = pd.DataFrame({"Product Name":Product_Name,"Prices": Prices, "Description":Description, "Reviews":Reviews})

print(df)

df.to_csv(strs+".csv")