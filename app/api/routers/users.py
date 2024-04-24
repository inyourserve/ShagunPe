from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from jose import jwt
from datetime import datetime, timedelta
from app.models.schemas import UserSchema
from app.utils.msg91 import send_otp, verify_otp
from app.models.database import db
import secrets

router = APIRouter()

# OAuth2PasswordBearer is a class that provides an authentication mechanism
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
# Secret key and algorithm for JWT token generation
SECRET_KEY = secrets.token_hex(32) # Generates a 64-character hexadecimal string
ALGORITHM = "HS256"

# Function to create an access token using JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=600000)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the JWT token and extract the mobile number


@router.post("/users/register")
def register_user(user: UserSchema):
    if not send_otp(user.mobile):
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    return {"message": "OTP sent to mobile"}

@router.post("/users/auth")
def authenticate_user(mobile: str, otp: str):
    if not verify_otp(mobile, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    existing_user = db.users.find_one({"mobile": mobile})
    if not existing_user:
        result = db.users.insert_one({"mobile": mobile})
        user_id = result.inserted_id  # Get the MongoDB ObjectId
    else:
        user_id = existing_user['_id']

    # Generate a JWT token for the user with user_id
    token = create_access_token(data={"user_id": str(user_id), "mobile": mobile})

    return {"access_token": token, "token_type": "bearer"}


def get_current_user(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = api_key.split(" ")[1] if api_key.startswith("Bearer ") else api_key
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        mobile: str = payload.get("mobile")
        user_id: str = payload.get("user_id")
        if mobile is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


# @router.get("/me")
# def get_current_user_endpoint(user_id: str = Depends(get_current_user)):
#     # Fetch user details from the database using the user_id extracted from the token
#     print(user_id)
#     user_details = db.users.find_one({"_id": user_id})
#     if not user_details:
#         raise HTTPException(status_code=404, detail="User not found")
#     # Optionally, return any specific user details
#     return {"user_id": user_id, "mobile": user_details["mobile"]}

@router.get("/me")
def get_current_user_endpoint(user_id: str = Depends(get_current_user)):
    # Convert user_id from string to ObjectId
    object_id = ObjectId(user_id)
    print(object_id)  # Debug print to confirm correct ObjectId conversion

    # Fetch user details from the database using the ObjectId
    user_details = db.users.find_one({"_id": object_id})
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")

    # Optionally, return any specific user details
    return {"user_id": user_id, "mobile": user_details["mobile"]}