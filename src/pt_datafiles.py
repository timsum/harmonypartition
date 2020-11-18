#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:23:28 2020

@author: timsummers
"""

import numpy as np
import pt_utils


# write and pack

def save_bin_kpd_file(filename, bin_a, kpdve_a):
    '''
    Take the binary and kpdve analyses of a file and put them into an external
    file.

    Parameters
    ----------
    filename : string 
        usually that of the notation or audio file, without extension.
    bin_a : ndarray(n,)
        a one-dimensional array of integers (notegroups).
    kpdve_a : ndarray(n, 5)
        DESCRIPTION.

    Returns
    -------
    None. writes to external file

    '''
    write_data_file(filename, pack_bin_kpdve_data_from_list_analysis(bin_a, kpdve_a))
    

def read_bin_kpd_file(filename):
    '''
    

    Parameters
    ----------
    filename : str
        the name of the _.

    Returns
    -------
    (bin_a, kpdve_a)
        an int an a numpy array.

    '''
    return unpack_bin_kpdve_data_from_packed_list(read_data_file(filename))


def pack_bin_kpdve_data_from_list_analysis(bin_a, kpdve_a):
    '''
    compress bin and kpdve data to minimal form 0bKKKKPPPDDDVVVEEEC-D-EF-G-A-B
    in an array

    Parameters
    ----------
    bin_a : a binary analysis of an audio
        DESCRIPTION.
    kpdve_a : TYPE
        DESCRIPTION.

    Returns
    -------
    a combination of the binary and kpdve values, as a list of integers.
    
    >>> pack_bin_kpdve_data_from_list_analysis(np.array([[2244]]), np.array([[0,0,0,4,3]]))
    array([145604])
    '''
    
    packed_a = np.zeros(len(bin_a), dtype=int)
    
    for i in range(bin_a.shape[0]):
        packed_a[i] = pt_utils.minimal_bin_kpdve(bin_a[i], kpdve_a[i])
        
    return packed_a


def unpack_bin_kpdve_data_from_packed_list(packed_a):
    '''
    

    Parameters
    ----------
    packed_a : a binary analysis of an audio file, probably retrieved from a file
        DESCRIPTION.

    Returns
    -------
    bin_a, kpdve_a

    >>> unpack_bin_kpdve_data_from_packed_list(np.array([145604]))
    (array([2244]), array([[0, 0, 0, 4, 3]]))
    
    '''
    
    bin_a = np.zeros(len(packed_a), dtype=int)
    kpdve_a = np.zeros((len(packed_a), 5), dtype=int)
    
    for i, pckd in enumerate(packed_a):
        bin_a[i], kpdve_a[i] = pt_utils.bin_kpdve_from_minimal(pckd)
    
    return bin_a, kpdve_a



# read/write

def write_data_file(filename, np_array):
    '''

    Parameters
    ----------
    filename : Str
        the name of the file, corresponding to the name of the original audio file

    Returns
    -------
    None.
        writes audio files to file path;

    '''
    
    savestring = filename + ".npy"
    np.save(savestring, np_array)
    
    
def read_data_file(filename):
    '''
    

    Parameters
    ----------
    filename : str
        name of the file to be read (without '.npy').

    Returns
    -------
    numpy array.

    '''
    loadstring = filename + ".npy"
    return np.load(loadstring)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    