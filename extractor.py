import pandas as pd
import networkx as nx

csv_file = 'title_reddit_sorted.csv'
csv_table = pd.read_table(csv_file, sep=',', header="infer")
G = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT'], create_using=nx.MultiDiGraph())

out_list_P = []
out_list_N = []
in_list_P = []
in_list_N = []

for n in G.out_edges:

    data = G.get_edge_data(n[0], n[1]).values()
    for d in data:
        if d['LINK_SENTIMENT'] == 1:
            out_list_P.append(n)
        elif d['LINK_SENTIMENT'] == -1:
            out_list_N.append(n)

for n in G.in_edges:
    data = G.get_edge_data(n[0], n[1]).values()
    for d in data:
        if d['LINK_SENTIMENT'] == 1:
            in_list_P.append(n)
        elif d['LINK_SENTIMENT'] == -1:
            in_list_N.append(n)

POG = nx.from_edgelist(out_list_P, nx.MultiDiGraph)
NOG = nx.from_edgelist(out_list_N, nx.MultiDiGraph)
PI = nx.from_edgelist(in_list_P, nx.MultiDiGraph)
NI = nx.from_edgelist(in_list_N, nx.MultiDiGraph)
templist = []


def top_ten_out(graph1, graph2, p1, p2):
    nlist = graph1.nodes(False)
    mlist = {}
    altlist = {}
    for n in nlist:
        mlist[n] = int(graph1.out_degree(n))
    alist = graph2.nodes(False)
    for n in alist:
        altlist[n] = int(graph2.out_degree(n))
    sorted_values = sorted(mlist.values())  # Sort the values
    printer(sorted_values, mlist, altlist, p1, p2)


def top_ten_in(graph1, graph2, p1, p2):
    nlist = graph1.nodes(False)
    mlist = {}
    altlist = {}
    for n in nlist:
        mlist[n] = int(graph1.in_degree(n))

    alist = graph2.nodes(False)
    for n in alist:
        altlist[n] = int(graph2.in_degree(n))
    sorted_values = sorted(mlist.values())  # Sort the values
    printer(sorted_values, mlist, altlist, p1, p2)


def printer(sorted_values, mlist, altlist, p1, p2):
    sorted_dict = {}
    count = 0

    for i in sorted_values:
        for k in mlist.keys():
            if mlist[k] == i:
                count += 1
                sorted_dict[k] = mlist[k]
                break

    for n in list(reversed(list(sorted_dict)))[0:20]:

        if n not in templist:
            templist.append(n)
        print(n, " ", p1, " ", sorted_dict[n], " ", p2, " ", altlist[n])


print("out degree positive!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
top_ten_out(POG, NOG, "positive", "negative")
print("out degree negative!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
top_ten_out(NOG, POG, "negative", "positive")
print("in degree positive!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
top_ten_in(PI, NI, "positive", "negative")
print("in degree negative!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
top_ten_in(NI, PI, "negative", "positive")

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("unique subreddits from the above list")
for n in templist:
    print(n)
