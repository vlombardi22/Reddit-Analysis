import pandas as pd
import networkx as nx

"""
helpers have been attacked
"""

G = nx.from_pandas_edgelist(pd.read_table('title_reddit_sorted.csv', sep=',', header="infer"), source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT'], create_using=nx.MultiDiGraph())

attack_list = []
help_list = []
count = 0
for n in G.out_edges():
    data = G.get_edge_data(n[0], n[1]).values()
    print(count)
    count += 1
    t1 = False
    t2 = True
    for d in data:

        if d['LINK_SENTIMENT'] == -1:
            if len(attack_list) < 54075:
                if n[1] not in attack_list:
                    attack_list.append(n[1])
            else:
                t1 = True
        else:
            if len(help_list) < 54075:
                if n[0] not in help_list:
                    help_list.append(n[0])
            else:
                t2 = True

        if t1 and t2:
            print("full")
            break


count = 0
for n in attack_list:
    if n in help_list:
        count += 1
print("helpers have been attacked")
print((count / len(help_list)) * 100)