import random
from datetime import datetime

def initiate_payment(amount, receiver_id):
    # Simulate a delay like a real payment gateway might have
    from time import sleep
    sleep(1)  # Sleep for 1 second to simulate network delay

    # Simulate a random success or failure
    if random.choice([True, False]):
        return {
            "success": True,
            "transaction_id": f"TXN{random.randint(1000,9999)}",
            "amount": amount,
            "receiver_id": receiver_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Payment successful"
        }
    else:
        return {
            "success": False,
            "transaction_id": f"TXN{random.randint(1000,9999)}",
            "amount": amount,
            "receiver_id": receiver_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Payment failed"
        }
