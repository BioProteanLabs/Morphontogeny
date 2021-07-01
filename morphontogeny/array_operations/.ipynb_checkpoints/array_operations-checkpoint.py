import numpy as np

def std_vector(vector):
    '''
    Standardizes the given vector.
    
    Arguments:
        vector(vec): Input vector
    
    Returns:
        std_vector (vec): The standardized vector
    '''
    
    # The maximum value in the vector
    max_vector = np.amax(vector)
    
    # Dividing by the maximum value to standardize the vector
    std_vector = vector/max_vector
    
    return std_vector



def reconstruct_ABA (vector, array_3D = False):
    '''
    This function reconstructs the masked vector to the original shape (159326,).
    
    Args:
        vector: vec
            The masked vector
        array: bool, default = False
            if True, an array of size (67,58,41) is returned.
    
    Returns:
        output: array
            output vector/array
    '''
    
    # Loading the indices from file
    indices = np.load('/data/bioprotean/ABA/MEMMAP/genes_list/mask_indices.npy') # need to fix this at some point
    
    # Reconstructing the array
    output = np.zeros(159326,)
    output[indices] = vector
    
    # If 3D array is favored
    if array_3D == True:
        output = output.reshape(67,58,41)
    
    return output