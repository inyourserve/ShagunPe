from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class UserSchema(BaseModel):
    mobile: str

class EventSchema(BaseModel):
    eventName: str
    guardianName: str
    location: str
    eventDate: datetime
    isPrivate: Optional[bool] = True

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: lambda oid: str(oid)}

class EventDetailSchema(EventSchema):
    event_id: PyObjectId = Field(default=None, alias='_id')  # Use alias to map MongoDB '_id'
    shagunId: Optional[str]
    qrCode: Optional[str]

class CashEntrySchema(BaseModel):
    eventId: PyObjectId
    senderName: str
    senderLocation: str
    amount: float
    transactionDate: datetime

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: lambda oid: str(oid)}

class TransactionSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    senderId: PyObjectId
    receiverId: PyObjectId
    eventId: PyObjectId
    amount: float
    transactionDate: datetime
    paymentMethod: str
    status: str
    paymentGateway: Optional[str]
    gatewayTransactionId: Optional[str]
    paymentStatus: Optional[str]

class EntrySumSchema(BaseModel):
    total_entries: int
    total_amount: float

# class AddressSchema(BaseModel):
#     id: Optional[PyObjectId] = Field(alias='_id')
#     userId: PyObjectId
#     name: str
#     location: str
#     isDefault: bool = False
#     isDeleted: bool = False

class AddressSchema(BaseModel):
    name: str
    location: str
    isDefault: bool = False
    isSaved: bool = True  # Indicates if the user has chosen to save this address
    isDeleted: bool = False  # Soft delete flag
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = None

    class Config:
            orm_mode = True
            json_encoders = {
                ObjectId: lambda oid: str(oid),
                datetime: lambda dt: dt.isoformat() if dt else None
            }

class GetAddressSchema(AddressSchema):
    id: Optional[PyObjectId] = Field(alias='_id')

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: lambda oid: str(oid)}
