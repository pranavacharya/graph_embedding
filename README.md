# Ingredient recommendation  
Steps:  

Our data is case sensitive have to consider that   

Data is unsupervised -> use clustering to label the data -> use KNN on that  

1.  - [x] Standardize the data such that every column range between 0 and 1   
      - [x] Check if standardizattion was implemented  
      - [x] Store the standardize data as a seperate file    

2.  - [x] Remove edge with weight = 0   
      - [x] Check number of edges removed == number of zeros in the dataset  

3.  - [x] baseline model (base_model.py)  
      - [x] Check for null values   
      - [x] Standardize data  
      - [x] PCA implementation  
      - [x] Run ML algorothim  
      - [x] Get the accuracy  

4.  - [x] Implement Random walk - edge weight is the probability of that path(or edge).  
      - [x] Create toy bipartite graph   
      - [x] Verify random walk(without weights) and get the embeddings of toy graph   
      - [x] Tweak the algorithm to cosider weight of edges as probabilities  
      - [x] Implement random walk on toy graph using weights 
      - [x] Verify random walk and get the embeddings of toy graph    
      - [x] Implement random walk on main graph using weights  
      - [x] Save the embedding  

5. - [x] Clustering  
      - [x] For default paramters  
      - [x] Decide number of clusters  
      - [x] Get nearest neignor after clustering   
6. - [x] TSNE to cisualize data  
6. - [x] KNN (K-Nearest Neighbor)    

Reference:  
GitHub docs- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax    
