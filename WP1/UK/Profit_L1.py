# Calculate UK Profit for sp_upc_lookup 1st table 
from pymongo import MongoClient
from datetime import datetime
from helper import parse_price

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
uk_daily_data = db['UK_Daily_Data']
 
def calculateProfit_sp_upc_lookup1():
    try:
        # Fetch unique ASIN values from UK_Daily_Data
        unique_asins = uk_daily_data.distinct('ASIN')
        print("ASIN's", unique_asins)
        for asin in unique_asins:
            # Fetch all documents from sp_upc_lookup for this ASIN
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
                  
                  
                print(f"{uk_buybox_price} - ({uk_fba_fees} + {uk_variable_closing_fee} + {uk_referral_fee} + {seller_price})")
                uk_profit = uk_buybox_price - (uk_fba_fees + uk_variable_closing_fee + uk_referral_fee + seller_price)
                uk_profit_rounded = round(uk_profit, 2)
                
                # Update the document with the calculated UK_Profit
                sp_upc_lookup.update_one(
                    {'_id': document['_id']},
                    {'$set': {'UK_Profit': uk_profit_rounded}}
                )
                
                print(f"Updated document with ASIN {asin}  ",document.get('_id'))

    except Exception as e:
        print(f"An error occurred: {e}")

    print("============Completed Profit Calculatoin =============")


calculateProfit_sp_upc_lookup1() 