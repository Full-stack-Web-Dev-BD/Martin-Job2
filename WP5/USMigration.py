from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://alamin:1zqbsg2vBlyY1bce@cluster0.sngd13i.mongodb.net/mvp2?retryWrites=true&w=majority')
db = client['mvp2']

# Define the destination collection
UK_Daily_Data=db['A2A_Asin_Lookup']
US_Daily_Data=db['A2A_Asin_Lookup']