# app/api/routers/events.py

from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import EventSchema
from app.models.database import db
from app.api.routers.users import get_current_user
from app.models.schemas import CashEntrySchema
from bson import ObjectId

import uuid
import qrcode
from io import BytesIO
import base64

router = APIRouter()


def generate_shagun_id():
    return str(uuid.uuid4())


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    return base64.b64encode(buffered.getvalue()).decode()


@router.post("/events", response_model=EventSchema)
def create_event(event: EventSchema, mobile: str = Depends(get_current_user)):
    user = db.users.find_one({"mobile": mobile})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    shagun_id = generate_shagun_id()
    qr_code = generate_qr_code(shagun_id)

    event_data = event.dict()
    event_data["userId"] = user["_id"]
    event_data["shagunId"] = shagun_id
    event_data["qrCode"] = qr_code
    event_id = db.events.insert_one(event_data).inserted_id

    created_event = db.events.find_one({"_id": event_id})
    return created_event


@router.post("/events/cash_entry", response_model=CashEntrySchema)
def create_cash_entry(entry: CashEntrySchema, mobile: str = Depends(get_current_user)):
    # Find the event by ID
    event = db.events.find_one({"_id": ObjectId(entry.eventId)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Find the receiver's user ID
    receiver_user_id = db.users.find_one({"mobile": mobile})["_id"]

    # Create the cash entry
    entry_data = entry.dict()
    entry_data["receiverId"] = receiver_user_id  # Receiver is making the entry
    entry_data["paymentMethod"] = "cash"
    entry_data["isOnline"] = False
    entry_id = db.transactions.insert_one(entry_data).inserted_id

    # Retrieve the created entry and return it
    created_entry = db.transactions.find_one({"_id": entry_id})
    return created_entry

