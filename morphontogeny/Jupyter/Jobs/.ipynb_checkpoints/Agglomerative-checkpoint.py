import numpy as np
import concurrent.futures as cf
from sklearn.cluster import AgglomerativeClustering

# mode: 'serial' or 'parallel'
mode = 'serial'

# Loading the principal components array
X = np.load('/data/bioprotean/ABA/KernelPCA/rbf/31512_80v_components.npy')

# List of numbers
numbers_list = list(range(1,50))
extra_list = list(range(50,551,50))
add_number = 594
numbers_list.extend(extra_list)
numbers_list.append(add_number)

def clustering_function(n):
    # Running Agglomerative clustering
    AC = AgglomerativeClustering(n_clusters=n)
    AC.fit_predict(X)
    
    # Saving the labels
    labels = AC.labels_
    labels_path = '/data/bioprotean/ABA/KernelPCA/rbf/Agglomerative/labels/'+str(n)+'_clusters.npy'
    np.save(labels_path, labels)
    
    # Saving the children
    children = AC.children_
    children_path = '/data/bioprotean/ABA/KernelPCA/rbf/Agglomerative/children/'+str(n)+'_clusters.npy'
    np.save(children_path, children)

if mode == 'parallel':
    with cf.ProcessPoolExecutor() as executor:
        results = executor.map(clustering_function, numbers_list)

elif mode == 'serial':
    for n in numbers_list:
        clustering_function(n)