import numpy as np
import matplotlib.pyplot as plt

def plot_regions_DICE(region_ids_list, cluster_path):
    '''
    Plotting DICE score for brain regions over cluster numbers.
    
    Args:        
        region_ids_list: list
            List of brain region IDs to visualize.
        
        cluster_path: str
            The path to the cluster file.
    
    Returns:
        plot
    '''
    
    # List of K values
    number_range = list(range(1,50))
    ext_range = list(range(50,551,50))
    last_number = 594
    number_range.extend(ext_range)
    number_range.append(last_number)

    # Number of values in the range
    len_range = len(number_range)

    # Loading the anatomy file
    ant_file = '/data/bioprotean/RAG2/AVG/MWT_avg/to_allen/overlap/200um/allen_annot200.nii'
    ant_vec = nifti_to_array(ant_file)
    
    # Making a dictionary to save scores
    score_dict = {}

    for count, ID in enumerate(region_ids_list):
        # Selecting a brain region
        region_ID = [ID]

        # Creating an array to store overlap ratios
        score_arr = np.zeros((last_number, len_range))

        # Looping over different clusters
        for i, n_clusters in enumerate(number_range):
            # Inputting path to the cluster file
            cluster_file = cluster_path+str(n_clusters)+'_clusters.npy'
            cluster_vec = np.load(cluster_file)
            cluster_ids = list(range(n_clusters))

            # Computing the overlap for the cluster
            overlap_list = overlap_function(base_arr = ant_vec, input_arr = cluster_vec,\
            base_ids_list = region_ID, input_ids_list = cluster_ids)

            # Adding the overlap list to the array
            score_arr[:n_clusters, i] = np.array(overlap_list)

        # Adding the array to the dictionary
        score_dict[count] = score_arr
    
    # Setting the figure size
    plt.rcParams["figure.figsize"] = (7,5)

    # Initiating the plots
    fig, ax = plt.subplots()

    # Iterating over dictionary items
    for i, (j, score_arr) in enumerate(score_dict.items()):

        # List of max overlap from each column
        max_ratio_list = []

        for z in range(len_range):
            max_ratio = np.amax(score_arr[:,z])
            max_ratio_list.append(max_ratio)

        # Defining x and y
        x = number_range
        y = max_ratio_list

        # print('Maximum ratio is {} for {} clusters.\n'.format(max(y), y.index(max(y))+1))

        # Plotting the ratios
        ax.plot(x, y)

    # Setting the grid style
    sns.set(style = "darkgrid")

    # Manual set of grid values and labels
    plt.xscale('log')
    x_values = [1,10,25,50,100,200,300,400,500,594]
    ax.set_xticks(x_values)
    ax.tick_params(axis = 'both', which = 'major', labelsize = 14)

    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Number of K-means clusters", fontsize = 16)
    plt.ylabel("DICE coefficient", fontsize = 16)
    plt.title("Maximum DICE coefficient", fontsize = 16)
    plt.legend(['RegionID_'+str(ID) for ID in region_ids_list], fontsize = 10)

    # Visualizing
    plt.show()