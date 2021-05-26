import numpy as np
import concurrent.futures as cf
from sklearn.decomposition import KernelPCA

# Loading the voxel * gene matrix
X = np.load('/data/bioprotean/ABA/MEMMAP/genes_list/genes_half_mask_pos_std.npy')

# List of numbers
# numbers_list = list(range(50,551,50))
# add = 594
# numbers_list.append(add)
numbers_list = [31512]

for n in numbers_list:
    # Running K-means clustering
    kpca = KernelPCA(n_components=n, kernel='poly', degree=2, fit_inverse_transform=True, random_state=0, n_jobs=-1)
    components = kpca.fit_transform(X)
    lambdas = kpca.lambdas_
    alphas = kpca.alphas_
    dual_coef = kpca.dual_coef_
    transformed_fit = kpca.X_transformed_fit_

    # Reshaping and saving the array
    np.save('/data/bioprotean/ABA/KernelPCA/poly2/'+str(n)+'_components.npy', components)
    np.save('/data/bioprotean/ABA/KernelPCA/poly2/'+str(n)+'_lambdas.npy', lambdas)
    np.save('/data/bioprotean/ABA/KernelPCA/poly2/'+str(n)+'_alphas.npy', alphas)
    np.save('/data/bioprotean/ABA/KernelPCA/poly2/'+str(n)+'_dual_coef.npy', dual_coef)
    np.save('/data/bioprotean/ABA/KernelPCA/poly2/'+str(n)+'_transformed_fit.npy', transformed_fit)