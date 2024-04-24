from pymongo import MongoClient
import certifi
from bson import ObjectId

# Replace the following with your actual MongoDB connection string
MONGO_CONNECTION_STRING = "mongodb+srv://inyourserve:R33c3b1h6JXbrJoK@shagunpe.dhmtxh2.mongodb.net/"

client = MongoClient(MONGO_CONNECTION_STRING, tlsCAFile=certifi.where())
db = client.shagunpe  # Use the actual database name


def save_new_transaction(transaction_data):
    """Insert a new transaction into the database."""
    return db.transactions.insert_one(transaction_data).inserted_id


def update_transaction_status(transaction_id, status, additional_info=None):
    """Update the transaction's status."""
    update_data = {'status': status}
    if additional_info:
        update_data.update(additional_info)
    db.transactions.update_one({'_id': ObjectId(transaction_id)}, {'$set': update_data})


def save_new_event(event_data):
    """Insert a new event into the database."""
    return db.events.insert_one(event_data).inserted_id


def get_event_by_id(event_id):
    """Retrieve an event by its ID."""
    return db.events.find_one({'_id': ObjectId(event_id)})


def get_user_events(user_id):
    """Retrieve all events created by a specific user."""
    return list(db.events.find({"userId": ObjectId(user_id)}))

# def get_online_transaction(user_id):
#     """Retrieve all Online Transaction created by a specific user."""
#     return list(db.transactions.find({"userId": ObjectId(user_id), "paymentMethod": "online"}))


def get_online_transactions(user_id):
    """Retrieve all online transactions where the user is either the sender or the receiver."""
    user_object_id = ObjectId(user_id)  # Ensure the user_id is converted to ObjectId
    query = {
        "$or": [
            {"senderId": user_object_id},
            {"receiverId": user_object_id}
        ],
        "paymentMethod": "online"  # Ensure only online transactions are retrieved
    }
    return list(db.transactions.find(query))
