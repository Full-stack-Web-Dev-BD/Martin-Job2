import requests
import json

# API URL and headers
api_url = "https://app.rocketsource.io/api/v3/scans?page={}"
headers = {
    "Authorization": "Bearer 3440|CbZEnbJHKBFRadAjSWk94KiSSvwGu5WHBbG4hw0lea0c94cc",
    "Content-Type": "application/json"
}

# File names to match
file_names = ["mvp2_upc.csv", "US_DD.csv"]

# Array to store the results
results = []

# Function to get and process data from API
def get_data(page):
    response = requests.get(api_url.format(page), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for page {page}: {response.status_code}")
        return None

# Initial page
page = 1

while True:
    print(f"Fetching data for page {page}...")
    data = get_data(page)
    if not data or not data.get('data'):
        print("No more data available or failed to fetch data.")
        break
    
    # Process the data
    for item in data['data']:
        if item['name'] in file_names:
            results.append({"file_name": item['name'], "id": item['id']})
            print(f"Found matching file: {item['name']}, ID: {item['id']}")

    # Move to the next page
    page += 1

# Print the results
print("Results:")
for result in results:
    print(result)

# Save the results as a JSON file
with open('scan_ids.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

print("Results have been written to scan_ids.json")
