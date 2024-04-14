from pymongo import MongoClient
import certifi

# Replace the following with your actual MongoDB connection string
MONGO_CONNECTION_STRING = "mongodb+srv://inyourserve:R33c3b1h6JXbrJoK@shagunpe.dhmtxh2.mongodb.net/"

client = MongoClient(MONGO_CONNECTION_STRING,tlsCAFile=certifi.where())
db = client.shagunpe  # Change 'shagunpe' to your database name
