import numpy as np
from sklearn.cluster import KMeans

# Loading the principal components array
X = np.load('/data/bioprotean/ABA/PCA/mask/mask_PC_80v.npy')

# List of numbers
numbers_list = list(range(1,50))
extra_list = list(range(50,551,50))
add_number = 594
numbers_list.extend(extra_list)
numbers_list.append(add_number)

for n in numbers_list:
    # Running K-means clustering
    kmeans = KMeans(n_clusters=n, random_state=0)
    kmeans.fit_predict(X)
    
    # Reshaping and saving the array
    arr = kmeans.labels_
    np.save('/data/bioprotean/ABA/PCA/mask/clusters/'+str(n)+'_clusters.npy', arr)