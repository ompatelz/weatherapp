import json
import re
import ast
import os

with open('c:/Users/Om Patel/Videos/Projects/Energy Website/india_energy_scraper/extracted_capacities.json', 'r') as f:
    real_caps = json.load(f)

normalized = {}
for k, v in real_caps.items():
    key = k.replace(' ', '_').replace('&', 'and')
    normalized[key] = v

with open('c:/Users/Om Patel/Videos/Projects/Energy Website/web/backend/services/mock_data.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
current_state = None

for i, line in enumerate(lines):
    m = re.search(r'\"([a-z_]+)\":\s*\{', line)
    if m:
        current_state = m.group(1)
        
    if current_state and '2026: {' in line:
        try:
            dict_str = line.split('2026: ')[1].split('},')[0] + '}'
            breakdown = ast.literal_eval(dict_str)
            mock_total = sum(breakdown.values())
            
            lookup_key = current_state
            if lookup_key == 'andaman_nicobar': lookup_key = 'andaman_and_nicobar_islands'
            
            real_total = normalized.get(lookup_key, normalized.get(lookup_key.replace('_', ' ')))
            if real_total and mock_total > 0:
                scale = real_total / mock_total
                new_breakdown = {k: int(v * scale) for k, v in breakdown.items()}
                diff = int(real_total) - sum(new_breakdown.values())
                if 'solar' in new_breakdown: new_breakdown['solar'] += diff
                
                # replace
                new_str = '            2026: ' + json.dumps(new_breakdown).replace('\"', '\'') + ','
                lines[i] = new_str
        except Exception as e:
            pass

with open('c:/Users/Om Patel/Videos/Projects/Energy Website/web/backend/services/mock_data.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Done syncing capacities!')
