# Code to check if required libraries installed or not 
# if not do something



##############
''' Before uploading to carbonate check word2vec version accordingly change size and iter paramter name'''
############

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import random
from sklearn.cluster import KMeans
# from tqdm import tqdm
# from gensim.models.word2vec import Word2Vec
warnings.filterwarnings("ignore", category=FutureWarning)

#-------------------------------------------- READ DATA

kaggle = pd.read_csv('dataset/nutrition_kaggle.csv')
kaggle_copy = kaggle.copy() # copy of original data
kaggle.drop(['Unnamed: 0','serving_size'],inplace=True,axis=1)
clmns = kaggle.columns
print('Dataset loaded\n')

# Remove all unit values like sodium = 9.00 mg then we need to remove mg
# Iterate over all column and if column data type is Object then remove all string characters present in column values
for i in clmns[1:]:
    if kaggle[i].dtype == 'O':
        kaggle[i] = kaggle[i].str.replace('[a-zA-Z]', '')
    else:
        continue
#-------------------------------------------- DATA PRE PROCESSING AND GRAPH CREATION
'''EDA- still remaining'''
# Count null values in every column
(kaggle.isnull().sum(axis = 0)).sum()
kaggle = kaggle.fillna(0)
(kaggle.isnull().sum(axis = 0)).sum()
kaggle.fillna(9999,inplace=True)

'''1.1.  Standardize the data'''
kaggle[clmns[1:]] = kaggle[clmns[1:]].apply(pd.to_numeric)
kaggle[clmns[1:]]= (kaggle[clmns[1:]]-kaggle[clmns[1:]].min())/(kaggle[clmns[1:]].max()-kaggle[clmns[1:]].min())
kaggle[clmns[1:]] = kaggle[clmns[1:]].astype(str)
'''1.3.  Standardize the data'''
# kaggle.to_csv('srtandardized_dataset.csv')

''' Graph Creation'''
# Stacking
# willnot include any column wiht null values
ing_nut = kaggle.set_index('name').stack()
# edges
edges = ing_nut.index.tolist()

# ''' Approach to create Bipartite graph directly'''
B = nx.Graph()
B.add_nodes_from(kaggle['name'].tolist(), bipartite=0)
B.add_nodes_from(kaggle.columns.tolist(), bipartite=1)
B.add_edges_from(edges)
print('Bipartite graph created\n')

kaggle.set_index('name', inplace=True)
names = kaggle.index.to_list()

# Add weight to each edge
clmns = clmns[1:]
for i in names:
    for j in clmns:
        B[i][j]['weight'] = kaggle.loc[i,j]

'''2.1.  Remove Edges with weight=0 '''
edge_wgt = nx.get_edge_attributes(B,'weight')
before = len(B.edges)
print('Number of edges before removal: ',before)
B.remove_edges_from((edge for edge, weight in edge_wgt.items() if weight == '0.0'))
print('Edges with weight 0 removed')
after = len(B.edges)
print('Number of edges after removal: ',after)
print('Number of edges removed: ',before-after,'\n' )

''' 2.2. '''
# count number of zeros in the dataset
zero = ((kaggle == '0.0').sum()).sum()
zero == before-after

#-------------------------------------------- TOY GRAPH
''' 4.2. TOy graph '''
# Toy Graph
m, n = 3, 4
K = nx.complete_bipartite_graph(m, n)
print('Toy graph created\n')
### To plot the toy graph- without edge weights
# pos = {}
# pos.update((i, (i - m/2, 1)) for i in range(m))
# pos.update((i, (i - m - n/2, 0)) for i in range(m, m + n))
# fig, ax = plt.subplots()
# fig.set_size_inches(15, 4)
# nx.draw(K, with_labels=True, pos=pos, node_size=300, width=0.4)
# plt.show()

# Assign random weights to each edge- weight ranges between 0 and 1
for (u, v) in K.edges():
    K.edges[u,v]['weight'] = round(random.random(),3)
print('Toy graph weights added\n')

