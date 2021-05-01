import pandas as pd
import networkx as nx
from datetime import timedelta

"""
checks for when two Subreddits that have been attacked come together
"""

csv_file = 'title_reddit_sorted.csv'
csv_table = pd.read_table(csv_file, sep=',', header="infer")
G = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT', 'TIMESTAMP', 'ID'], create_using=nx.MultiDiGraph())

time_table = {}
c = 0
for n in G.out_edges:
    print(c)
    c += 1
    d = G.get_edge_data(n[0], n[1]).values()
    for data in d:
        time_table[int(data['ID'])] = pd.to_datetime(data['TIMESTAMP'])
print("time loading done")

day = timedelta(days=1)
id_list = []
attacktotal = 0
jointattacks = 0
instances = 0
defence = 0
counter = 0
for n in G.out_edges:
    d1 = G.get_edge_data(n[0], n[1]).values()
    print(counter)
    counter += 1
    for data in d1:
        id = int(data['ID'])
        if data['LINK_SENTIMENT'] == -1 and id not in id_list:
            time = time_table[id]
            id_list.append(id)
            window = time - day
            attacktotal += 1
            window2 = time + day
            alone = True
            for m in G.out_edges(n[0]):
                if m[1] != n[1]:
                    d2 = G.get_edge_data(m[0], m[1]).values()
                    for data2 in d2:
                        id2 = int(data2['ID'])
                        t = time_table[id2]
                        if (t > window) and (t < window2):
                            if data2['LINK_SENTIMENT'] == -1 and id2 not in id_list:
                                id_list.append(id2)
                                jointattacks += 1
                                if alone:
                                    instances += 1
                                    alone = False

                                data3 = None
                                if G.get_edge_data(m[1], n[1]):
                                    data3 = G.get_edge_data(m[1], n[1]).values()

                                elif G.get_edge_data(n[1], m[1]):
                                    data3 = G.get_edge_data(n[1], m[1]).values()

                                if data3:
                                    for d3 in data3:
                                        id3 = d3['ID']
                                        time3 = time_table[id3]
                                        if time <= time3 < window2:
                                            if data3['LINK_SENTIMENT'] == 1:
                                                defence += 1


print(attacktotal)
print(jointattacks)
print(instances)
dif = jointattacks - instances
num_attacks = attacktotal - dif
print(((defence / num_attacks) * 100))
