import pymongo

MONGO_URI = "mongodb+srv://yunbiyomi:If1bVa7tPtpkxa08@cluster0.ntzk0r5.mongodb.net/?retryWrites=true&w=majority"
MONGO_CONN = pymongo.MongoClient(MONGO_URI)

def conn_mongodb():
    db = MONGO_CONN.store
    return db