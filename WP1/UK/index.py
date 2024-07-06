import time
from pymongo import MongoClient
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from helper import parse_price

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
sp_upc_lookup = db['sp_upc_lookup']
sp_upc_lookup2 = db['sp_upc_lookup2']
sp_gsl_lookup2 = db['sp_gsl_lookup2']
sp_ID_lookup = db['sp_ID_lookup']
uk_daily_data = db['UK_Daily_Data']

# Configuration
BATCH_SIZE = 1000  # Adjust this size based on your memory and performance requirements
MAX_WORKERS = 10   # Number of threads to use



# SP UPC Lookup
def update_sp_upc_lookup(asin, row):
    update_data = {
        "UK_Buybox_Price_£": row.get('UK_Buybox_Price'),
        "UK_FBA_Fees_£": row.get('UK_FBA_Fees'),
        "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee'),
        "UK_Referral_Fee_£": row.get('UK_Referral_Fee'),
        "time_date_stamp": datetime.now()
    }

    result = sp_upc_lookup.update_many(
        {"asin": asin, "to_be_removed": {"$ne": "Y"}, "gsl_code": "C"},
        {"$set": update_data}
    )

    print(f"==>Updated {result.matched_count} documents for ASIN: {asin}")

def calculate_sp_upc_lookup_Profit(asin):
    documents = sp_upc_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}, "gsl_code": "C"})
    for document in documents:
        uk_buybox_price = parse_price(document.get('UK_Buybox_Price_£'))
        uk_fba_fees = parse_price(document.get('UK_FBA_Fees_£'))
        uk_variable_closing_fee = parse_price(document.get('UK_Variable_Closing_Fee_£'))
        uk_referral_fee = parse_price(document.get('UK_Referral_Fee_£'))
        seller_price = parse_price(document.get('seller_price'))

        if any(price is None for price in [uk_buybox_price, uk_fba_fees, uk_variable_closing_fee, uk_referral_fee, seller_price]):
            print(f"Skipping document with ASIN {asin} due to missing or invalid price data")
            continue

        uk_profit = uk_buybox_price - (uk_fba_fees + uk_variable_closing_fee + uk_referral_fee + seller_price)
        uk_profit_rounded = round(uk_profit, 2)

        sp_upc_lookup.update_one(
            {'_id': document['_id']},
            {'$set': {'UK_Profit': uk_profit_rounded}}
        )
        print(f"Updated UK_Profit with ASIN {asin}  ", document.get('_id'))

# SP UPC Lookup 2
def update_sp_upc_lookup_2(asin , row):        
    update_data = {
        "UK_Buybox_Price_£": row.get('UK_Buybox_Price'),
        "UK_FBA_Fees_£": row.get('UK_FBA_Fees'),
        "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee'),
        "UK_Referral_Fee_£": row.get('UK_Referral_Fee'),
        "time_date_stamp": datetime.now()
    }

    # Perform update
    result = sp_upc_lookup2.update_many(
        {"asin": asin, "to_be_removed": {"$ne": "Y"}, "gsl_code": "C"},
        {"$set": update_data}
    )
    print(f"Updated {result.matched_count} documents for ASIN: {asin}")

def calculate_sp_upc_lookup_2_Profit(asin):
    documents = sp_upc_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}, "gsl_code": "C"})
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
        sp_upc_lookup2.update_one(
            {'_id': document['_id']},
            {'$set': {'UK_Profit': uk_profit_rounded}}
        )
        print(f"Updated document with ASIN {asin}  ",document.get('_id'))

# SP GSL Lookup 2
def update_sp_gsl_lookup_2(asin, row):
    update_data = {
        "UK_Buybox_Price_£": row.get('UK_Buybox_Price'),
        "UK_FBA_Fees_£": row.get('UK_FBA_Fees'),
        "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee'),
        "UK_Referral_Fee_£": row.get('UK_Referral_Fee'),
        "time_date_stamp": datetime.now()
    }
    # Perform update
    result = sp_gsl_lookup2.update_many(
        {"asin": asin, "to_be_removed": {"$ne": "Y"}, "gsl_code": "A"},
        {"$set": update_data}
    )
    print(f"Updated {result.matched_count} documents for ASIN: {asin}")

