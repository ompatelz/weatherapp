import json
import urllib.request

try:
    with open('c:/Users/Om Patel/Videos/Projects/Energy Website/india_energy_scraper/extracted_capacities.json', 'r') as f:
        real_caps = json.load(f)

    real_dict = {}
    for key, val in real_caps.items():
        k = key.replace(' ', '_').replace('&', 'and')
        if k == 'andaman_and_nicobar_islands': k = 'andaman_nicobar'
        if k == 'chhatisgarh': k = 'chhattisgarh'
        real_dict[k] = val

    states_data = json.loads(urllib.request.urlopen('http://localhost:8000/api/states').read())
    
    print(f'{"State":<25}| {"System (MW)":<15}| {"Actual (MW)":<15}| {"Diff":<10}')
    print('-'*70)

    mismatches = []

    for state_info in states_data:
        state_id = state_info['id']
        try:
            res = urllib.request.urlopen(f'http://localhost:8000/api/states/{state_id}?year=2026').read()
            sys_cap = json.loads(res)['capacity']['total_mw']
            real_cap = real_dict.get(state_id, 0.0)
            
            diff = abs(sys_cap - real_cap)
            print(f'{state_id:<25}| {sys_cap:<15}| {real_cap:<15}| {diff:.2f}')
            
            if diff > 1.0 and real_cap > 0:
                mismatches.append(f'{state_id}: diff={diff}')
                
        except Exception as e:
            print(f'Error fetching {state_id}: {e}')

    print('-'*70)
    if mismatches:
        print('Mismatches found:', mismatches)
    else:
        print('All matching states cross-verified successfully.')

except Exception as e:
    print('Failed:', e)
