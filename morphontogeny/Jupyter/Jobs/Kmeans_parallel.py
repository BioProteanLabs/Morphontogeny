import numpy as np
import concurrent.futures as cf
from sklearn.cluster import KMeans

# Loading the principal components array
X = np.load('/data/bioprotean/ABA/DLSC/pos_std/code_100.npy')

# List of numbers
numbers_list = list(range(1,50))
# add = 594
# numbers_list.append(add)

def Kmeans_parallel(n):
    # Running K-means clustering
    kmeans = KMeans(init='k-means++', n_clusters=n, random_state=0)
    kmeans.fit_predict(X)
    
    # Reshaping and saving the array
    arr = kmeans.labels_.reshape(67,58,41)
    np.save('/data/bioprotean/ABA/DLSC/pos_std/Kmeans_labels/'+str(n)+'_clusters.npy', arr)
    
with cf.ProcessPoolExecutor() as executor:
    results = executor.map(Kmeans_parallel, numbers_list)