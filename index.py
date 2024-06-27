from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
uk_daily_data = db['UK_Daily_Data']

# Debug prints to confirm connection and collections
print("Connected to database:", db.name)
print("sp_upc_lookup collection:", sp_upc_lookup.name)
print("uk_daily_data collection:", uk_daily_data.name)

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
            if not asin:
                continue  # Skip rows without ASIN
            update_data = {
                "UK_Buybox_Price_£": row.get('UK_Buybox_Price_£'),
                "UK_FBA_Fees_£": row.get('UK_FBA_Fees_£'),
                "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee_£'),
                "UK_Referral_Fee_£": row.get('UK_Referral_Fee_£'),
                "time_date_stamp": datetime.now()
            }

            result = sp_upc_lookup.update_many(
                {"ASIN": asin, "to_be_removed": {"$ne": "Y"}},
                {"$set": update_data}
            )

            print(f"Updated {result.matched_count} documents for ASIN: {asin}")

        if not data_found:
            print("No data found in uk_daily_data collection.")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Update completed successfully.")

fetch_and_update()
