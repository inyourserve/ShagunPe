from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import TransactionSchema
from app.utils.dummy_payment_getway import initiate_payment
from app.models.database import save_new_transaction, update_transaction_status, get_online_transactions
from app.api.routers.users import get_current_user
from bson import ObjectId

router = APIRouter()


@router.post("/transactions/send_shagun")
async def send_shagun(transaction: TransactionSchema):
    # Convert Pydantic model to dictionary for database insertion
    transaction_dict = transaction.dict()
    transaction_dict['status'] = 'pending'  # Initial status

    # Save the new transaction in the database
    transaction_id = save_new_transaction(transaction_dict)

    # Initiate payment
    payment_response = initiate_payment(transaction.amount, transaction.receiverId)

    if payment_response['success']:
        # Update the transaction status to "successful" in the database
        update_transaction_status(transaction_id, "successful", {
            "transaction_id": payment_response['transaction_id'],
            "payment_details": payment_response['message']
        })
        return {"status": "success", "details": payment_response['message'],
                "transaction_id": payment_response['transaction_id']}
    else:
        # Update the transaction status to "failed" in the database
        update_transaction_status(transaction_id, "failed", {
            "error_details": payment_response['message']
        })
        return {"status": "error", "details": payment_response['message']}


@router.get("/transactions/online", response_model=List[TransactionSchema])
async def list_online_transactions(user_id: str = Depends(get_current_user)):
    # Fetch online transactions for the user
    object_id = ObjectId(user_id)
    transactions = get_online_transactions(object_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No Transaction Found")
    return transactions
