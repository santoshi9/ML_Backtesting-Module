from fyers_apiv3 import fyersModel
import webbrowser
import asyncio
import time
from datetime import datetime
import pandas as pd
import json, os

# App credentials
grant_type = "authorization_code"
response_type = "code"
state = "sample"
secret_key = "LQB3KW42GC"
client_id = "AANHR796OG-100"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
generateTokenUrl = appSession.generate_authcode()

#Run 1 time and use its token if re-run it , then code with exiting token may change 
# webbrowser.open(generateTokenUrl,new=1)
# print(kk,"----^^^^----^^^^^")


auth_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJBQU5IUjc5Nk9HIiwidXVpZCI6IjdhN2Q0YzIxZjhiMTQ3NzRhZGY0ZDlhYjVjNGIxODg4IiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IllTNjE0OTciLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI5ZmUwNWEzZDRmZjk5NjJlNmFmY2YwMzYwMzkxMmJhYmE1MmY3ODBiMjk2NGIwMjFlZWY4YTVlYyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzc5OTc4ODcwLCJpYXQiOjE3Nzk5NDg4NzAsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3OTk0ODg3MCwic3ViIjoiYXV0aF9jb2RlIn0.3hTDnNTRk5FEJjOOmPYniUO0VY7EYpfPMqWbjwGM0FU"
appSession.set_token(auth_code)
response = appSession.generate_token()

## There can be two cases over here you can successfully get the acccessToken over the request or you might get some error over here. so to avoid that have this in try except block
try: 
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]
    
    data = pd.DataFrame([{"access_token": access_token, "refresh_token": refresh_token}])
    data.to_csv("auth_refresh_tokens.csv", index=False)
    print(data,"access_token112233")
    print("csv saved successfully.")
except Exception as e:
    print(e,response)
    
    