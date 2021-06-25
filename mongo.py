from pymongo import MongoClient
import config

#initiate an instance of mongodb
cluster = MongoClient(config.MONGO_URI)

#selecting the required cluster and collection
#cluster is similar to "database" name
#collection is similar to "table" name
db = cluster["amazon"]
collection = db["product_info"]

#function to fetch all records for given product id(s) from db
def fetchProductInfo(product_ids):
    productInfo = []
    for pid in product_ids:
        results = collection.find({"product_id": pid})
        for result in results:
            productInfo.append(result)
    return productInfo

#function to fetch all records (all product ids) from db
def fetchAll():
    productInfo = []
    results = collection.find()
    for result in results:
        productInfo.append(result)
    return productInfo

#function to insert a new record into db
def insertProductInfo(info):
    collection.insert_many(info)


