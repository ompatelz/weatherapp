import json
import os

geojson_path = r'c:\Users\Om Patel\Videos\Projects\Energy Website\web\backend\data\power_plants.geojson'
if not os.path.exists(geojson_path):
    print(f'Error: {geojson_path} not found')
    exit(1)

with open(geojson_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

missing_total = 0
missing_capacity = 0
missing_operator = 0
missing_both = 0

plants_to_fix = []

for f in data['features']:
    props = f['properties']
    name = props.get('name', 'Unknown')
    cap = props.get('capacity_mw')
    op = props.get('operator')
    
    # Handle various "missing" states
    is_cap_missing = False
    if cap is None or cap == 0 or cap == 'Unknown':
        is_cap_missing = True
    elif isinstance(cap, str) and cap.strip().lower() == 'unknown':
        is_cap_missing = True
    
    is_op_missing = False
    if op is None or op == 'Unknown' or op == '':
        is_op_missing = True
    elif isinstance(op, str) and op.strip().lower() == 'unknown':
        is_op_missing = True
    
    if is_cap_missing or is_op_missing:
        missing_total += 1
        plants_to_fix.append({
            'name': name,
            'osm_id': props.get('osm_id'),
            'capacity_mw': cap,
            'operator': op,
            'state': props.get('state'),
            'type': props.get('type')
        })
        
        if is_cap_missing and is_op_missing:
            missing_both += 1
        elif is_cap_missing:
            missing_capacity += 1
        else:
            missing_operator += 1

print(f'Total Plants: {len(data["features"])}')
print(f'Plants with missing info: {missing_total}')
print(f'  - Missing Capacity Only: {missing_capacity}')
print(f'  - Missing Operator Only: {missing_operator}')
print(f'  - Missing Both: {missing_both}')

# Save the list of plants to fix
output_path = r'plants_missing_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(plants_to_fix, f, indent=2)
print(f'\nList of {len(plants_to_fix)} plants saved to {output_path}')
