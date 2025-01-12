from pymongo import MongoClient
import pandas as pd

# Connection string (replace <password> with your actual password)
connection_string = "mongodb+srv://ravisha23sharma:xWjmqRy8ymJNzyuu@cluster0.xe6ha.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(connection_string)

# Created a new database
db = client["payment_app"]  

# Created a collection
collection = db["payments"]  

# Load the normalized data from a CSV file
csv_file_path = "normalized_payment_information.csv" 
data = pd.read_csv(csv_file_path)

# Convert the DataFrame to a list of dictionaries (MongoDB's required format)
documents = data.to_dict(orient="records")

# Insert the data into the MongoDB collection
try:
    result = collection.insert_many(documents)
    print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
except Exception as e:
    print("An error occurred while inserting data into MongoDB:", e)
