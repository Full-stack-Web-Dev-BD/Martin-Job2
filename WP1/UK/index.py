# Insert Data from Uk Daily Data to Sp Upc Lookup 1st table ( Mongo)

from pymongo import MongoClient
from datetime import datetime
from helper import parse_price


# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
uk_daily_data = db['UK_Daily_Data']
 
# Check if uk_daily_data collection has any documents
count = uk_daily_data.count_documents({})




# C to C Sp Upc Lookup 
def update_sp_upc_lookup(asin, row):
    update_data = {
        "UK_Buybox_Price_£": row.get('UK_Buybox_Price'),
        "UK_FBA_Fees_£": row.get('UK_FBA_Fees'),
        "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee'),
        "UK_Referral_Fee_£": row.get('UK_Referral_Fee'),
        "time_date_stamp": datetime.now()
    }

    # Perform update
    result = sp_upc_lookup.update_many(
        {"asin": asin, "to_be_removed": {"$ne": "Y"},  "gsl_code": "C"},
        {"$set": update_data}
    )

    print(f"==>Updated {result.matched_count} documents for ASIN: {asin}")


def calculate_sp_upc_lookup_Profit(asin):
    documents = sp_upc_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'},"gsl_code": "C"})
    for document in documents:
        # Calculate UK_Profit for this document
        uk_buybox_price = parse_price(document.get('UK_Buybox_Price_£'))
        uk_fba_fees = parse_price(document.get('UK_FBA_Fees_£'))
        uk_variable_closing_fee = parse_price(document.get('UK_Variable_Closing_Fee_£'))
        uk_referral_fee = parse_price(document.get('UK_Referral_Fee_£'))
        seller_price = parse_price(document.get('seller_price'))
        
        # Handle missing or non-numeric fields
        if any(price is None for price in [uk_buybox_price, uk_fba_fees, uk_variable_closing_fee, uk_referral_fee, seller_price]):
            print(f"Skipping document with ASIN {asin} due to missing or invalid price data")
            continue
        
        # print(f"{uk_buybox_price} - ({uk_fba_fees} + {uk_variable_closing_fee} + {uk_referral_fee} + {seller_price})")
        uk_profit = uk_buybox_price - (uk_fba_fees + uk_variable_closing_fee + uk_referral_fee + seller_price)
        uk_profit_rounded = round(uk_profit, 2)
        
        # Update the document with the calculated UK_Profit
        sp_upc_lookup.update_one(
            {'_id': document['_id']},
            {'$set': {'UK_Profit': uk_profit_rounded}}
        )
        print(f"Updated UK_Profit with ASIN {asin}  ",document.get('_id'))
        
        
def fetch_and_update_sp_upc_lookup():
    print(f"Number of documents in uk_daily_data: {count} Updating for sp_upc_lookup ")
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
            # Start Update 
            update_sp_upc_lookup(asin, row)
            calculate_sp_upc_lookup_Profit(asin)
        if not data_found:
            print("No data found in uk_daily_data collection.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("============Update completed successfully SP_UPC_LOOKUP from Daily Data =============")


fetch_and_update_sp_upc_lookup()