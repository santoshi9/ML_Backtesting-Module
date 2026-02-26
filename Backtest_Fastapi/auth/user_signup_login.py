from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
# from Database.db import get_collection
# from Database.model import UserSignup
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
import bcrypt
import os
from sqlalchemy.orm import Session



# users_collection = get_collection("users")   # ✅ get collection here


# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
# ALGORITHM = "HS256"
# JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
# JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

# def user_exists(email: str):
#     return users_collection.find_one({"email": email})


# def signup(user):
#     # Check existing user
#     if user_exists(user.email):
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Confirm password match
#     if user.password != user.confirm_password:
#         raise HTTPException(status_code=400, detail="Passwords do not match")

#     # Hash password
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

#     user_data = {
#         "username": user.username,
#         "email": user.email,
#         "password": hashed_password.decode('utf-8')
#     }

#     result = users_collection.insert_one(user_data)
#     return {"user_id": str(result.inserted_id)}



# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def userlogin(email, password):
#     # Check existing user
#     if user_exists(user.email):
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Confirm password match
#     if user.password != user.confirm_password:
#         raise HTTPException(status_code=400, detail="Passwords do not match")

#     # Hash password
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

#     user_data = {
#         "username": user.username,
#         "email": user.email,
#         "password": hashed_password.decode('utf-8')
#     }

#     result = users_collection.insert_one(user_data)
#     return {"user_id": str(result.inserted_id)}