import numpy as np
import concurrent.futures as cf
from sklearn.cluster import KMeans

# mode: 'serial' or 'parallel'
mode = 'parallel'

# Loading the voxel * gene matrix
X = np.load('/data/bioprotean/ABA/MEMMAP/genes_list/genes_half_mask_pos_std.npy')

# List of feature numbers
features_list = range(50,601,50)

# List of cluster numbers
numbers_list = list(range(1,50))
extra_list = list(range(50,551,50))
add_number = 594
numbers_list.extend(extra_list)
numbers_list.append(add_number)

def clustering_function(n_clusters):
    for n_features in features_list:
        # Loading features
        features = np.load('/data/bioprotean/ABA/SFT/'+str(n_features)+'_features.npy')

        # Running K-means
        for n_clusters in numbers_list:
            kmeans = KMeans(n_clusters = n_clusters, n_init = 50, random_state = 0)
            kmeans.fit_predict(X)
            labels = kmeans.labels_

            # Saving the labels
            np.save('/data/bioprotean/ABA/SFT/'+str(n_features)+'features_'+str(n_clusters)+'_clusters.npy', labels)

if mode == 'parallel':
    with cf.ProcessPoolExecutor() as executor:
        results = executor.map(clustering_function, numbers_list)

elif mode == 'serial':
    for n in numbers_list:
        clustering_function(n)