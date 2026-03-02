import json
import ast
import re

with open('extracted_capacities.json', 'r') as f:
    real_caps = json.load(f)

normalized = {}
for k, v in real_caps.items():
    key = k.replace(' ', '_').replace('&', 'and')
    normalized[key] = v

with open('../web/backend/services/mock_data.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_state = None
for i, line in enumerate(lines):
    if line.strip().startswith('"') and '": {' in line and 'capacity_by_year' not in line and 'generation_by_year' not in line:
        current_state = line.strip().split('"')[1]
        
    if current_state and '2026: {' in line:
        try:
            dict_str = line.split('2026: ')[1].strip()
            if dict_str.endswith(','): dict_str = dict_str[:-1]
                
            breakdown = ast.literal_eval(dict_str)
            mock_total = sum(breakdown.values())
            
            lookup = current_state
            if lookup == 'andaman_nicobar': lookup = 'andaman_and_nicobar_islands'
            if lookup == 'chhattisgarh': lookup = 'chhatisgarh'
            
            real_total = normalized.get(lookup, normalized.get(lookup.replace('_', ' ')))
            
            if real_total and mock_total > 0:
                scale = real_total / mock_total
                new_breakdown = {k: int(v * scale) for k, v in breakdown.items()}
                diff = int(real_total) - sum(new_breakdown.values())
                if 'solar' in new_breakdown: new_breakdown['solar'] += diff
                
                lines[i] = '            2026: ' + str(new_breakdown) + ',\n'
                print('Updated', current_state, 'to', sum(new_breakdown.values()))
        except Exception as e:
            pass

with open('../web/backend/services/mock_data.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
