import requests
import os
import csv

url = "https://raw.githubusercontent.com/wri/global-power-plant-database/master/output_database/global_power_plant_database.csv"
output_path = r"c:\Users\Om Patel\Videos\Projects\Energy Website\tmp\india_power_plants_wri.csv"

print(f"Downloading WRI database from {url}...")
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Process the CSV in memory to filter for India (IND)
    lines = response.text.splitlines()
    reader = csv.DictReader(lines)
    
    india_plants = []
    for row in reader:
        if row.get('country') == 'IND':
            india_plants.append(row)
            
    if not india_plants:
        print("Error: No India plants found in the dataset.")
        exit(1)
        
    # Write filtered data to CSV
    keys = india_plants[0].keys()
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(india_plants)
        
    print(f"Successfully downloaded and filtered {len(india_plants)} plants to {output_path}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
