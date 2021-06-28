import numpy as np

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
        input_ids_list: list, default = None
            The list of IDs in the input to be considered as one bundle.
            If None, all non-zero values are considered.
        input_mode: {'separate', 'bundle'}
            If separate, all values in input_ids_list are measured separately.
            If bundle, all values in input_ids_list are considered as one ROI.
        base_ids_list: list
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
        overlap_list = [x / count_base for x in count_input_list]
        
    elif basis == 'input':
        overlap_list = [x/y for x, y in zip(count_overlap_list, count_input_list)]
    
    return overlap_list