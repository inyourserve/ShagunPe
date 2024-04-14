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

    # Save the user's mobile number to the database
    existing_user = db.users.find_one({"mobile": mobile})
    if not existing_user:
        result = db.users.insert_one({"mobile": mobile})
        print("Inserted user with ID:", result.inserted_id)  # For debugging purposes

    # Generate a JWT token for the user
    token = create_access_token(data={"mobile": mobile})

    # Return the JWT token to the user
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = api_key.split(" ")[1] if api_key.startswith("Bearer ") else api_key
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        mobile: str = payload.get("mobile")
        if mobile is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return mobile
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

@router.get("/me")
def get_current_user_endpoint(mobile: str = Depends(get_current_user)):
    return {"mobile": mobile}
