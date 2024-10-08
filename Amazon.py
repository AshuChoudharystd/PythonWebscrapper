from flask import Flask, request, send_file, jsonify
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import io
import csv

app = Flask(__name__)

# Functions for scraping (from your provided code)
def get_title(soup):
    try:
        title = soup.find('span', attrs={'id': 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ''
    return title_string

def get_price(soup):
    try:
        price = soup.find('span', attrs={'class': 'a-price aok-align-center'}).find('span', attrs={'class': 'a-offscreen'}).text
    except AttributeError:
        price = ''
    return price

def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'class': 'a-icon-alt'}).text
    except AttributeError:
        rating = ''
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find('span', attrs={'id': 'acrCustomerReviewText'}).text
    except AttributeError:
        review_count = ''
    return review_count

def get_availability(soup):
    try:
        availability = soup.find('span', attrs={'class': 'a-size-medium a-color-success'}).text
    except AttributeError:
        availability = ''
    return availability

@app.route('/scrape', methods=['POST'])
def scrape_amazon():
    # Get the URL from the request body
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400

    url = data['url']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.amazon.com/'
    }

    # Send request and parse the page
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # Extract product links from the search results
    links = soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = ["https://www.amazon.com" + link.get('href') for link in links]

    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

    # Scrape each product page
    for link in links_list:
        new_webpage = requests.get(link, headers=headers)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    # Create DataFrame and clean it
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'] = amazon_df['title'].replace('', np.nan)
    amazon_df = amazon_df.dropna(subset=['title'])

    # Generate CSV in memory
    output = io.StringIO()
    amazon_df.to_csv(output, index=False)
    output.seek(0)

    # Return the CSV file as an attachment
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='amazon_data.csv')

if __name__ == '__main__':
    app.run(debug=True)
