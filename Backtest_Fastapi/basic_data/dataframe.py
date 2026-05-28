from fyers_apiv3 import fyersModel
import webbrowser
import asyncio
import pandas as pd
import time
from datetime import datetime
from auth.auth_token import authentication
import os
import pyarrow as pa
import pyarrow.parquet as pq
import datetime as dt


fyers = authentication.get_access_token()

# dict = "Parquet_Reports"


class Dataframe():
    def backdata(exchange, symbol , interval, start_epoch, current_end, instrument_type):
        """
        Fetch historical 5-min candle data from Fyers API.
        Dates must be in the past and format: YYYY-MM-DD HH:MM:SS
        """
        try:

                data = {
                    "symbol": f"{exchange}:{symbol}-{instrument_type}",
                    "resolution": f"{interval}",        
                    "date_format": "0",   
                    "range_from": str(start_epoch),
                    "range_to": str(current_end),
                    "cont_flag": "1"
                }

                response = fyers.history(data)
                print("📊 Fyers Response:", response)

                if isinstance(response, dict) and response.get("code") == 429:
                    print("⚠️ Rate limit hit. Sleeping for 15 seconds...")
                    time.sleep(15)
                    

                if response.get("s") != "ok":
                    # return {"status": "error", "message": response}
                    print("Fyers Error:", response)
                    return None

                # ✅ Parse and save data
                candles = response["candles"]
                df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["timestamp"] = (
                        pd.to_datetime(df["timestamp"], unit="s", utc=True)
                        .dt.tz_convert("Asia/Kolkata")
                        .dt.tz_localize(None)
                    )

                
                data = df
                
                return data
            
            
        except Exception as e:
            print("⚠️ Exception:", str(e))
            return None 


    
    def append_to_parquet(symbol, df, file_path):
        try:
            table = pa.Table.from_pandas(df)

            if not os.path.exists(file_path):
                pq.write_table(table, file_path)
            else:
                pq.write_table(table, file_path, append=True)

            return True

        except Exception as e:
            print(f"❌ Parquet write failed: {e}")
            return False
        

    def basic_report():
        # include Volume
        return
    
     
    def rsi():
        

        Average_Gain = "Sum of gains over last 14 periods"/ 14


        Average_Loss = "Sum of losses over last 14 periods"/ 14


        return