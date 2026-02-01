import requests
import pandas as pd
import time
import os
from datetime import datetime

# --- SETTINGS ---
API_KEY = 'f351df860eb7474f8b49f602e5a0509c'  # Replace with your actual key!
STATION_ID = '40590'  # Damen Blue Line
FILE_NAME = 'data/cta_train_data.csv'

# 1. THE PRO FIX: Create the 'data' folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
    print("Created 'data' directory!")


def fetch_arrivals():
    # URL for JSON arrival predictions
    url = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={API_KEY}&mapid={STATION_ID}&outputType=JSON"

    try:
        response = requests.get(url)
        data = response.json()

        # Pull out the "eta" (Estimated Time of Arrival) list
        if 'eta' in data['ctatt']:
            arrivals = data['ctatt']['eta']
            df = pd.DataFrame(arrivals)

            # Add a timestamp for when we collected this
            df['collection_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Save to CSV (append mode)
            df.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
            print(f"Successfully saved {len(df)} arrivals at {df['collection_time'].iloc[0]}")
        else:
            print("No trains currently approaching this station.")

    except Exception as e:
        print(f"Error: {e}")


# --- RUN EVERY 1 MINUTE ---
print("Starting Data Collection... Press Ctrl+C to stop.")
while True:
    fetch_arrivals()
    time.sleep(60)  # Wait 60 seconds before next fetch