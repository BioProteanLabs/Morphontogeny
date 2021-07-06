import numpy as np
from numpy import std, mean, sqrt
# Need to import IO

def overlap_function(base_arr, input_arr, input_ids_list, input_mode = 'separate',\
    base_ids_list = None, basis = 'DICE'):
    '''
    Measures the overlap between the base and values of the the input.
    The values of the input to be measured against are provided in the input_ids_list.
    Measures are based on 'DICE', 'base', or 'input'.
    
    Parameters:
        base_arr: arr
            The base array.
            
        input_arr: arr
            The input array.
            
        input_ids_list: list
            The list of IDs in the input to be considered.
            
        input_mode: {'separate', 'bundle'}
            If separate, all values in input_ids_list are measured separately.
            If bundle, all values in input_ids_list are considered as one ROI.
            
        base_ids_list: list, default = None
            The list of IDs in the base to be considered as one bundle.
            If None, all non-zero values are considered.
            
        basis: {'DICE', 'base', 'input'}
            The basis of overlap measure.
    
    Returns:
        overlap_list: list
            The list of overlap ratios.
    '''

    # Making an array of zeros with the same size
    masked_base = np.zeros_like(base_arr)
    masked_input = np.zeros_like(input_arr)

    # Masking the base based on base_ids_list
    if base_ids_list != None:
        for ID in base_ids_list:
            masked_base += np.where(base_arr == ID, 1, 0)
    
    # Converting base vector to a binary vector, in case it is not
    elif base_ids_list == None:
        masked_base = np.where(base_arr != 0, 1, 0)
    
    # Getting count of considered voxels in base
    count_base = np.sum(masked_base)

    # Creating lists to store overlap counts
    count_input_list = []
    count_overlap_list = []
    
    # Creating a list to store final overlap ratios
    overlap_list = []
    
    # Masking the input in 'bundle' mode
    if input_mode == 'bundle':
        for ID in input_ids_list:
            masked_input += np.where(input_arr == ID, 1, 0)

        # Counting the input and adding to the list
        count_input = np.sum(masked_input)
        count_input_list.append(count_input)

        # Counting the overlap and adding to the list
        count_overlap = np.vdot(masked_base, masked_input)
        count_overlap_list.append(count_overlap)

    # Measuring overlap for 'separate' mode
    elif input_mode == 'separate':
        for ID in input_ids_list:
            # Masking input for that specific ID
            masked_input = np.where(input_arr == ID, 1, 0)
            
            # Count of voxels in the ROI and adding to the list
            count_input = np.sum(masked_input)
            count_input_list.append(count_input)

            # Counting the overlap and adding to the list
            count_overlap = np.vdot(masked_base, masked_input)
            count_overlap_list.append(count_overlap)
    
    # Computing on different bases
    if basis == 'DICE':
        # Total count of base ROI and input ROI
        total_count_list = [x + count_base for x in count_input_list]
        
        # Overlap list
        overlap_list = [(2*x)/y for x, y in zip(count_overlap_list, total_count_list)]

    elif basis == 'base':
        overlap_list = [x/count_base for x in count_input_list]
        
    elif basis == 'input':
        overlap_list = [x/y for x, y in zip(count_overlap_list, count_input_list)]
    
    return overlap_list



def DICE_length_function(region_ids_list, cluster_vec):
    '''
    Plotting DICE score for brain regions over cluster numbers.
    
    Args:        
        region_ids_list: list
            List of brain region IDs to visualize.
        
        cluster_vec: vec
            The clusters vector.
    
    Returns:
        plot
    '''
    
    # Making lists to save DICE scores and length rations
    DICE_list = []
    length_list = []
    
    # Getting the number of clusters
    n_clusters = np.unique(cluster_vec).shape[0]
    cluster_ids = list(range(n_clusters))
    
    # Loading the anatomy file
    ant_file = '/data/bioprotean/RAG2/AVG/MWT_avg/to_allen/overlap/200um/allen_annot200.nii'
    ant_vec = nifti_to_array(ant_file)
    
    for count, ID in enumerate(region_ids_list):
        # Selecting a brain region
        region_ID = [ID]
        
        # Computing the overlap for the cluster
        overlap_list = overlap_function(base_arr = ant_vec, input_arr = cluster_vec,\
        base_ids_list = region_ID, input_ids_list = cluster_ids)

        # Adding the maximum DICE score to the list
        top_DICE = max(overlap_list)
        DICE_list.append(top_DICE)
        
        # Computing the length
        length = region_length(ID)
        length_list.append(length)
        
    return length_list, DICE_list



