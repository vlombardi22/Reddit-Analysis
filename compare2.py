import pandas as pd
import networkx as nx

"""
helpers are helped
"""

G = nx.from_pandas_edgelist(pd.read_table('title_reddit_sorted.csv', sep=',', header="infer"),
                            source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT'], create_using=nx.MultiDiGraph())

out_list = []
in_list = []
count = 0
for n in G.out_edges():
    data = G.get_edge_data(n[0], n[1]).values()
    print(count)
    count += 1
    for d in data:

        if d['LINK_SENTIMENT'] == 1:
            if len(out_list) < 54075:
                if n[0] not in out_list:
                    out_list.append(n[0])
            if len(in_list) < 54075:
                if n[1] not in in_list:
                    in_list.append(n[1])

count = 0
for n in out_list:
    if n in in_list:
        count += 1
print("helpers are helped")
print((count / len(out_list)) * 100)
