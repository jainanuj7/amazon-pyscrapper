from pymongo import MongoClient
import config

cluster = MongoClient(config.MONGO_URI)
db = cluster["amazon"]
collection = db["product_info"]

def fetchProductInfo(product_ids):
    productInfo = []
    for pid in product_ids:
        results = collection.find({"product_id": pid})
        for result in results:
            productInfo.append(result)
    return productInfo

def fetchAll():
    productInfo = []
    results = collection.find()
    for result in results:
        productInfo.append(result)
    return productInfo

def insertProductInfo(info):
    collection.insert_many(info)


