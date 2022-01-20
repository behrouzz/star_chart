import pandas as pd

df = pd.read_csv('hip7.csv')
df = df[df['Vmag']<5]

main_ids = str(tuple(list(df['main_id'])))

script = f"""SELECT main_id, id
FROM basic
JOIN ident
ON basic.oid=ident.oidref
WHERE (main_id IN {main_ids}) AND (id LIKE 'NAME%')
"""

#print(script)


#==============================================

import json

with open('NAMEs5.json', 'r') as f:
    rows = json.load(f)['data']

cols = ['main_id', 'name']

a = pd.DataFrame(data=rows, columns=cols)
aa = a.groupby('main_id').sum()
aa = aa['name'].str.replace('NAME', '|')
aa = aa.str[2:]
aa = aa.str.replace('|', ' |')
aa = pd.DataFrame(aa).reset_index()

# Save to hip7.csv
# ----------------
df = pd.read_csv('hip7.csv')

final = pd.merge(df, aa, how='left', on='main_id')

final.set_index('hip').to_csv('hip7_with_names.csv')
