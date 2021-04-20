import os
import sys
import json
import pandas as pd


class SplitCo():
    def __init__(self):
        super().__init__()

        self.basepath = os.getcwd()
        self.input_dir = os.path.join(self.basepath,'input')
        self.output_dir = os.path.join(self.basepath,'output')
        self.input_file = 'receipt-template.json'
        self.description = self.get_description()
        self.time_stamp = self.get_timestamp()

    def file_open(self):
        with open(os.path.join(self.input_dir, self.input_file)) as f:
            return json.loads(f.read())

    def get_description(self):
        json_data = self.file_open()
        return json_data['description']

    def get_timestamp(self):
        json_data = self.file_open()
        return pd.to_datetime(json_data['timestamp']).strftime('%Y%m%d')

    def multiply_columns(self, column, weights):
        return column * weights

    def json_to_df(self):
        return pd.json_normalize(self.file_open(), record_path =['items']).set_index('item')

    def split_costs(self):
        items = self.json_to_df()
        items['weights'] = (items.cost + items.adjustment)/items['contributors'].str.len()
        df = items[['weights']].join(items.contributors.str.join('|').str.get_dummies())
        df = df.apply(lambda x: self.multiply_columns(x, df['weights'])).drop('weights', axis=1)
        df.loc['total']= df.sum()
        return df


if __name__ == "__main__":
    split = SplitCo()
    split.input_file = sys.argv[1] 
    print(split.split_costs())

