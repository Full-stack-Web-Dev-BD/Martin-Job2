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
        print("============Update completed successfully SP_UPC_LOOKUP from Daily Data =============")

# Call the fetch_and_update function
fetch_and_update()


def fetch_and_update_uk_profit():
    try:
        # Fetch unique ASIN values from UK_Daily_Data
        unique_asins = uk_daily_data.distinct('ASIN')
        print("ASIN's", unique_asins)
        for asin in unique_asins:
            # Fetch all documents from sp_upc_lookup for this ASIN
            documents = sp_upc_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}})
            print("Document loaded ")
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
                  
                  
                print(f"{uk_buybox_price} - ({uk_fba_fees} + {uk_variable_closing_fee} + {uk_referral_fee} + {seller_price})")
                uk_profit = uk_buybox_price - (uk_fba_fees + uk_variable_closing_fee + uk_referral_fee + seller_price)
                
                # Update the document with the calculated UK_Profit
                sp_upc_lookup.update_one(
                    {'_id': document['_id']},
                    {'$set': {'UK_Profit': uk_profit}}
                )
                
                print(f"Updated document with ASIN {asin}  ",document.get('_id'))

    except Exception as e:
        print(f"An error occurred: {e}")

    print("============Completed Profit Calculatoin =============")

def parse_price(price_str):
    if isinstance(price_str, (int, float)):
        return float(price_str)
    elif isinstance(price_str, str):
        # Remove currency symbols and commas, and then convert to float
        try:
            numeric_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_str)))
            return numeric_value
        except ValueError:
            return 0  # Set default value to 0 if cannot convert to float
    else:
        return 0  # Set default value to 0 for None or other non-string types

fetch_and_update_uk_profit() 