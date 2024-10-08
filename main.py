from flask import Flask, request, send_file, jsonify
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import io

app = Flask(__name__)

# Function to scrape Flipkart
def scrape_flipkart(product):
    Product_Name = []
    Prices = []
    Description = []
    Reviews = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.flipkart.com/'
    }

    for i in range(2, 12):
        url = f"https://www.flipkart.com/search?q={product}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        box = soup.find("div", class_="DOjaWF gdgoEp")

        if not box:
            continue

        names = box.find_all('div', class_="KzDlHZ")
        for name in names:
            Product_Name.append(name.text)

        prices = box.find_all('div', class_="Nx9bqj _4b5DiR")
        for price in prices:
            Prices.append(price.text)

        desc = box.find_all('ul', class_="G4BRas")
        for description in desc:
            Description.append(description.text)

        reviews = box.find_all('div', class_="XQDdHH")
        for review in reviews:
            Reviews.append(review.text if review else np.nan)

    # Ensure the lengths are the same
    min_length = min(len(Product_Name), len(Prices), len(Description), len(Reviews))

    Product_Name = Product_Name[:min_length]
    Prices = Prices[:min_length]
    Description = Description[:min_length]
    Reviews = Reviews[:min_length]

    # Create DataFrame
    df = pd.DataFrame({"Product Name": Product_Name, "Prices": Prices, "Description": Description, "Reviews": Reviews})
    return df

@app.route('/', methods=['GET'])
def scrape_product():
    # Get the product name from the query parameter
    product = request.args.get('product')
    if not product:
        return jsonify({"error": "Product name is required"}), 400

    # Scrape the data
    df = scrape_flipkart(product)

    # Generate CSV in memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Return the CSV file as an attachment
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name=f'{product}_flipkart_data.csv')

if __name__ == '__main__':
    app.run(debug=True)
