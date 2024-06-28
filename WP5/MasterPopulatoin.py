from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']

# Collections
collections = [
    'UK_Daily_Data',
    'US_Daily_Data',
    'asin_master_upc',
    'sp_upc_lookup',
    'sp_upc_lookup2',
    'sp_gsl_lookup2',
    'sp_ID_lookup'
]

# Target collection
website_collection = db['Website_collection']

# Helper function to check if a document should be included
def should_include_document(doc):
    if 'gsl_code' in doc and doc['gsl_code'] in ['D', 'Z']:
        return False
    if 'UK_Profit' in doc and 'US_Profit' in doc and doc['UK_Profit'] <= 0 and doc['US_Profit'] <= 0:
        return False
    if 'To_Be_Scraped' in doc and doc['To_Be_Scraped'] != 'Y':
        return False
    return True

# Helper function to merge documents
def merge_documents(existing_doc, new_doc):
    for key, value in new_doc.items():
        if key != '_id' and key != 'ASIN':
            existing_doc[key] = value
    return existing_doc

# Collect all unique ASINs from the specified collections
unique_asins = set()
for collection_name in collections:
    collection = db[collection_name]
    unique_asins.update(collection.distinct('ASIN'))

# Process each unique ASIN
for asin in unique_asins:
    merged_doc = {'ASIN': asin}
    for collection_name in collections:
        collection = db[collection_name]
        documents = collection.find({'ASIN': asin})
        for doc in documents:
            if should_include_document(doc):
                merged_doc = merge_documents(merged_doc, doc)
    # Insert the merged document into the website collection
    website_collection.insert_one(merged_doc)

print("Data migration completed successfully.")
