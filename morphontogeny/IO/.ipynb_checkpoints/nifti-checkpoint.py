import numpy as np
import nibabel as nib
from scipy.spatial.distance import directed_hausdorff
import os

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
