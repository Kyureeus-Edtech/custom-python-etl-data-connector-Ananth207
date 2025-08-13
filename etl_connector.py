import os
import json
import requests
import pymongo
from dotenv import load_dotenv
from datetime import datetime, timezone

def extract_data(api_url: str, api_key: str, days: int) -> list | None:
    """
    Extracts data from the authenticated ThreatFox API endpoint.

    Args:
        api_url: The URL of the API endpoint.
        api_key: The authentication key for the API.
        days: The number of past days to query for IOCs.

    Returns:
        A list of IOC records (dictionaries) if successful, otherwise None.
    """

    print(f"🔹 [Extract] Querying ThreatFox API for IOCs from the last {days} day(s)...")
    
    headers = {
        'Auth-Key': api_key
    }
    payload = {
        'query': 'get_iocs',
        'days': days
    }

    try:
        # Use POST request with headers and a JSON payload
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # Check for HTTP errors

        response_data = response.json()

        # Check the API's own status field in the response
        if response_data.get('query_status') == 'ok':
            records_list = response_data.get('data', [])
            print(f"✅ [Extract] Data fetched successfully. Found {len(records_list)} records.")
            return records_list
        
        else:
            # Handle API-level errors (e.g., invalid key, bad query)
            error_message = response_data.get('query_status')
            print(f"❌ [Extract] API returned an error: {error_message}")
            return None


    except requests.exceptions.RequestException as e:
        print(f"❌ [Extract] Error during API request: {e}")
        return None
    except ValueError:  # Catches JSON decoding errors
        print(f"❌ [Extract] Error decoding JSON from response.")
        return None

def transform_data(data: list) -> list | None:
    """
    Transforms the raw data by adding an ingestion timestamp to each record.
    (No changes needed here)
    """
    if not data or not isinstance(data, list):
        print("🔸 [Transform] No data to transform.")
        return None
    
    print("🔹 [Transform] Adding ingestion timestamps...")
    ingestion_timestamp = datetime.now(timezone.utc)
    
    for record in data:
        record['ingestion_timestamp'] = ingestion_timestamp
        
    print(f"✅ [Transform] Transformed {len(data)} records.")
    return data

def load_data(data: list, mongo_uri: str, db_name: str, collection_name: str):
    """
    Loads the transformed data into a MongoDB collection.
    (No changes needed here)
    """
    if not data:
        print("🔸 [Load] No data to load.")
        return

    print(f"🔹 [Load] Connecting to MongoDB and loading data into '{db_name}.{collection_name}'...")
    client = None
    try:
        client = pymongo.MongoClient(mongo_uri)
        client.admin.command('ping')
        print("✅ [Load] MongoDB connection successful.")
        
        db = client[db_name]
        collection = db[collection_name]
        
        result = collection.insert_many(data)
        
        print(f"✅ [Load] Successfully inserted {len(result.inserted_ids)} documents.")
        
    except pymongo.errors.ConnectionFailure as e:
        print(f"❌ [Load] MongoDB connection failed: {e}")
    except pymongo.errors.PyMongoError as e:
        print(f"❌ [Load] An error occurred during MongoDB operation: {e}")
    finally:
        if client:
            client.close()
            print("🔹 [Load] MongoDB connection closed.")

def main():

    print("🚀 Starting ThreatFox ETL Pipeline...")
    
    load_dotenv()
    
    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("THREATFOX_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "threat_intelligence")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "threatfox_raw")

    try:
        QUERY_DAYS = int(os.getenv("QUERY_DAYS", 7))
    except (ValueError, TypeError):
        QUERY_DAYS = 7

    if not all([API_URL, API_KEY, MONGO_URI]):
        print("❌ Critical environment variables 'API_URL', 'THREATFOX_API_KEY', or 'MONGO_URI' are missing.")
        print("Please check your .env file.")
        return
    if API_KEY == "YOUR-AUTH-KEY-HERE":
        print("❌ Please replace 'YOUR-AUTH-KEY-HERE' with your actual Auth-Key in the .env file.")
        return
        
    raw_data = extract_data(API_URL, API_KEY, QUERY_DAYS)
    
    if raw_data:
        transformed_data = transform_data(raw_data)
        if transformed_data:
            load_data(transformed_data, MONGO_URI, DB_NAME, COLLECTION_NAME)
        
    print("🏁 ETL Pipeline finished.")

if __name__ == "__main__":
    main()