import sys
import json
import pandas as pd

# Function to multiply binary indicators by weights
def multiply_columns(column, weights):
    return column * weights

filename = sys.argv[1]
with open('input/{}'.format(filename)) as f:
    data = json.loads(f.read())

description = data['description']
timestamp = pd.to_datetime(data['timestamp']).strftime('%Y%m%d')

items = pd.json_normalize(data, record_path =['items']).set_index('item')
items['weights'] = (items.cost + items.adjustment)/items['contributors'].str.len()
df = items[['weights']].join(items.contributors.str.join('|').str.get_dummies())
df = df.apply(lambda x: multiply_columns(x, df['weights'])).drop('weights', axis=1)
df.loc['total']= df.sum()
print(df)
df.to_csv('output/{}-{}.csv'.format(description,timestamp))
