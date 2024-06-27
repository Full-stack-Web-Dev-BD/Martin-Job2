import pandas as pd
import json
from bson import ObjectId

# Load the Excel file
file_path = 'data.xlsx'
xls = pd.ExcelFile(file_path)

# Load the US_Daily_Data sheet
us_daily_data_df = pd.read_excel(xls, sheet_name='US_Daily_Data')

# Define the base structure for the MongoDB model
base_model = { 
  "_id":None,
  "ASIN": None,
  "AMZ_Marketplace": None,
  "US_Average_BSR_30d": None,
  "US_Average_BSR_90d": None,
  "US_BSR": None,
  "US_BSR%": None,
  "US_Buybox_Price_£": None,
  "US_Competitive_Sellers": None,
  "US_FBA_Fees_£": None,
  "US_FBA_Offers": None,
  "US_FBM_Offers": None,
  "US_Lowest_Price_FBA_£": None,
  "US_Lowest_Price_FBM_£": None,
  "US_Number_Variations": None,
  "US_Referral_Fee_£": None,
  "US_Sales_per_Month": None,
  "US_Total_Offers": None,
  "US_Units_per_Month": None,
  "US_Variable_Closing_Fee_£": None,
  "US_No_reviews": None,
  "US_Review_Rating": None,
  "US_Time_Datestamp": None
}

# Generate the JSON data from the US_Daily_Data sheet
json_data = []

for index, row in us_daily_data_df.iterrows():
    item = base_model.copy()
    item["_id"] = {"$oid": str(ObjectId())}  # Generate a unique ObjectId
    item["ASIN"] = row.get("ASIN")
    item["US_Buybox_Price_£"] = row.get("Buybox Price")
    item["US_FBA_Fees_£"] = row.get("FBA Fees")
    item["US_Variable_Closing_Fee_£"] = row.get("Variable Closing Fee")
    item["US_Referral_Fee_£"] = row.get("Referral Fee")
    json_data.append(item)

# Convert to JSON format
json_output = json.dumps(json_data, indent=2)

# Save to a file
with open('us_daily_data.json', 'w') as json_file:
    json_file.write(json_output)

print("JSON file has been created successfully.")



# US_Buybox_Price_£	
# US_FBA_Fees_£	
# US_Variable_Closing_Fee_£	
# US_Referral_Fee_£	