def DICE_orientation_function(region_ids_list, cluster_vec):
    '''
    Plotting DICE score for brain regions over cluster numbers.
    
    Args:        
        region_ids_list: list
            List of brain region IDs to visualize.
        
        cluster_vec: vec
            The clusters vector.
    
    Returns:
        plot
    '''
    
    # Making lists to save DICE scores and length rations
    DICE_list = []
    length_list = []
    
    # Getting the number of clusters
    n_clusters = np.unique(cluster_vec).shape[0]
    cluster_ids = list(range(n_clusters))
    
    # Loading the anatomy file
    ant_file = '/data/bioprotean/RAG2/AVG/MWT_avg/to_allen/overlap/200um/allen_annot200.nii'
    ant_vec = nifti_to_array(ant_file)
    
    for count, ID in enumerate(region_ids_list):
        # Selecting a brain region
        region_ID = [ID]
        
        # Computing the overlap for the cluster
        overlap_list = overlap_function(base_arr = ant_vec, input_arr = cluster_vec,\
        base_ids_list = region_ID, input_ids_list = cluster_ids)

        # Adding the maximum DICE score to the list
        top_DICE = max(overlap_list)
        DICE_list.append(top_DICE)
        
        # Computing the length
        length = find_orientation(ID)
        length_list.append(length)
        
    return length_list, DICE_list


def cohend_func(x,y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    
    d = (mean(x) - mean(y)) / sqrt(((nx-1)*std(x, ddof=1) ** 2 + (ny-1)*std(y, ddof=1) ** 2) / dof)
    return d


def cohen_d(stack1, stack2):
    '''
    Takes 2 arrays and computes then Cohen's d using the cohend_func function
    
    Parameters:
        stack1, stack2 (array): Arrays with subjects as rows and voxels as columns
    
    Returns:
        d (vector): Vector with size of stack1/stack2 columns
    '''
    d = np.zeros(stack1.shape[1])
    for i in range (stack1.shape[1]):
        d[i] = cohend_func(stack1[:,i], stack2[:,i])
        
    return d


def find_orientation(region_id):
    '''
    Showing the main orientation of the region.
    
    Args:
        region_id: int
            ID of the brain region.
    
    Returns:
        orientation: int
            Main orientation of the region.
    '''
    
    # Loading the Allen Reference Atlas
    allen_path = '/data/bioprotean/ABA/PCA/80_variance/allen_annot200.nii'
    reference = nifti_to_array(allen_path)
    
    # Masking the ARA for the brain region
    mask_region = np.where(reference == region_id)
    
    # Lengths in different locations
    length_0 = mask_region[0][-1] - mask_region[0][0]
    length_1 = mask_region[1][-1] - mask_region[1][0]
    length_2 = mask_region[2][-1] - mask_region[2][0]
    
    # Choosing the orientation
    length_list = [length_0, length_1, length_2]
    max_value = max(length_list)
    orientation = length_list.index(max_value)
    
    return orientation


def region_length(region_id):
    '''
    Showing the main orientation of the region.
    
    Args:
        region_id: int
            ID of the brain region.
    
    Returns:
        ratio: float
            Ratio of Sagittal/Axial length.
    '''
    
    # Loading the Allen Reference Atlas
    allen_path = '/data/bioprotean/ABA/PCA/80_variance/allen_annot200.nii'
    reference = nifti_to_array(allen_path)
    
    # Masking the ARA for the brain region
    mask_region = np.where(reference == region_id)
    
    # Lengths in different locations
    length_0 = mask_region[0][-1] - mask_region[0][0]
    length_1 = mask_region[1][-1] - mask_region[1][0]
    length_2 = mask_region[2][-1] - mask_region[2][0]
    
    # Computing the ratio
    ratio = length_0 / length_1
    
    return ratio