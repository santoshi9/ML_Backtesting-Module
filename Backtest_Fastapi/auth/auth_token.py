import requests
import hashlib
import json
from fyers_apiv3 import fyersModel
import pandas as pd
import os

refresh_token_file = "auth_refresh_tokens.csv"



if not os.path.exists(refresh_token_file):
    raise FileNotFoundError("❌ Token file not found. Run manual_login.py first.")



read_csv = pd.read_csv(refresh_token_file)
refresh_token = read_csv["refresh_token"].iloc[-1]
access_token = read_csv["access_token"].iloc[0]
secret_key = "LQB3KW42GC"
client_id = "AANHR796OG-100"


class authentication:

    @staticmethod
    def generate_app_hash(client_id: str, secret_key: str) -> str:

        combined = f"{client_id}:{secret_key}"
        return hashlib.sha256(combined.encode()).hexdigest()



    @staticmethod
    def get_access_token():

        try:

            # with open("access_token.txt", "r") as file:
            #     access_token = file.read().strip()

            fyers = fyersModel.FyersModel(
                client_id=client_id,
                token=access_token,
                log_path="",
                is_async=False
            )

            profile = fyers.get_profile()

            print("✅ Fyers Connected Successfully")
            print(profile)

            return fyers

        except Exception as e:

            print("❌ Error while loading access token:", str(e))
            return None



    def get_fyers_profile(access_token: str):
        """
        Initialize FyersModel and fetch user profile.
        """
        fyers = fyersModel.FyersModel(
            client_id=client_id,
            token=access_token,
            log_path="",
            is_async=False
        )

        profile = fyers.get_profile()
        return profile