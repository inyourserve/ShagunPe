from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    mobile: str

class EventSchema(BaseModel):
    eventName: str
    guardianName: str
    location: str
    eventDate: datetime
    isPrivate: Optional[bool] = True



class CashEntrySchema(BaseModel):
    eventId: str
    senderName: str
    senderLocation: str
    amount: float
    transactionDate: datetime

    class Config:
        orm_mode = True

