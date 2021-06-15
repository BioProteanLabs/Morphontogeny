import os.path
from os import path
import numpy as np
import concurrent.futures as cf
from sklearn.cluster import KMeans

# mode: 'serial' or 'parallel'
mode = 'serial'

# List of feature numbers
features_list1 = range(50,101,50)
features_list2 = range(150,201,50)
features_list3 = range(250,301,50)
features_list4 = range(350,401,50)
features_list5 = range(450,501,50)
features_list6 = range(550,601,50)

# List of cluster numbers
numbers_list = list(range(1,50))
extra_list = list(range(50,551,50))
add_number = 594
numbers_list.extend(extra_list)
numbers_list.append(add_number)

def clustering_function(n_clusters):
    for n_features in features_list6:
        # Loading features
        features = np.load('/data/bioprotean/ABA/SFT/'+str(n_features)+'_features.npy')
        
        # Running K-means
        for n_clusters in numbers_list:
            # Checking if the file exists
            save_path = '/data/bioprotean/ABA/SFT/clusters/'+str(n_features)+'features_'+str(n_clusters)+'_clusters.npy'
            if not path.exists(save_path):
                kmeans = KMeans(n_clusters = n_clusters, n_init = 50, random_state = 0)
                kmeans.fit_predict(features)
                labels = kmeans.labels_

                # Saving the labels
                np.save(save_path, labels)

if mode == 'parallel':
    with cf.ProcessPoolExecutor() as executor:
        results = executor.map(clustering_function, numbers_list)

elif mode == 'serial':
    for n in numbers_list:
        clustering_function(n)