''' Graph Visualiation'''
# pos = {}
# pos.update((i, (i - m/2, 1)) for i in range(m))
# pos.update((i, (i - m - n/2, 0)) for i in range(m, m + n))
# fig, ax = plt.subplots()
# fig.set_size_inches(15, 4)
# labels = nx.get_edge_attributes(K,'weight')
# nx.draw(K,pos)
# nx.draw_networkx_edge_labels(K,  pos=pos, edge_labels=labels)
# plt.show()
# print('Toy graph plotted with weights\n')

#-------------------------------------------- CLASS / EMBEDDING
''' 4.1. Random walk'''
''' Professor code run''' # helper-2.ipynb used
# // TODO Need to add weights to walker
import networkx as nx
import random
import numpy as np
from typing import List
from tqdm import tqdm
from gensim.models.word2vec import Word2Vec

class DeepWalk:
    def __init__(self, window_size: int, embed_size: int, walk_length: int, walks_per_node: int):
        """
        ATTRIBUTES:  
        window_size: window size for the Word2Vec model
        embedding_size: size of the final embedding
        walk_length: length of the walk
        walks_per_node: number of walks per node
        """
        self.window_size = window_size
        self.embed_size = embed_size
        self.walk_length = walk_length
        self.walk_per_node = walks_per_node

    def get_walks(self, g: nx.Graph, use_weight: bool = False) -> List[List[str]]:
        """
        Generate all the random walks
        g: Graph
        use_weight: use edge weights as probabilioties for random walk
        """
        walks = []
        for _ in range(self.walk_per_node):
            random_nodes = list(g.nodes)
            random.shuffle(random_nodes)
            for node in tqdm(random_nodes):
              walk = [node] # node =start
              for i in range(self.walk_length):
                  neighbours = g.neighbors(walk[i])
                  neighs = list(neighbours)
                  if use_weight:
                      probabilities = [g.get_edge_data(walk[i], neig)["weight"] for neig in neighs]
                      sum_probabilities = sum(probabilities)
                      probabilities = list(map(lambda t: t / sum_probabilities, probabilities))
                      p = np.random.choice(neighs, p=probabilities)
                  else:
                      p = random.choice(neighs)
                  walk.append(p)
              walks.append(walk)
                # walks.append(self.random_walk(g=g, start=node, use_weight = use_weight))
        return walks

    def get_embedding(self, G, walks,workers=3, iter=5, **kwargs):
          kwargs["sentences"] = walks
          kwargs["min_count"] = kwargs.get("min_count", 0)
          kwargs["vector_size"] = self.embed_size
          kwargs["sg"] = 1  # skip gram
          kwargs["hs"] = 1  # deepwalk use Hierarchical Softmax
          kwargs["workers"] = workers
          kwargs["window"] = self.window_size
          kwargs["epochs"] = iter
          print("Learning embedding vectors...")
          model = Word2Vec(**kwargs)
          print("Learning embedding vectors done!")

          embeddings = {}
          for word in G.nodes():
              embeddings[str(word)] = model.wv[str(word)]
          return embeddings
#-------------------------------------------- Random walk opn toy graph

# Try the embedding in toy graph
graph = K
p = DeepWalk(2,2,2,2)
wal = p.get_walks(graph,use_weight=True)

# need to convert walk values to string datatype as by default node value are of inte type and therefore the nested 
# list items also
z1 = []
for i in wal:
  z2 = []
  for j in i:
    j = str(j)
    z2.append(j)
  z1.append(z2)

# get_embedding(K,z1)

# //TODO plot the embeddings of toy graph in 2D space- embedding_size=2'''

# wlak_length = 10 and 12

#-------------------------------------------- CLUSTERING
# //TODO to decide cluster- elbow method or sihoutte index'''


''' 5.1. Clustering '''
df_cluster = pd.DataFrame.from_dict(p.get_embedding(graph,z1), orient='index')

''' 5.2. Default clusters parameter'''
kmeans = KMeans(n_clusters=2, random_state=0).fit(df_cluster)

kmeans.labels_
