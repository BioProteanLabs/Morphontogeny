import time
import numpy as np
import scipy
from sklearn.decomposition import KernelPCA

# Benchmarking
samples_list = [100,200,400,600,800,1000,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]
time_list = []

for n_samples in samples_list:
    # Generating random X
    X = np.random.randn(n_samples,3000)
    
    # Starting the counter
    start_time = time.time()
    
    # Running KPCA
    kpca = KernelPCA(n_components=X.shape[0], kernel='poly', degree=2, \
    fit_inverse_transform=True, random_state=0, n_jobs=-1)
    components = kpca.fit_transform(X)
    lambdas = kpca.lambdas_
    alphas = kpca.alphas_
    dual_coef = kpca.dual_coef_
    transformed_fit = kpca.X_transformed_fit_
    
    # Adding time to the list
    finish_time = time.time()
    time_list.append(finish_time - start_time)

# Exponential fit
x = np.array(samples_list)
y = np.array(time_list)
fit = scipy.optimize.curve_fit(lambda t,a,b: a*np.exp(b*t),x,y,p0=(0, 0))

x_fit = 30000
y_est = fit[0][0] * np.exp(fit[0][1] * x_fit) / (24*3600)

print('Estimated time to run for {} samples is {} days.'.format(x_fit, y_est))