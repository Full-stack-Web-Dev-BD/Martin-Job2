# Calculate UK Profit for sp_upc_lookup 1st table
from pymongo import MongoClient
from datetime import datetime
import json

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
uk_daily_data = db['UK_Daily_Data']

def calculateProfit_sp_upc_lookup1(batch_size=1000):
    try:
        last_processed_asin = None
        while True:
            query = {} if last_processed_asin is None else {'ASIN': {'$gt': last_processed_asin}}
            batch_asins = uk_daily_data.distinct('ASIN', query).limit(batch_size)
            if not batch_asins:
                break
            for asin in batch_asins:
                last_processed_asin = asin
                # Fetch all documents from sp_upc_lookup for this ASIN
                documents = sp_upc_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}, "gsl_code": "C"})
                print(f"Processing ASIN: {asin}")
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

                    uk_profit = uk_buybox_price - (uk_fba_fees + uk_variable_closing_fee + uk_referral_fee + seller_price)
                    uk_profit_rounded = round(uk_profit, 2)

                    # Update the document with the calculated UK_Profit
                    sp_upc_lookup.update_one(
                        {'_id': document['_id']},
                        {'$set': {'UK_Profit': uk_profit_rounded}}
                    )
                    print(f"Updated document with ASIN {asin}")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("============Completed Profit Calculation =============")

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

calculateProfit_sp_upc_lookup1()
