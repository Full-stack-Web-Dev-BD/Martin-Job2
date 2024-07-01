from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
us_daily_data = db['US_Daily_Data']
uk_daily_data = db['UK_Daily_Data']

def update_sp_upc_lookup(data_cursor, update_fields, gsl_code):
    data_found = False
    for row in data_cursor:
        data_found = True
        asin = row.get('ASIN')
        print("ASIN:", asin)
        if not asin:
            continue  # Skip rows without ASIN

        update_data = {**{field: row.get(field) for field in update_fields}, "time_date_stamp": datetime.now()}

        # Perform update
        result = sp_upc_lookup.update_many(
            {"asin": asin, "to_be_removed": {"$ne": "Y"}, "gsl_code": gsl_code},
            {"$set": update_data}
        )

        # Retrieve and log the updated document(s)
        updated_documents= sp_upc_lookup.find({"asin": asin, "gsl_code": gsl_code})
        for doc in updated_documents:
          print(f"Updated {result.matched_count} documents for ASIN: {asin}")
          print(f"Document ID: {doc['_id']}")
        #     print("rough Data ===========================")
        #     print("Updated Document:", doc)
        #     print("===========>>>>>>>>>>>",data_cursor)
        #     print("rough Data ===========================")
        

    if not data_found:
        print(f"No data found in the specified collection.")

def fetch_and_update():
    try:
        # Update based on US daily data
        us_count = us_daily_data.count_documents({})
        print(f"Number of documents in us_daily_data: {us_count}")

        us_daily_data_cursor = us_daily_data.find()
        us_update_fields = [
            "US_Buybox_Price",
            "US_FBA_Fees",
            "US_Variable_Closing_Fee",
            "US_Referral_Fee"
        ]
        update_sp_upc_lookup(us_daily_data_cursor, us_update_fields, "B")

        # Update based on UK daily data
        uk_count = uk_daily_data.count_documents({})
        print(f"Number of documents in uk_daily_data: {uk_count}")

        uk_daily_data_cursor = uk_daily_data.find()
        uk_update_fields = [
            "UK_Buybox_Price",
            "UK_FBA_Fees",
            "UK_Variable_Closing_Fee",
            "UK_Referral_Fee"
        ]
        update_sp_upc_lookup(uk_daily_data_cursor, uk_update_fields, "C")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("============Update completed successfully SP_UPC_LOOKUP from Daily Data Tables=============")

# Call the fetch_and_update function
fetch_and_update()
