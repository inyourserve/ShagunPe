from fastapi import APIRouter, HTTPException, Depends, Body
from app.models.schemas import AddressSchema, PyObjectId
from app.api.routers.users import get_current_user
from app.models.database import db  # Your MongoDB integration module
from typing import List

router = APIRouter()


@router.post("/addresses", response_model=AddressSchema)
async def add_address(address: AddressSchema = Body(...), user_id: PyObjectId = Depends(get_current_user)):
    # Ensure all incoming address data is properly formatted
    address_data = address.dict(by_alias=True)
    address_data['userId'] = user_id

    if not address_data.get('isSaved', True):
        address_data['isDeleted'] = True
    else:
        # Check if the address already exists for the user
        existing_address = db.savedAddresses.find_one({
            "userId": user_id,
            "name": address_data['name'],
            "location": address_data['location'],
            "isDeleted": False
        })
        if existing_address:
            raise HTTPException(status_code=400, detail="Address already exists")

    # Ensure only one default address per user
    if address_data.get('isDefault', False):
        # Update all other addresses of the user to set isDefault to False
        db.savedAddresses.update_many(
            {"userId": user_id, "isDefault": True},
            {"$set": {"isDefault": False}}
        )

    # Insert the new address into the database
    result = db.savedAddresses.insert_one(address_data)
    # Retrieve the newly added address from the database to return it
    return db.savedAddresses.find_one({"_id": result.inserted_id})


@router.delete("/addresses/{address_id}")
async def delete_address(address_id: PyObjectId, user_id: PyObjectId = Depends(get_current_user)):
    # Mark the address as deleted instead of removing it from the database
    update_result = db.savedAddresses.update_one(
        {"_id": address_id, "userId": user_id},
        {"$set": {"isDeleted": True}}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Address not found or not authorized to delete")
    return {"status": "address marked as deleted"}


@router.get("/addresses", response_model=List[AddressSchema])
async def list_addresses(user_id: PyObjectId = Depends(get_current_user)):
    # Retrieve all non-deleted addresses associated with the user
    addresses = list(db.savedAddresses.find({"userId": user_id, "isDeleted": False}))
    return addresses
