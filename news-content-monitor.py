import requests
import csv
import re
import os
from datetime import datetime

def fetch_committee_news(committee_ids, cutoff_date):
    file_path = 'committee_news.csv'
    
    # Check what we've already saved to avoid duplicates
    existing_ids = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Assuming first column is the News ID
            existing_ids = {row[0] for row in reader if row}

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header if file is new
        if os.stat(file_path).st_size == 0:
            writer.writerow(['News ID', 'Committee ID', 'Heading', 'Teaser', 'Date Published'])

        for cttee_id in committee_ids:
            print(f"Fetching news for committee {cttee_id}...")
            url = f"https://www.parliament.uk/api/content/committee/{cttee_id}/news/"
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get('items', []):
                    val = item.get('value', {})
                    news_url = val.get('url', '')
                    
                    # Extract integer following '/news/' using regex
                    match = re.search(r'/news/(\d+)/', news_url)
                    if not match:
                        continue
                    
                    news_id = match.group(1)
                    
                    # Stop if this news ID is already in our CSV
                    if news_id in existing_ids:
                        print(f"  Reached existing record {news_id}. Stopping for this committee.")
                        break
                    
                    # Parse date and filter by cutoff
                    pub_date_str = val.get('datePublished', '')
                    # Handling the ISO format (e.g., 2026-01-23T17:34:57+00:00)
                    pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                    
                    if pub_date < cutoff_date:
                        continue

                    # Write to CSV
                    writer.writerow([
                        news_id,
                        cttee_id,
                        val.get('heading', '').strip(),
                        val.get('teaser', '').strip(),
                        pub_date_str
                    ])
                    
            except Exception as e:
                print(f"  Error fetching committee {cttee_id}: {e}")

# --- Execution ---
if __name__ == "__main__":
    # Example Inputs
    ids = [24, 100] # Add your committee IDs here
    since_date = datetime(2025, 1, 1) # Filter for news since Jan 1st, 2025
    
    fetch_committee_news(ids, since_date)
