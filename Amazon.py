from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title = soup.find('span',attrs = {'id': 'productTitle'})
        title_value = title.text
        title_string  = title_value.strip()

    except AttributeError:
        title_string = ''

    return title_string

def get_price(soup):

    try:
        price = soup.find('span',attrs = {'class':'a-price aok-align-center'}).find('span',attrs = {'class':'a-offscreen'}).text

    except AttributeError:
        price = ''

    return price

def get_rating(soup):
    try:
        rating  = soup.find('span',attrs = {'class':'a-icon-alt'}).text
    except AttributeError:
        rating = ''

    return rating

def get_review_count(soup):
    try:
        review_count = soup.find('span',attrs = {'id':'acrCustomerReviewText'}).text
    except AttributeError:
        review_count = ''
    return review_count

def get_availability(soup):
    try:
        availability = soup.find('span',attrs = {'class':'a-size-medium a-color-success'}).text
    except AttributeError:
        availability = ''
    return availability

if '__main__' == __name__:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.amazon.com/'
    }
    strs = input("Enter the product name: ")
    url = strs

    webpage = requests.get(url, headers=headers)

    soup = BeautifulSoup(webpage.content, 'html.parser')

    links = soup.find_all('a',attrs = {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    links_list = []

    for link in links:
        links_list.append(link.get('href'))

    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=headers)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'] = amazon_df['title'].replace('', np.nan)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)




# url = "https://www.amazon.com/s?k=gaming+laptop&crid=2ST1RM1WTQQ5N&sprefix=gaming+latop%2Caps%2C427&ref=nb_sb_noss_2"
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Referer': 'https://www.amazon.com/'
#     }
#
# webpage = requests.get(url, headers=headers)
# soup = BeautifulSoup(webpage.content, 'html.parser')
# # print(soup.prettify())
#
# links = soup.find_all('a',attrs = {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
# link = links[0].attrs['href']
# print(link)
#
# fullLink = "https://www.amazon.com/"+ link
# print(fullLink)
#
# new_webpage = requests.get(fullLink, headers=headers)
# new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
# title = new_soup.find('span',attrs = {'id': 'productTitle'}).text.strip()
# print(title)
#
# price = new_soup.find('span',attrs = {'class':'a-price aok-align-center'}).find('span',attrs = {'class':'a-offscreen'}).text
# print(price)
#
# rating = new_soup.find('span',attrs = {'class':'a-icon-alt'}).text
# print(rating)
#
# review_count = new_soup.find('span',attrs = {'id':'acrCustomerReviewText'}).text
# print(review_count)
#
# availability = new_soup.find('span',attrs = {'class':'a-size-medium a-color-success'}).text
# print(availability)