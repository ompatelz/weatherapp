import json
import pandas as pd
from io import StringIO
import urllib.request
import re

url = 'https://en.wikipedia.org/wiki/States_of_India_by_installed_power_capacity'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    tables = pd.read_html(StringIO(html))
    
    # We found earlier that table 1 is the actual data table. 
    df = tables[1]
    df.columns = ['_'.join(str(c) for c in col).strip() if type(col) is tuple else str(col) for col in df.columns.values]
    
    wiki_data = {}
    state_col = df.columns[0]
    total_col = [c for c in df.columns if 'Total' in str(c)]
    
    if not total_col:
        total_col = df.columns[-1]
    else:
        total_col = total_col[-1]

    for index, row in df.iterrows():
        state = str(row[state_col]).strip().lower()
        if 'total' in state or 'central' in state or state == '':
            continue
            
        state = re.sub(r'\[.*?\]', '', state).replace(' ', '_').replace('&', 'and')
        if state == 'andaman_and_nicobar_islands': state = 'andaman_nicobar'
        if state == 'chhatisgarh' or state == 'chhattisgarh': state = 'chhattisgarh'
        
        try:
            val_str = str(row[total_col]).replace(',', '').replace('*', '').strip()
            # If it has a footnote inside the cell like "68509.95[2]"
            val_str = re.sub(r'\[.*?\]', '', val_str)
            wiki_data[state] = float(val_str)
        except:
            pass

    with open('extracted_capacities.json', 'r') as f:
        pdf_data = json.load(f)

    # Normalize PDF Data keys
    real_dict = {}
    for key, val in pdf_data.items():
        k = key.replace(' ', '_').replace('&', 'and')
        if k == 'andaman_and_nicobar_islands': k = 'andaman_nicobar'
        if k == 'chhatisgarh': k = 'chhattisgarh'
        real_dict[k] = val

    out_file = open('comparison_output.txt', 'w', encoding='utf-8')
    
    out_file.write(f'{"State":<25}| {"Wikipedia (MW)":<15}| {"NPP Source (MW)":<15}| {"Diff":<10}\n')
    out_file.write('-'*70 + '\n')
    
    mismatches = 0
    checked = 0
    for state, wiki_cap in wiki_data.items():
        if state in real_dict:
            checked += 1
            pdf_cap = real_dict[state]
            diff = abs(wiki_cap - pdf_cap)
            out_file.write(f'{state:<25}| {wiki_cap:<15.2f}| {pdf_cap:<15.2f}| {diff:.2f}\n')
            if diff > 10.0: # allow 10 MW float/update delay difference
                mismatches += 1
        else:
             out_file.write(f'MISSING in NPP: {state:<13}| {wiki_cap:<15.2f}\n')

    out_file.write('-'*70 + '\n')
    out_file.write(f'Found {mismatches} mismatches out of {checked} states checked.\n')
    out_file.close()
    print('Comparison written to comparison_output.txt smoothly.')

except Exception as e:
    print('Failed:', e)
