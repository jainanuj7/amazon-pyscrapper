import http.client
from bs4 import BeautifulSoup
from datetime import datetime
from mongo import *
import config
import scrapper_config

product_ids = config.PRODUCT_IDS

productInfo = []
for pid in product_ids:

    conn = http.client.HTTPSConnection("www.amazon.com")
    
    #rotate user agents
    headers = scrapper_config.get_user_agent()

    conn.request("GET", "/dp/" + pid, headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    soup = BeautifulSoup(data, features="html.parser")
    
    #Find availability status
    try:
        availability = soup.find(id='availability').get_text().find("Currently unavailable")
        if availability != -1:
            availability = "Out of Stock"
    except(AttributeError):
        availability = "In Stock"

    #Find price
    try:
        price = soup.find(id='priceblock_ourprice').get_text().strip().replace("$", "").replace(",", "")
    except(AttributeError):
        price = None
    

    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    obj = {"product_id": pid, "timestamp": timestamp, "price": price, "availability": availability}
    print("-----Appending------")
    print(obj)
    productInfo.append(obj)

#Commit to MongoDB
insertProductInfo(productInfo)