
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']

def update_data():
    try:
        # Define the filter criteria
        query = {
            "gsl_code": { "$nin": ["D", "Z"] },
            "BSR_150_Plus": { "$ne": "Y" },
            "To_Be_Scraped": { "$ne": "Y" }
        }
        
        # Define the update operation
        update = { "$set": { "To_Be_Scraped": "Y" } }
        
        # Update documents that match the criteria
        collection = db['master_asin_upc']
        result = collection.update_many(query, update)
        
        # Print the number of documents updated
        print(f"Number of documents updated: {result.modified_count}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the update_data function
update_data()