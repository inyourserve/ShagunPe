from pydantic import BaseModel, Field, validator
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

class EventDetailSchema(EventSchema):
    id: Optional[PyObjectId] = Field(alias='_id')
    shagunId: Optional[str]
    qrCode: Optional[str]

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }

class CashEntrySchema(BaseModel):
    eventId: PyObjectId
    senderName: str
    senderLocation: str
    amount: float
    transactionDate: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }

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

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda oid: str(oid)}
        schema_extra = {
            "example": {
                "senderId": "507f1f77bcf86cd799439011",
                "receiverId": "507f1f77bcf86cd799439012",
                "eventId": "507f1f77bcf86cd799439013",
                "amount": 100.00,
                "transactionDate": "2021-07-21T14:00:00",
                "paymentMethod": "online",
                "status": "pending",
                "paymentGateway": "Stripe",
                "gatewayTransactionId": "ch_1Isqxw2eZvKYlo2C1B576xdu",
                "paymentStatus": "successful"
            }
        }

