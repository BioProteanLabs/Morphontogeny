import numpy as np
import concurrent.futures as cf
from sklearn.cluster import KMeans

# Loading the principal components array
X = np.load('/data/bioprotean/ABA/KernelPCA/rbf/31512_80v_components.npy')

# List of numbers
numbers_list = list(range(1,50))
# extra_list = list(range(50,551,50))
# add_number = 594
# numbers_list.extend(extra_list)
# numbers_list.append(add_number)

def Kmeans_parallel(n):
    # Running K-means clustering
    kmeans = KMeans(n_clusters=n, random_state=0)
    kmeans.fit_predict(X)
    
    # Reshaping and saving the array
    arr = kmeans.labels_
    np.save('/data/bioprotean/ABA/KernelPCA/rbf/Kmeans/'+str(n)+'_clusters.npy', arr)
    
with cf.ProcessPoolExecutor() as executor:
    results = executor.map(Kmeans_parallel, numbers_list)