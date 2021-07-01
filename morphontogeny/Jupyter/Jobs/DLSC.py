import numpy as np
import concurrent.futures as cf
from sklearn.decomposition import dict_learning_online

# -1s to 0s, and scaled
# Masked for voxels inside the brain using annotations
X = np.load('/data/bioprotean/ABA/MEMMAP/genes_list/ABA_mask_pos_std.npy')

# Defining the number of components to do DLSC
# range(start, stop, step)
n = list(range(350,1001,50))

for i in n:
    # Creating a DLSC instance and computing it
    dict_learner = dict_learning_online(X, n_components=i, alpha = 0.1, return_code=True, n_jobs=-1, \
random_state=42)
    
    # Saving to file
    np.save('/data/bioprotean/ABA/DLSC/mask/code_'+str(i)+'.npy', dict_learner[0])
    np.save('/data/bioprotean/ABA/DLSC/mask/dictionary_'+str(i)+'.npy', dict_learner[1])