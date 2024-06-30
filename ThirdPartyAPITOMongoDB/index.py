import requests
import json
import logging
from datetime import datetime


from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']
UK_Daily_Data=db['UK_Daily_Data']
US_Daily_Data = db['US_Daily_Data']

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_URL = "https://app.rocketsource.io/api/v3/scans/66646"
API_KEY = "3440|CbZEnbJHKBFRadAjSWk94KiSSvwGu5WHBbG4hw0lea0c94cc"

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to make the POST request
def make_post_request(page):
    body = {
        "per_page": 100,
        "page": page
    }
    try:
        response = requests.post(API_URL, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

# UK
def add_decimal_point(number, asin):
    if number:
            
        # Convert the number to a string
        num_str = str(number)

        # Determine the number of digits
        num_digits = len(num_str)

        # Add decimal point before the last two digits
        if num_digits > 2:
            result = float(num_str[:-2] + '.' + num_str[-2:])
        elif num_digits == 2:
            result = float('0.' + num_str)
            # print(f"{asin, number}========>Danger: This is a 2-digit number.", result)
        else:
            result = float('0.0' + num_str if num_digits == 1 else '0.00')
            # print(f"{asin, number}========>Most Danger: This is a 1-digit number.", result)

        if num_digits == 3:
            # print(f"{asin, number}======>Warning: This is a 3-digit number.", result)
        return result
    else:
        return None
    
    
    
def collect_UK_data():
    page = 1
    while True:
        data = make_post_request(page)
        
        if data:
            data_array = data.get("data", [])
            
            if not data_array:
                break

            for item in data_array:
                asinID= item.get("asin"),

                processed_item = {
                    "ASIN": item.get("asin"),
                    "UK_Buybox_Price": add_decimal_point(item.get("buybox_price"), asin=asinID),                    
                    "UK_Competitive_Sellers": item.get("competitive_sellers"),
                    "UK_FBA_Fees": add_decimal_point(item.get("amazon_fees", {}).get("fba_fees"), asin=asinID),                    
                    "UK_Lowest_Price_FBA": add_decimal_point(item.get("lowest_price_new_fba"), asin=asinID),                    
                    "UK_Lowest_Price_FBM": add_decimal_point(item.get("lowest_price_new_fbm"), asin=asinID),                    
                    "UK_FBA_Offers": item.get("new_fba_offers_count"),
                    "UK_FBM_Offers": item.get("new_fbm_offers_count"),
                    "UK_BSR": item.get("rank"),
                    "UK_Referral_Fee": add_decimal_point(item.get("amazon_fees", {}).get("referral_fee"), asin=asinID),                    
                    "UK_Sales_Per_Month":add_decimal_point(item.get("sales_per_month"), asin=asinID),                    
                    "UK_Total_Offers": item.get("total_offers_count"),
                    "UK_Units_Per_Month": item.get("units_per_month"),
                    "UK_Variable_Closing_Fee": item.get("amazon_fees", {}).get("variable_closing_fee"),
                    "UK_Number_Variations": item.get("number_of_variations"),
                    "AMZ_Marketplace": item.get("marketplace_id"),
                    "UK_Time_Datestamp": datetime.now().isoformat()
                }
                
                # Insert the processed_item into MongoDB
                UK_Daily_Data.insert_one(processed_item)
                # Print the ASIN code of the inserted item
                # print(f"Inserted ASIN: {processed_item['ASIN']}")
                # print(processed_item)
            
            # Increment the page number
            page += 1
        else:
            break

        
collect_UK_data()

def calculate_US_conversion(arg):
    _usdToGbp = 0.79
    if isinstance(arg, (int, float)):
        return arg * _usdToGbp
    else:
        return None
    
    
def round_to_two_decimals(value):
    if isinstance(value, (int, float)):
        return round(value / 100, 2)
    else:
        return None

    
def collect_US_data():
    page = 1
    while True:
        logger.info(f"Making POST request to RocketSource API for page {page}...")
        data = make_post_request(page)
        
        if data:
            # Access and print data array
            data_array = data.get("data", [])
            
            if not data_array:
                logger.info(f"No more data found on page {page}. Exiting loop.")
                break

            logger.info(f"Processing page {page} data...")

            # Process each item in the data array
            for item in data_array:
                processed_item = {
                    "ASIN": item.get("asin"),                    
                    "US_BSR_Percentage": round_to_two_decimals(item.get("bsr_percentage")),
                    "US_Buybox_Price": calculate_US_conversion(round_to_two_decimals(item.get("buybox_price"))),
                    "US_Competitive_Sellers": item.get("competitive_sellers"),
                    "US_FBA_Fees":calculate_US_conversion(round_to_two_decimals(item.get("amazon_fees", {}).get("fba_fees"))),
                    "US_Lowest_Price_FBA": calculate_US_conversion(round_to_two_decimals(item.get("lowest_price_new_fba"))),
                    "US_Lowest_Price_FBM": calculate_US_conversion(round_to_two_decimals(item.get("lowest_price_new_fbm"))),
                    "US_FBA_Offers": item.get("new_fba_offers_count"),
                    "US_FBM_Offers": item.get("new_fbm_offers_count"),
                    "US_BSR": item.get("rank"),
                    "US_Referral_Fee":calculate_US_conversion(round_to_two_decimals(item.get("amazon_fees", {}).get("referral_fee"))),
                    "US_Sales_Per_Month": round_to_two_decimals(item.get("sales_per_month")),
                    "US_Total_Offers": item.get("total_offers_count"),
                    "US_Units_Per_Month": item.get("units_per_month"),
                    "US_Variable_Closing_Fee":calculate_US_conversion(round_to_two_decimals(item.get("amazon_fees", {}).get("variable_closing_fee"))) ,
                    "US_Number_Variations": item.get("number_of_variations"),
                    "US_Time_Datestamp": datetime.now().isoformat(),
                    "AMZ_Marketplace": item.get("marketplace_id"),
                }
            

                # Insert the processed_item into MongoDB
                US_Daily_Data.insert_one(processed_item)
                
                # Print the ASIN code of the inserted item
                print(f"Inserted ASIN: {processed_item['ASIN']}")
                print(processed_item)
            # Increment the page number
            page += 1
        else:
            logger.error(f"Failed to retrieve data for page {page}. Exiting loop.")
            break
      
      
# collect_US_data()