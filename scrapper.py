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
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}
    # print(headers)
    conn.request("GET", "/dp/" + pid, headers=headers)
    res = conn.getresponse()
    data = res.read()
    soup = BeautifulSoup(data, features="html.parser")
    price = soup.find(id='priceblock_ourprice').get_text().strip().replace("$", "").replace(",", "")
    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    obj = {"product_id": pid, "timestamp": timestamp, "price": price}
    print("-----Appending------")
    print(obj)
    productInfo.append(obj)

insertProductInfo(productInfo)