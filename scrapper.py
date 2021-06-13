import http.client
from bs4 import BeautifulSoup
from datetime import datetime
from mongo import *
import config

product_ids = config.PRODUCT_IDS

productInfo = []
for pid in product_ids:

    conn = http.client.HTTPSConnection("www.amazon.com")
    conn.request("GET", "/dp/" + pid)
    res = conn.getresponse()
    data = res.read()
    soup = BeautifulSoup(data, features="html.parser")
    price = soup.find(id='priceblock_ourprice').get_text().strip().replace("$", "").replace(",", "")
    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    productInfo.append({"product_id": pid, "timestamp": timestamp, "price": price})

insertProductInfo(productInfo)