
from fyers_apiv3 import fyersModel
import webbrowser
import asyncio
import pandas as pd
import time
from datetime import datetime

# App credentials
grant_type = "authorization_code"
response_type = "code"
state = "sample"
secret_key = "LQB3KW42GC"
client_id = "AANHR796OG-100"
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
# authorization_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJBQU5IUjc5Nk9HIiwidXVpZCI6ImQzN2QxMzMyZjFlZDRhMzhiZTlmMzc2MzZmMWRkNGE5IiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IllTNjE0OTciLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjNWIwNDFjMmEzMzIzMjc1NzNhOWQxMjQ3ZmNiZWUwYjFjOGI0ZjYzYjA3MmM5MWJjMDQ1NmI4NCIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzUxNDczNTg2LCJpYXQiOjE3NTE0NDM1ODYsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc1MTQ0MzU4Niwic3ViIjoiYXV0aF9jb2RlIn0.BmDp1CeqRD_kRXlgj0JzNRj9VSLcSAluukaeG1pqnrc"

appSession = fyersModel.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,state=state,secret_key=secret_key,grant_type=grant_type)
print("appSession", appSession)
generateTokenUrl = appSession.generate_authcode()
print((generateTokenUrl,"000000000000000000000000"))  
# webbrowser.open(generateTokenUrl,new=1)


auth_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJBQU5IUjc5Nk9HIiwidXVpZCI6IjdhN2Q0YzIxZjhiMTQ3NzRhZGY0ZDlhYjVjNGIxODg4IiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IllTNjE0OTciLCJvbXMiOiJLMSIsImhzbV9rZXkiOiI5ZmUwNWEzZDRmZjk5NjJlNmFmY2YwMzYwMzkxMmJhYmE1MmY3ODBiMjk2NGIwMjFlZWY4YTVlYyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzc5OTc4ODcwLCJpYXQiOjE3Nzk5NDg4NzAsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3OTk0ODg3MCwic3ViIjoiYXV0aF9jb2RlIn0.3hTDnNTRk5FEJjOOmPYniUO0VY7EYpfPMqWbjwGM0FU"
appSession.set_token(auth_code)
response = appSession.generate_token()

## There can be two cases over here you can successfully get the acccessToken over the request or you might get some error over here. so to avoid that have this in try except block
try: 
    access_token = response["access_token"]
except Exception as e:
    print(e,response)
    
    
fyers = fyersModel.FyersModel(token=access_token,is_async=False,client_id=client_id,log_path="")    

# fyers_async = fyersModel.FyersModel(client_id=client_id, token=f"{client_id}:{access_token}", is_async=True)



print(fyers.get_profile())  ## This will provide us with the user related data 

print(fyers.funds(),"FUNDS")        ## This will provide us with the funds the user has 

print(fyers.holdings()) 

## Historical Data 

data = {"symbol":"NSE:SBIN-EQ","resolution":"D","date_format":"0","range_from":"1622097600","range_to":"1622097685","cont_flag":"1"}

print(fyers.history(data))

## Quotes 

# data = {"symbols":"NSE:SBIN-EQ"}
dft = fyers.quotes(data)
# his_df = pd.DataFrame(dft)
print("****his_df****",dft)

start = int(time.mktime(datetime.strptime("2025-07-01 09:15:00", "%Y-%m-%d %H:%M:%S").timetuple()))
end   = int(time.mktime(datetime.strptime("2025-07-01 10:00:00", "%Y-%m-%d %H:%M:%S").timetuple()))

print(start , end ,"***Datetime***")

async def get_history():
    data = {
        "symbol": "NSE:HDFCBANK-EQ",
        "resolution": "5",
        "date_format": "0",                  # Using UNIX timestamp
        "range_from": str(start),         # 2021-05-27
        "range_to": str(end),           # Short range
        "cont_flag": "1"
    }
    response = fyers.history(data)
    print("📊 Historical Data Response:", response)
    if response["s"] == "ok":
        candles = response["candles"]
        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")  # convert UNIX to datetime
        print(df)
    else:
        print("Error fetching data:", response)

asyncio.run(get_history())