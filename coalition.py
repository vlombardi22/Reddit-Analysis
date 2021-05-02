import pandas as pd
import networkx as nx
from datetime import timedelta

"""
file for finding attacker coalitions
"""

csv_file = 'title_reddit_sorted.csv'
G = nx.from_pandas_edgelist(pd.read_table(csv_file, sep=',', header="infer"), source='SOURCE_SUBREDDIT',
                            target='TARGET_SUBREDDIT',
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
counter = 0
teamups = 0
for n in G.out_edges:
    d = G.get_edge_data(n[0], n[1]).values()
    print(counter)
    counter += 1
    for data in d:
        id = int(data['ID'])
        if data['LINK_SENTIMENT'] == -1 and id not in id_list:
            time = time_table[id]
            id_list.append(id)
            window = time - day
            attacktotal += 1
            window2 = time + day
            alone = True
            for m in G.in_edges(n[1]):
                if m[0] != n[0]:
                    d2 = G.get_edge_data(m[0], m[1]).values()
                    for data2 in d2:
                        if data2['LINK_SENTIMENT'] == -1:
                            id2 = int(data2['ID'])
                            t = time_table[id2]
                            if (t > window) and (t < window2):
                                if id2 not in id_list:
                                    id_list.append(id2)
                                    jointattacks += 1
                                    if alone:
                                        instances += 1
                                        alone = False
                                    check = True
                                    if G.get_edge_data(m[0], n[0]):
                                        d3 = G.get_edge_data(m[0], n[0]).values()
                                        for data3 in d3:
                                            if data3['LINK_SENTIMENT'] == 1:
                                                id3 = int(data3['ID'])
                                                t2 = time_table[id3]
                                                if (t2 > time) and (t2 < window2):
                                                    if id3 not in id_list:
                                                        teamups += 1
                                                        id_list.append(id3)
                                                        check = False

                                    if check and G.get_edge_data(n[0], m[0]):
                                        d3 = G.get_edge_data(n[0], m[0]).values()
                                        for data3 in d3:
                                            if data3['LINK_SENTIMENT'] == 1:
                                                id3 = int(data3['ID'])
                                                t2 = time_table[id3]
                                                if (t2 > time) and (t2 < window2):
                                                    if id3 not in id_list:
                                                        teamups += 1
                                                        id_list.append(id3)



print("teamups:", teamups)
print(attacktotal)
print(jointattacks)
print(instances)
dif = jointattacks - instances
numattacks = attacktotal - dif
print(((instances / numattacks) * 100))
