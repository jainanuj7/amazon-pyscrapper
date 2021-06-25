import http.client
from bs4 import BeautifulSoup
from datetime import datetime
from mongo import *
import config
import scrapper_config

#Note: running this scrapper will fetch details for all product id(s) mentioned in config file
product_ids = config.PRODUCT_IDS

productInfo = []
for pid in product_ids:

    conn = http.client.HTTPSConnection("www.amazon.com")
    
    #rotate user agents
    #rotation is not implemented as of now
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}

    #trigger an https request
    conn.request("GET", "/dp/" + pid, headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    #save the response from request as a BeautifulSoup object
    soup = BeautifulSoup(data, features="html.parser")
    
    #Find product availability status
    try:
        availability = soup.find(id='availability').get_text().find("Currently unavailable")
        if availability != -1:
            availability = "Out of Stock"
    except(AttributeError):
        availability = "In Stock"

    #Find product price
    try:
        price = soup.find(id='priceblock_ourprice').get_text().strip().replace("$", "").replace(",", "")
    except(AttributeError):
        price = None
    
    #set current timestamp
    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    
    #prepare object to be inserted into db
    obj = {"product_id": pid, "timestamp": timestamp, "price": price, "availability": availability}
    print("-----Appending------")
    print(obj)
    productInfo.append(obj)

#Commit to MongoDB
insertProductInfo(productInfo)