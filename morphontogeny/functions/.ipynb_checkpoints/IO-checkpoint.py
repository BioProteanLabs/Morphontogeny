import numpy as np
import nibabel as nib
from numpy import load


def get_best_cluster(structure_acronym:str, clustering_K:int, dr_method:str, filepath:str = "./data"):
    """
    Given a particular brain region and a particular k-value, returns the cluster that best fits that brain region.
    Expects a directory called "data" which contains a file "DICE_scores_master_table.csv" from which to get scores.

    params:
    structure acronym (string): the acronym for the structure you'd like to find the best fit cluster to
    clustering_K (integer): the order of clustering you'd like to find the best fit in.
    dr_method (string): the dimensionality reduction method you'd like to search for clusters in.
    filepath (string): path to the directory containing the master tables and clustering labels.
    """
    assert dr_method in ["DLSC", "PCA"]

    table_filepath = filepath + f"/DICE_scores_master_table_{dr_method}.csv"

    score_frame = pd.read_csv(filepath, index_col=0)

    # filter by region acronym and K value
    # then sort by overlap score, best first
    # then retrieve the top element of the sorted frame

    best_record = score_frame[((score_frame["structure_acronym"] == "".join(['"',structure_acronym,'"'])) & (score_frame['clustering_K'] == clustering_K))].sort_values(by="overlap_score", ascending=False).head(1)

    best_cluster_id = int(best_record.cluster_id) # get the cluster ID

    best_cluster = load(filepath + f"/Kmeans_labels_{dr_method}/{str(clustering_K)}_clusters.npy") == best_cluster_id # load the cluster

    return best_cluster


def copy_nifti_header(base, input, outfile):
    """
    Takes the NIFTI header from base file and overwrites it for the input
    (Nibabel library needed)
    
    Parameters:
        base (str): base file address, its header gets copied to input's
        input (str): input file address, its header gets replaced with base's
        outfile (str): output file address
    
    Returns:
        None
    """
    
    base_img = nib.load(base)
    
    input_img = nib.load(input)
    input_matrix = np.array(input_img.dataobj).astype('float32')
    
    copy_img = nib.Nifti1Image(input_matrix, header=base_img.header, affine=base_img.affine)
    nib.save(copy_img, outfile)


def array_to_nifti(arr, output_file, master_file = None):
    """
    Takes an array and saves it as NIFTI file in the given output address
    
    Parameters:
        arr (array): matrix of image voxels.
        output_file (string): output file path.
        master_file (str): Master file to copy header from.
    
    Returns:
        None
    """
    
    # Saving the NII with the same header as master file
    if master_file != None:
        master_img = nib.load(master_file)
        output_img = nib.Nifti1Image(arr, header = master_img.header, affine = master_img.affine)
        nib.save(output_img, output_file)
    
    # Saving NII file with a general header
    else:
        save = nib.Nifti1Image(arr, np.eye(4))
        save.header.get_xyzt_units()
        save.to_filename(os.path.join('build',output_file))


def nifti_to_array(nii_file):
    '''
    Takes an input file path (str) to the NIFTI file and returns the 3D array.
    
    Parameters:
        nii_file (str): The address to nii file
    
    Returns:
        vector (np.array): The flattened 1D array

    '''
    img = nib.load(nii_file)
    array = np.array(img.dataobj)
    
    return array


def nifti_to_vector(nii_file):
    '''
    Takes an input file address (str) to the NIFTI file and returns
    the flattened vector of the input array.
    
    Parameters:
        nii_file (str): The address to nii file
    
    Returns:
        vector (np.array): The flattened 1D array
    '''
    img = nib.load(nii_file)
    array = np.array(img.dataobj)
    vector = array.flatten()
    
    return vector


def stack_nii(path_prefix, n):
    '''
    Takes the path to NIFTI files and stacks them in rows.
    
    Parameters:
        path_prefix (str): Prefix of the path to the NIFTI file until the number,
            example: '/data/img' if the complete location is: '/data/img1.nii'
    
        n (int): Number of NIFTI files to input
    
    Returns:
        stack (array): Numpy array with n rows
    '''
    input_list = [path_prefix+str(i)+'.nii' for i in range(1,n+1)]
    stack = np.vstack([nifti_to_vector(input)[0]] for input in input_list)
    
    return stack


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


def nifti_to_npy(nifti_file, output_file):
    '''
    Takes the array of an NII file and saves as NPY file.
    
    Arguments:
        nifti_file(str): The input NII path.
        output_file(str): The output NPY file.
        
    Returns:
        None.
    '''
    arr = nifti_to_array(nifti_file)
    np.save(output_file, arr)


def reconstruct_ABA (vector, indices_file, outside_value = -1, mirror = True, array_3D = True):
    '''
    This function reconstructs the masked and/or halved
    vector to the original shape (159326,).
    
    Args:
        vector: vec
            The masked vector.
        
        indices_file: str
            The path to the indices file.
        
        outside_value: int, default = -1
            The value set for outside of brain voxels.
        
        scale = bool, default = False
            If True, the values get scaled up to avoid becoming zero.
            Used for features and values between 0 and 1.
        
        mirror: bool, default = True
            If True, the vector gets mirrored (such as half-brain cases).
        
        array_3D: bool, default = True
            if True, an array of size (67,58,41) is returned.
    
    Returns:
        output_3D: array
            output vector/array
    '''
    # Loading the indices
    indices = np.load(indices_file)
    
    # Making empty array to reconstruct the original array
    output = np.full((159326), outside_value, dtype='float32')
    
    # Reconstructing the array
    output[indices] = vector

    # Making a 3D output
    output_3D = output.reshape(67,58,41)
    
    # Mirroring the array
    if mirror == True:
        for i in range(29):
            output_3D[:,57-i,:] = output_3D[:,i,:]
    
    # If 3D array is not requested
    if array_3D == False:
        output_3D = output.flatten()
    
    return output_3D