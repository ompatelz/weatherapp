import json
import os

with open('plants_missing_data.json', 'r', encoding='utf-8') as f:
    plants = json.load(f)

large_keywords = ['super', 'thermal', 'ultra', 'mega', 'park', 'dam', 'project', 'station']
priority_plants = []

for p in plants:
    name = p.get('name', 'Unknown')
    name_lower = name.lower()
    score = 0
    for kw in large_keywords:
        if kw in name_lower:
            score += 1
    if score > 0:
        priority_plants.append({
            'score': score,
            'name': name,
            'state': p.get('state'),
            'type': p.get('type')
        })

priority_plants.sort(key=lambda x: x['score'], reverse=True)

print(f"Found {len(priority_plants)} potential priority plants.")
for p in priority_plants[:30]:
    print(f"Score: {p['score']} | Name: {p['name']} | State: {p['state']} | Type: {p['type']}")
