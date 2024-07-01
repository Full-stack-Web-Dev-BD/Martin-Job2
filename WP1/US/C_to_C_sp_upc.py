from pymongo import MongoClient
from datetime import datetime
import json

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
us_daily_data = db['US_Daily_Data']

# Arrays to store before and after update data
before_update = []
after_update = []

# Check if us_daily_data collection has any documents
count = us_daily_data.count_documents({})

def fetch_and_update_sp_upc_lookup():
    print(f"Number of documents in us_daily_data: {count} sp upc lookup table ")

    try:
        # Fetch data from us_daily_data collection
        us_daily_data_cursor = us_daily_data.find()
        data_found = False
        
        # Update sp_upc_lookup based on us_daily_data
        for row in us_daily_data_cursor:
            data_found = True
            asin = row.get('ASIN')
            print("asin", asin)
            if not asin:
                continue  # Skip rows without ASIN
             
            update_data = {
                "US_Buybox_Price_£": row.get('US_Buybox_Price'),
                "US_FBA_Fees_£": row.get('US_FBA_Fees'),
                "US_Variable_Closing_Fee_£": row.get('US_Variable_Closing_Fee'),
                "US_Referral_Fee_£": row.get('US_Referral_Fee'),
                "time_date_stamp": datetime.now()
            }

            # Perform update
            result = sp_upc_lookup.update_many(
                {"asin": asin, "to_be_removed": {"$ne": "Y"}, "gsl_code": "B"},
                {"$set": update_data}
            )
            print(f"Updated {result.matched_count} documents for ASIN: {asin}")

        if not data_found:
            print("No data found in us_daily_data collection.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("============Update completed successfully SP_UPC_LOOKUP from US Daily Data  Table=============")

# Call the fetch_and_update_sp_upc_lookup function
# fetch_and_update_sp_upc_lookup()