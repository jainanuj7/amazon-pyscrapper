import os

basedir = os.path.abspath(os.path.dirname(__file__))

#mongo db credentials
MONGO_USER = "root"
MONGO_PASS = "root"

#URI to connect to mongodb
MONGO_URI = "mongodb+srv://"+ MONGO_USER + ":" + MONGO_PASS + "@cluster0.i8b6s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
PRODUCT_IDS = ['B08BB9RWXD', 'B08SJTX6PN', 'B09453B84Z']