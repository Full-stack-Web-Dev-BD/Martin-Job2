from pymongo import MongoClient
from datetime import datetime
import json

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
uk_daily_data = db['UK_Daily_Data']

# Arrays to store before and after update data
before_update = []
after_update = []

# Check if uk_daily_data collection has any documents
count = uk_daily_data.count_documents({})
print(f"Number of documents in uk_daily_data: {count}")

def fetch_and_update():
    try:
        # Fetch data from uk_daily_data collection
        uk_daily_data_cursor = uk_daily_data.find()
        data_found = False
        
        # Update sp_upc_lookup based on uk_daily_data
        for row in uk_daily_data_cursor:
            data_found = True
            asin = row.get('ASIN')
            print("asin", asin)
            if not asin:
                continue  # Skip rows without ASIN
             
            update_data = {
                "UK_Buybox_Price_£": row.get('UK_Buybox_Price'),
                "UK_FBA_Fees_£": row.get('UK_FBA_Fees'),
                "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee'),
                "UK_Referral_Fee_£": row.get('UK_Referral_Fee'),
                "time_date_stamp": datetime.now()
            }

            # Perform update
            result = sp_upc_lookup.update_many(
                {"asin": asin, "to_be_removed": {"$ne": "Y"}},
                {"$set": update_data}
            )

            print(f"Updated {result.matched_count} documents for ASIN: {asin}")

        if not data_found:
            print("No data found in uk_daily_data collection.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Update completed successfully.")

# Call the fetch_and_update function
fetch_and_update()
