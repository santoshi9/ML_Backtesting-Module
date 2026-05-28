from fastapi import FastAPI, HTTPException
from fyers_apiv3 import fyersModel
from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from datetime import datetime, timedelta
import time
import asyncio
from auth.auth_token import authentication
from fastapi import Query
import uvicorn
import json
import os
from basic_data.dataframe import Dataframe
# from bson import ObjectId
from Database.db import get_db
from Database.model import User
from Database.schemas import UserCreate, UserLogin, UserResponse
# from auth.user_signup_login import signup
from auth.hasing import hash_password, verify_password
from auth.jwt_handler import create_access_token
from sqlalchemy.orm import Session



folder_path  = "CSV_Reports"
Dic_file_path = "Parquet_Reports"
# --------------------- CONFIGURATION ---------------------
grant_type = "authorization_code"
response_type = "code"
state = "sample"
secret_key = "LQB3KW42GC"
client_id = "AANHR796OG-100"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"


fyers = authentication.get_access_token()
# fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=client_id, log_path="")

router = APIRouter(prefix="/auth", tags=["Auth"])

# --------------------- FASTAPI APP ---------------------
app = FastAPI(title="Fyers API Service")

@app.get("/")
def home():
    return {"message": "✅ Fyers FastAPI is running!"}


# --------------------- PROFILE / FUNDS / HOLDINGS ---------------------
@app.get("/profile")
def get_profile():
    try:
        return fyers.get_profile()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/funds")
def get_funds():
    try:
        return fyers.funds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/holdings")
async def get_holdings():
    try:
        return fyers.holdings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------- QUOTES ---------------------
@app.get("/quotes/{symbol}")
def get_quotes(symbol: str):
    try:
        data = {"symbols": symbol}
        return fyers.quotes(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------- HISTORICAL DATA ---------------------
 


@app.get("/History")
async def get_history(
    exchange: str,
    symbol: str,
    interval: int,
    start: str,
    end: str,
    instrument_type: str = Query("EQ")
):

    try:
        MAX_CANDLES = 100
        now = int(time.time())

        interval_seconds = interval * 60

        start_epoch = int(time.mktime(datetime.strptime(start, "%Y-%m-%d %H:%M:%S").timetuple()))
        end_epoch   = int(time.mktime(datetime.strptime(end, "%Y-%m-%d %H:%M:%S").timetuple()))

        if start_epoch >= end_epoch:
            return {"status": "error", "message": "Start time cannot be greater or equal to end time."}

        if end_epoch > now:
            return {"status": "error", "message": "End time cannot be in the future."}

        candles = (end_epoch - start_epoch) // interval_seconds

        if candles > 100:
            print(f"⚠️ Requested {candles} candles, which exceeds the API limit of {MAX_CANDLES}. Fetching in chunks...")

            CHUNK_SECONDS = interval_seconds * MAX_CANDLES
            current_start = start_epoch

            filename = f"{symbol}_5min_{now}.csv"
            full_path = os.path.join(folder_path, filename)   # ✅ FIXED
            print(full_path,"full_path")  # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            while current_start < end_epoch:

                current_end = min(current_start + CHUNK_SECONDS, end_epoch)

                data = Dataframe.backdata(exchange, symbol, interval, current_start, current_end,instrument_type                )
                print("TYPE OF DATA:", type(data))


                if data is None:
                    current_start = current_end
                    continue

                if not isinstance(data, pd.DataFrame):
                    print("Unexpected type:", type(data))
                    current_start = current_end
                    continue

                if data.empty:
                    current_start = current_end
                    continue

                data.to_csv(
                    full_path,
                    mode="a",
                    index=False,
                    header=not os.path.exists(full_path)
                )

                print(f"Saved {len(data)} rows")

                current_start = current_end
                
                time.sleep(1.5)

                # To avoid hitting rate limits           

        return {"status": "ok"}

    except Exception as e:
        print("⚠️ Exception:", str(e))
        return {"status": "error", "message": str(e)}

    



@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(400, "Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(400, "Invalid credentials")

    if not verify_password(data.password, user.password):
        raise HTTPException(400, "Invalid credentials")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token}

# ------------------- STARTUP & SHUTDOWN EVENTS -------------------

@app.on_event("startup")
async def startup():
    print("🚀 FastAPI started... Launching background data fetcher.")
    # asyncio.create_task(get_history())  # Run it once at startup


@app.on_event("shutdown")
async def shutdown():
    print("🛑 Shutting down server... cleaning up resources.")


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)