import pandas as pd
import json
from bson import ObjectId

# Load the Excel file
file_path = 'data.xlsx'
xls = pd.ExcelFile(file_path)

# Load the UK_Daily_Data sheet
uk_daily_data_df = pd.read_excel(xls, sheet_name='UK_Daily_Data')

# Define the base structure for the MongoDB model
base_model = {
    "_id": None,
    "ASIN": None,
    "AMZ_Marketplace": None,
    "UK_Average_BSR_30d": None,
    "UK_Average_BSR_90d": None,
    "UK_BSR": None,
    "UK_BSR%": None,
    "UK_Buybox_Price_£": None,
    "UK_Competitive_Sellers": None,
    "UK_FBA_Fees_£": None,
    "UK_FBA_Offers": None,
    "UK_FBM_Offers": None,
    "UK_Lowest_Price_FBA_£": None,
    "UK_Lowest_Price_FBM_£": None,
    "UK_Number_Variations": None,
    "UK_Referral_Fee_£": None,
    "UK_Sales_per_Month": None,
    "UK_Total_Offers": None,
    "UK_Units_per_Month": None,
    "UK_Variable_Closing_Fee_£": None,
    "UK_No_reviews": None,
    "UK_Review_Rating": None,
    "UK_Time_Datestamp": None
}

# Generate the JSON data from the UK_Daily_Data sheet
json_data = []

for index, row in uk_daily_data_df.iterrows():
    item = base_model.copy()
    item["_id"] = {"$oid": str(ObjectId())}  # Generate a unique ObjectId
    item["ASIN"] = row.get("ASIN")
    item["UK_Buybox_Price_£"] = row.get("UK_Buybox_Price_£")
    item["UK_FBA_Fees_£"] = row.get("UK_FBA_Fees_£")
    item["UK_Variable_Closing_Fee_£"] = row.get("UK_Variable_Closing_Fee_£")
    item["UK_Referral_Fee_£"] = row.get("UK_Referral_Fee_£")
    json_data.append(item)

# Convert to JSON format
json_output = json.dumps(json_data, indent=2)

# Save to a file
with open('uk_daily_data.json', 'w') as json_file:
    json_file.write(json_output)

print("JSON file has been created successfully.")
