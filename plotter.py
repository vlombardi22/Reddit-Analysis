
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

"""
in degree plot for hubs and authorities
"""
csv_file = 'title_reddit_sorted.csv'
csv_table = pd.read_table(csv_file, sep=',', header="infer")
G = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT'], create_using=nx.MultiDiGraph())

edge_list = []
count = 0
for n in G.in_edges:
    print(count)
    count += 1
    data = G.get_edge_data(n[0], n[1]).values()
    for d in data:
        if d['LINK_SENTIMENT'] == -1:
            edge_list.append(n)

gtemp = nx.from_edgelist(edge_list, nx.MultiDiGraph)

nlist = gtemp.nodes(False)
mlist = {}
sorted_dict = {}
count = 0
for n in nlist:
    print(count)
    count += 1
    mlist[n] = int(gtemp.in_degree(n))

sorted_values = sorted(mlist.values())  # Sort the values

count = 0

for i in sorted_values:
    print(count)
    count += 1
    for k in mlist.keys():
        if mlist[k] == i:
            sorted_dict[k] = mlist[k]
            break

G2 = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                             edge_attr=['LINK_SENTIMENT'], create_using=nx.DiGraph())
hub_list = []
auth_list = []
count = 0
hubs, authorities = nx.hits(G2, normalized=False)
for n in sorted_dict.keys():
    print(count)
    count += 1
    hub_list.append(hubs[n])
    auth_list.append(authorities[n])

plt.figure(num="Graph")
lb1 = "hubs"
lb2 = "authorities"
plt.plot(np.arange(1, len(hub_list) + 1), hub_list, 'x-b', label=lb1)
plt.plot(np.arange(1, len(auth_list) + 1), auth_list, 'o-r', label=lb2)
plt.legend(['out', 'in'], loc='upper left')
plt.xlabel('negative in edges')
plt.ylabel('scores')
plt.legend()
plt.show()



"""
out degree plot for hubs and authorities
"""

"""
csv_file = 'title_reddit_sorted.csv'
csv_table = pd.read_table(csv_file, sep=',', header="infer")
G = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT'], create_using=nx.MultiDiGraph())

edge_list = []
count = 0
for n in G.out_edges:
    print(count)
    count += 1
    data = G.get_edge_data(n[0], n[1]).values()
    for d in data:
        if d['LINK_SENTIMENT'] == -1:
            edge_list.append(n)

gtemp = nx.from_edgelist(edge_list, nx.MultiDiGraph)

nlist = gtemp.nodes(False)
mlist = {}
sorted_dict = {}
count = 0
for n in nlist:
    print(count)
    count += 1
    mlist[n] = int(gtemp.out_degree(n))

sorted_values = sorted(mlist.values())  # Sort the values

count = 0

for i in sorted_values:
    print(count)
    count += 1
    for k in mlist.keys():
        if mlist[k] == i:
            sorted_dict[k] = mlist[k]
            break

G2 = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                             edge_attr=['LINK_SENTIMENT'], create_using=nx.DiGraph())
hub_list = []
auth_list = []
count = 0
hubs, authorities = nx.hits(G2, normalized=False)
for n in sorted_dict.keys():
    print(count)
    count += 1
    hub_list.append(hubs[n])
    auth_list.append(authorities[n])

plt.figure(num="Graph")
lb1 = "hubs"
lb2 = "authorities"
plt.plot(np.arange(1, len(hub_list) + 1), hub_list, 'x-b', label=lb1)
plt.plot(np.arange(1, len(auth_list) + 1), auth_list, 'o-r', label=lb2)
plt.legend(['out', 'in'], loc='upper left')
plt.xlabel('negative out edges')
plt.ylabel('scores')
plt.legend()
plt.show()
"""