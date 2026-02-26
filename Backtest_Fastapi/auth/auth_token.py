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
secret_key = "LQB3KW42GC"
client_id = "AANHR796OG-100"


class authentication:

    @staticmethod
    def generate_app_hash(client_id: str, secret_key: str) -> str:

        combined = f"{client_id}:{secret_key}"
        return hashlib.sha256(combined.encode()).hexdigest()



    @staticmethod
    def get_access_token():
        
        pin = "4568"

        app_hash = authentication.generate_app_hash(client_id, secret_key)
        url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"

        payload = {
            "grant_type": "refresh_token",
            "appIdHash": app_hash,
            "refresh_token": refresh_token,
            "pin": pin
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            data = response.json()

            if data.get("s") == "ok":
                access_token = data["access_token"]
                print("✅ Access Token generated successfully!")
                
                fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="", is_async=False )
                return fyers
            else:
                print("❌ Error while generating access token:", data)
                return None
        except Exception as e:
            print("❌ Exception while generating access token:", str(e))
            return None


    # def get_fyers_profile(access_token: str):
    #     """
    #     Initialize FyersModel and fetch user profile.
    #     """
    #     fyers = fyersModel.FyersModel(
    #         client_id=client_id,
    #         token=access_token,
    #         log_path="",
    #         is_async=False
    #     )

    #     profile = fyers.get_profile()
    #     return fyers