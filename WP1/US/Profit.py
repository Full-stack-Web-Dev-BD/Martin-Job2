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

def fetch_and_update_us_profit():
    print(f"Number of documents in us_daily_data: {count} sp upc lookup ")
    try:
        # Fetch unique ASIN values from US_Daily_Data
        unique_asins = us_daily_data.distinct('ASIN')
        print("ASIN's", unique_asins)
        for asin in unique_asins:
            # Fetch all documents from sp_upc_lookup for this ASIN
            documents = sp_upc_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}, "gsl_code": "B"})
            print("Document Loaded")
            for document in documents:
                # Calculate US_Profit for this document
                us_buybox_price = parse_price(document.get('US_Buybox_Price_£'))
                us_fba_fees = parse_price(document.get('US_FBA_Fees_£'))
                us_variable_closing_fee = parse_price(document.get('US_Variable_Closing_Fee_£'))
                us_referral_fee = parse_price(document.get('US_Referral_Fee_£'))
                seller_price = parse_price(document.get('seller_price'))
                
                # Handle missing or non-numeric fields
                if any(price is None for price in [us_buybox_price, us_fba_fees, us_variable_closing_fee, us_referral_fee, seller_price]):
                    print(f"Skipping document with ASIN {asin} due to missing or invalid price data")
                    continue
                  
                  
                # print(f"{us_buybox_price} - ({us_fba_fees} + {us_variable_closing_fee} + {us_referral_fee} + {seller_price})")
                us_profit = us_buybox_price - (us_fba_fees + us_variable_closing_fee + us_referral_fee + seller_price)
                us_profit_rounded = round(us_profit, 2)

                # Update the document with the calculated Us_Profit
                sp_upc_lookup.update_one(
                    {'_id': document['_id']},
                    {'$set': {'US_Profit': us_profit_rounded}}
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

# fetch_and_update_us_profit() 