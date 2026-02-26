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


auth_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJBQU5IUjc5Nk9HIiwidXVpZCI6IjU0MTkyNzZjMWM5MzQ4NTc4MDc5ZjI0NGNkMjhiNGQwIiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IllTNjE0OTciLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI2MmNhNzdmZTA5OGRmYjc2YTg0Yjc0NDY2ODVhNThiYzRkOTlmODhkZjc2OGFjMDcyOGM4ODg3MSIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzcwMjIyOTQ5LCJpYXQiOjE3NzAxOTI5NDksImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3MDE5Mjk0OSwic3ViIjoiYXV0aF9jb2RlIn0.DmurQekZZG2wsjpvPNevbJIIH53NvGLOrdcp0CYi3BA"
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
    
    