import pandas as pd
import networkx as nx
from datetime import timedelta

"""
checks if victims retaliate
"""

csv_file = 'title_reddit_sorted.csv'
csv_table = pd.read_table(csv_file, sep=',', header="infer")
csv_table = csv_table[csv_table['LINK_SENTIMENT'] != 1]  # get only negative edges
G = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['TIMESTAMP', 'ID'], create_using=nx.MultiDiGraph())

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
for n in G.out_edges:
    d = G.get_edge_data(n[0], n[1]).values()
    print(counter)
    counter += 1
    for data in d:
        id = int(data['ID'])

        if id not in id_list:
            time = time_table[id]
            id_list.append(id)

            attacktotal += 1
            window = time + day
            alone = True
            for m in G.out_edges(n[1]):
                if m[1] == n[0]:
                    d2 = G.get_edge_data(m[0], m[1]).values()
                    for data2 in d2:
                        id2 = int(data2['ID'])
                        t = time_table[id2]
                        if (t > time) and (t < window):

                            if id2 not in id_list:
                                id_list.append(id2)
                                jointattacks += 1
                                if alone:
                                    instances += 1
                                    alone = False

print(attacktotal)
print(jointattacks)
print(instances)
dif = jointattacks - instances
numattacks = attacktotal - dif
print(((instances / numattacks) * 100))
