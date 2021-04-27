import pandas as pd
import networkx as nx

csv_file = 'title_reddit_sorted.csv'
csv_table = pd.read_table(csv_file, sep=',', header="infer")
G = nx.from_pandas_edgelist(csv_table, source='SOURCE_SUBREDDIT', target='TARGET_SUBREDDIT',
                            edge_attr=['LINK_SENTIMENT'], create_using=nx.DiGraph())
toppos = ['subredditdrama', 'bestof', 'titlegore', 'shitredditsays', 'shitpost', 'switcharoo', 'circlebroke2', 'shitamericanssay', 'drama', 'shitstatistssay', 'hailcorporate', 'fitnesscirclejerk', 'badphilosophy', 'notcirclejerk', 'gamingcirclejerk', 'conspiracy', 'evenwithcontext', 'topmindsofreddit', 'the_donald', 'botsrights']
topneg = ['subredditdrama', 'bestof', 'shitredditsays', 'shitpost', 'circlebroke2', 'drama', 'shitamericanssay', 'switcharoo', 'shitstatistssay', 'fitnesscirclejerk', 'hailcorporate', 'badphilosophy', 'gamingcirclejerk', 'evenwithcontext', 'srssucks', 'topmindsofreddit', 'botsrights', 'thebluepill', 'enoughlibertarianspam', 'shitpoliticssays']
topinpos = ['askreddit', 'pics', 'iama', 'todayilearned', 'funny', 'worldnews', 'videos', 'news', 'politics', 'gaming', 'adviceanimals', 'wtf', 'gifs', 'science', 'the_donald', 'showerthoughts', 'conspiracy', 'bitcoin', 'movies', 'mildlyinteresting']
topinneg =['askreddit', 'worldnews', 'pics', 'todayilearned', 'funny', 'videos', 'news', 'politics', 'adviceanimals', 'wtf', 'iama', 'gaming', 'gifs', 'the_donald', 'nfl', 'subredditdrama', 'conspiracy', 'tifu', 'explainlikeimfive', 'movies']

# for n in node_list:
hubs, authorities = nx.hits(G,normalized=True)
rank = nx.pagerank(G)
rank2 = nx.pagerank(G,weight="LINK_SENTIMENT")

for n in toppos:
    print(rank2[n])
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for n in topinpos:
    print(rank2[n])
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for n in topinneg:
    print(rank2[n])