def update_sp_gsl_lookup_2_Profit(asin):
    documents = sp_gsl_lookup2.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}, "gsl_code": "A"})
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
        sp_gsl_lookup2.update_one(
            {'_id': document['_id'],},
            {'$set': {'UK_Profit': uk_profit_rounded}}
        )
        
        print(f"Updated document with ASIN {asin}  ",document.get('_id'))



# SP ID  Lookup
def update_sp_ID_lookup(asin, row):
    update_data = {
        "UK_Buybox_Price_£": row.get('UK_Buybox_Price'),
        "UK_FBA_Fees_£": row.get('UK_FBA_Fees'),
        "UK_Variable_Closing_Fee_£": row.get('UK_Variable_Closing_Fee'),
        "UK_Referral_Fee_£": row.get('UK_Referral_Fee'),
        "time_date_stamp": datetime.now()
    }
    # Perform update
    result = sp_ID_lookup.update_many(
        {"asin": asin, "to_be_removed": {"$ne": "Y"}, "gsl_code": "A"},
        {"$set": update_data}
    )
    print(f"Updated {result.matched_count} documents for ASIN: {asin}")

def update_sp_ID_lookup_Profit(asin):
    documents = sp_ID_lookup.find({'asin': asin, 'to_be_removed': {'$ne': 'Y'}, "gsl_code": "A"})
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
        sp_ID_lookup.update_one(
            {'_id': document['_id'],},
            {'$set': {'UK_Profit': uk_profit_rounded}}
        )
        
        print(f"Updated document with ASIN {asin}  ",document.get('_id'))



# def process_batch(batch):
#     for row in batch:
#         asin = row.get('ASIN')
#         if not asin:
#             continue  # Skip rows without ASIN

#         # Group 1
#         update_sp_upc_lookup(asin, row)
#         calculate_sp_upc_lookup_Profit(asin)

#         # Group 2
#         update_sp_upc_lookup_2(asin, row)
#         calculate_sp_upc_lookup_2_Profit(asin)
        
#         # Group 3
#         update_sp_gsl_lookup_2(asin,row)
#         update_sp_gsl_lookup_2_Profit(asin)
        
#         # Group 4
#         update_sp_ID_lookup(asin, row)
#         update_sp_ID_lookup_Profit(asin)

        
def process_batch(batch):
    with open("batch_processing_times.txt", "a") as log_file:
        for row in batch:
            asin = row.get('ASIN')
            if not asin:
                continue  # Skip rows without ASIN

            # Group 1
            start_time = time.time()
            update_sp_upc_lookup(asin, row)
            calculate_sp_upc_lookup_Profit(asin)
            end_time = time.time()
            duration_group1 = end_time - start_time
            log_file.write(f"Group 1 processed in {duration_group1:.2f} seconds for ASIN {asin}\n")

            # Group 2
            start_time = time.time()
            update_sp_upc_lookup_2(asin, row)
            calculate_sp_upc_lookup_2_Profit(asin)
            end_time = time.time()
            duration_group2 = end_time - start_time
            log_file.write(f"Group 2 processed in {duration_group2:.2f} seconds for ASIN {asin}\n")

            # Group 3
            start_time = time.time()
            update_sp_gsl_lookup_2(asin, row)
            update_sp_gsl_lookup_2_Profit(asin)
            end_time = time.time()
            duration_group3 = end_time - start_time
            log_file.write(f"Group 3 processed in {duration_group3:.2f} seconds for ASIN {asin}\n")

            # Group 4
            start_time = time.time()
            update_sp_ID_lookup(asin, row)
            update_sp_ID_lookup_Profit(asin)
            end_time = time.time()
            duration_group4 = end_time - start_time
            log_file.write(f"Group 4 processed in {duration_group4:.2f} seconds for ASIN {asin}\n")


def fetch_and_update_sp_upc_lookup():
    try:
        uk_daily_data_cursor = uk_daily_data.find()
        batch = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []

            for row in uk_daily_data_cursor:
                batch.append(row)
                if len(batch) >= BATCH_SIZE:
                    futures.append(executor.submit(process_batch, batch))
                    batch = []

            if batch:
                futures.append(executor.submit(process_batch, batch))

            for future in as_completed(futures):
                future.result()  # Ensure exceptions are raised

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("============Update completed successfully SP_UPC_LOOKUP from Daily Data =============")



if __name__ == "__main__":
    fetch_and_update_sp_upc_lookup()
