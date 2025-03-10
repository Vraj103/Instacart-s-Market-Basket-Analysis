import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth 
import warnings
warnings.filterwarnings('ignore')
import sys
from itertools import combinations, groupby
from collections import Counter
from IPython.display import display

"""Helper functions

1) freq: calculates frequency for items
2) order_count: Returns number of unique orders
3) get_item_pairs: it will give us item pairs in 2
4) merge_item_stats: Returns frequency and support associated with item
5) merge_item_name: Returns name associated with item
""" 

#Here, if it's a series, we count via value_counts and if it's not a series, we convert and count it with counter 
def freq(iterable):
    if type(iterable) == pd.core.series.Series:  
        return iterable.value_counts().rename("freq")
    else: 
        return pd.Series(Counter(iterable)).rename("freq")

"Returns number of unique orders"
def order_count(order_item):
    return len(set(order_item.index))

#This generator function will get us item pairs from the orders column
def get_item_pairs(order_item, num_items=2):
    order_item = order_item.reset_index().values #Drop = true prevents us from getting an extra column
    for order_id, order_object in groupby(order_item, lambda x: x[0]):
        item_list = [item[1] for item in order_object]

        for item_pair in combinations(item_list,num_items):
            yield item_pair

"""An Example
df = pd.DataFrame({
     #"order_id": [1, 1, 1, 2, 2],
     #"item": ['apple', 'egg', 'milk', 'egg', 'milk']
})

pairs = list(get_item_pairs(df, num_items=2))
print(pairs)
print(next(get_item_pairs(orders)))"""

#Returns frequency and support associated with item
def merge_item_stats(item_pairs, item_stats):
    return (item_pairs
                .merge(item_stats.rename(columns={'freq': 'freqA', 'support': 'supportA'}), left_on='item_A', right_index=True)
                .merge(item_stats.rename(columns={'freq': 'freqB', 'support': 'supportB'}), left_on='item_B', right_index=True))

#Returns name associated with item
def merge_item_name(rules, item_name):
    columns = ['itemA','itemB','freqAB','supportAB','freqA','supportA','freqB','supportB', 
               'confidenceAtoB','confidenceBtoA','lift']
    rules = (rules
                .merge(item_name.rename(columns={'item_name': 'itemA'}), left_on='item_A', right_on='item_id')
                .merge(item_name.rename(columns={'item_name': 'itemB'}), left_on='item_B', right_on='item_id'))
    return rules[columns]
