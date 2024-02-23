from pymongo import MongoClient

def connect_db():
    client=MongoClient('mongodb://localhost:27017')
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client
    