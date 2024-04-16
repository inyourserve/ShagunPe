from pymongo import MongoClient
import certifi
from bson import ObjectId

# Replace the following with your actual MongoDB connection string
MONGO_CONNECTION_STRING = "mongodb+srv://inyourserve:R33c3b1h6JXbrJoK@shagunpe.dhmtxh2.mongodb.net/"

client = MongoClient(MONGO_CONNECTION_STRING,tlsCAFile=certifi.where())
db = client.shagunpe  # Change 'shagunpe' to your database name
def save_new_transaction(transaction_data):
    # Insert a new transaction into the database
    return db.transactions.insert_one(transaction_data).inserted_id

def update_transaction_status(transaction_id, status, additional_info=None):
    # Update the transaction's status
    update_data = {'status': status}
    if additional_info:
        update_data.update(additional_info)
    db.transactions.update_one({'_id': ObjectId(transaction_id)}, {'$set': update_data})

