import pandas as pd

hip7 = pd.read_csv('data/hip7.csv')
ot = pd.read_csv('data/otypes.csv')

df = pd.merge(hip7, ot, how='left', left_on='otype_txt', right_on='short').set_index('hip')

df.loc[df['NAME'].notnull(), 'name'] = df['main_id'] + ' | ' + df['NAME']
df.loc[df['NAME'].isna(), 'name'] = df['main_id']

del df['NAME']
del df['short']

cols = ['oid', 'main_id', 'otype_txt', 'long', 'ra', 'dec',
        'Vmag', 'plx', 'period', 'SpType', 'rgb', 'temp', 'name']

df = df[cols]

df.to_csv('data/hip7_2.csv')
