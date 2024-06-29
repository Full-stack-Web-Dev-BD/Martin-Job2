import requests
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_URL_UK = "https://app.rocketsource.io/api/v3/scans/66646"
API_URL_US = "https://app.rocketsource.io/api/v3/scans/66647"  # Adjusted for US scan ID
API_KEY = "3440|CbZEnbJHKBFRadAjSWk94KiSSvwGu5WHBbG4hw0lea0c94cc"

# Conversion rate from USD to GBP (example)
_usdToGbp = 0.75  # Replace with actual conversion rate

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to make the POST request
def make_post_request(api_url, page):
    body = {
        "per_page": 100,
        "page": page
    }
    try:
        response = requests.post(api_url, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")

# Function to process UK data item
def process_uk_item(item):
    processed_item = {
        "ASIN": item.get("asin"),
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
    return processed_item

# Function to process US data item
def process_us_item(item):
    processed_item = {
        "ASIN": item.get("asin"),
        "US_BSR_Percentage": item.get("bsr_percentage"),
        "US_Buybox_Price": item.get("buybox_price") / _usdToGbp,
        "US_Competitive_Sellers": item.get("competitive_sellers"),
        "US_FBA_Fees": item.get("amazon_fees", {}).get("fba_fees") / _usdToGbp,
        "US_Lowest_Price_FBA": item.get("lowest_price_new_fba") / _usdToGbp,
        "US_Lowest_Price_FBM": item.get("lowest_price_new_fbm") / _usdToGbp,
        "US_FBA_Offers": item.get("new_fba_offers_count"),
        "US_FBM_Offers": item.get("new_fbm_offers_count"),
        "US_BSR": item.get("rank"),
        "US_Referral_Fee": item.get("amazon_fees", {}).get("referral_fee") / _usdToGbp,
        "US_Sales_Per_Month": item.get("sales_per_month"),
        "US_Total_Offers": item.get("total_offers_count"),
        "US_Units_Per_Month": item.get("units_per_month"),
        "US_Variable_Closing_Fee": item.get("amazon_fees", {}).get("variable_closing_fee") / _usdToGbp,
        "US_Number_Variations": item.get("number_of_variations"),
        "AMZ_Marketplace": item.get("marketplace_id"),
        "US_Time_Datestamp": datetime.now().isoformat()
    }
    return processed_item

# Main logic
if __name__ == "__main__":
    uk_page = 1
    us_page = 1

    while True:
        # Process UK data
        logger.info(f"Making POST request to RocketSource API for UK, page {uk_page}...")
        uk_data = make_post_request(API_URL_UK, uk_page)
        
        if uk_data:
            # Access and process UK data array
            uk_data_array = uk_data.get("data", [])
            
            if not uk_data_array:
                logger.info(f"No more UK data found on page {uk_page}. Exiting UK loop.")
                break

            logger.info(f"Processing UK page {uk_page} data...")

            # Process each item in the UK data array
            processed_uk_data = []
            for item in uk_data_array:
                processed_uk_item = process_uk_item(item)
                processed_uk_data.append(processed_uk_item)

            # Print processed UK data
            logger.info("Processed UK Data:")
            for item in processed_uk_data:
                logger.info(json.dumps(item, indent=4))
            
            logger.info(f"UK page {uk_page} processing done.")
            logger.info("===== Starting next UK page =====")

            # Increment UK page number
            uk_page += 1
        else:
            logger.error(f"Failed to retrieve UK data for page {uk_page}. Exiting UK loop.")
            break

        # Process US data
        logger.info(f"Making POST request to RocketSource API for US, page {us_page}...")
        us_data = make_post_request(API_URL_US, us_page)
        
        if us_data:
            # Access and process US data array
            us_data_array = us_data.get("data", [])
            
            if not us_data_array:
                logger.info(f"No more US data found on page {us_page}. Exiting US loop.")
                break

            logger.info(f"Processing US page {us_page} data...")

            # Process each item in the US data array
            processed_us_data = []
            for item in us_data_array:
                processed_us_item = process_us_item(item)
                processed_us_data.append(processed_us_item)

            # Print processed US data
            logger.info("Processed US Data:")
            for item in processed_us_data:
                logger.info(json.dumps(item, indent=4))
            
            logger.info(f"US page {us_page} processing done.")
            logger.info("===== Starting next US page =====")

            # Increment US page number
            us_page += 1
        else:
            logger.error(f"Failed to retrieve US data for page {us_page}. Exiting US loop.")
            break
