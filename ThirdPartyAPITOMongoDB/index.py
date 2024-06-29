import requests
import json
import logging
from datetime import datetime

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

# Body
body = {
    "per_page": 100,
    "page": 1
}

# Function to make the POST request
def make_post_request():
    try:
        response = requests.post(API_URL, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

# Main logic
if __name__ == "__main__":
    logger.info("Making POST request to RocketSource API...")
    data = make_post_request()
    if data:
        # Print count
        count = data.get("count", 0)
        logger.info(f"Count: {count}")
        
        # Access and print data array
        data_array = data.get("data", [])
        
        # Process each item in the data array
        processed_data = []
        for item in data_array:
            processed_item = {
                "ASIN":item.get("asin"),
                "UK_Buybox_Price": item.get("buybox_price"),
                "UK_Competitive_Sellers": item.get("competitive_sellers"),
                "UK_FBA_Fees": item.get("amazon_fees", {}).get("fba_fees"),
                "UK_Lowest_Price_FBA": item.get("lowest_price_new_fba"),
                "UK_Lowest_Price_FBM": item.get("lowest_price_new_fbm"),
                "UK_FBA_Offers": item.get("new_fba_offers_count"),
                "UK_FBM_Offers": item.get("new_fbm_offers_count"),
                "UK_BSR": item.get("rank"),
                "UK_Referral_Fee": item.get("amazon_fees", {}).get("referral_fee"),
                "UK_Sales_Per_Month": item.get("sales_per_month"),
                "UK_Total_Offers": item.get("total_offers_count"),
                "UK_Units_Per_Month": item.get("units_per_month"),
                "UK_Variable_Closing_Fee": item.get("amazon_fees", {}).get("variable_closing_fee"),
                "UK_Number_Variations": item.get("number_of_variations"),
                "AMZ_Marketplace": item.get("marketplace_id"),
                "UK_Time_Datestamp": datetime.now().isoformat()
            }
            processed_data.append(processed_item)

        # Print the processed data
        logger.info("Processed Data:")
        for item in processed_data:
            logger.info(json.dumps(item, indent=4))