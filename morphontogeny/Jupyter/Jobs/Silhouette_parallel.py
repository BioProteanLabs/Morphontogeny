import numpy as np
import concurrent.futures as cf
from sklearn.metrics import silhouette_score

# Loading the principal components array
X = np.load('/data/bioprotean/ABA/DLSC/pos_std/code_100.npy')

# List of numbers
numbers_list = list(range(1,50))
extra_list = list(range(50,551,50))
add_number = 594
numbers_list.extend(extra_list)
numbers_list.append(add_number)

def Silhouette_parallel(n): 
    # Loading the labels
    cluster_path = '/data/bioprotean/ABA/DLSC/pos_std/Kmeans_labels/'+str(n)+'_clusters.npy'
    cluster = np.load(cluster_path).flatten()
    
    # Computing the score
    score = silhouette_score(X, cluster)
    np.save('/data/bioprotean/ABA/DLSC/pos_std/Silhouette/SS_'+str(n)+'.npy', score)
    
with cf.ProcessPoolExecutor() as executor:
    results = executor.map(Silhouette_parallel, numbers_list)