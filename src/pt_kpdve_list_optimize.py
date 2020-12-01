# OPTIMIZATION OF KPDVE LIST STRATEGIES
# A SITE FOR FURTHER RESEARCH. FOR NOW IT FUNCTIONS

import numpy as np
from operator import itemgetter

import pt_utils

SAME_WEIGHTS = np.ones(5, dtype = float)
DEFAULT_WEIGHTS = np.array([3.0, 2.0, 1.0, 1.0, 0.5]) #REALLY GOOD MATCH BETWEEN WAV AND MIDI
DEFAULT_WEIGHTS_2 = np.array([7.0, 2.0, 1.0, 1.0, 1.0]) # pretty good
POLYNOMIAL_WEIGHTS = np.array([4116.0, 343.0, 49.0, 7.0, 7.0])
KPD_ONLY = np.array([12.0, 7.0, 7.0, 0.0, 0.0]) # HMM
KPD_ONES = np.array([1.0, 1.0, 1.0, 0.0, 0.0]) 
KPD_CHEAP = np.array([2.0, 1.0, 1.0, 0.0, 0.0]) 
KPD_REVERSE = np.array([1.0, 2.0, 1.0, 0.0, 0.0]) 

KPD_POLY = np.array([588.0, 7.0, 7.0, 0.0, 0.0])
POSITIONAL = np.array([5.0, 4.0, 3.0, 2.0, 1.0]) # bad -- too little key regulation
# harder to change the key, voicing, easier to change pattern degree, and extesnions
BUTTERFLY = np.array([5.0, 3.0, 2.0, 3.0, 1.0]) #PRETTY GOOD, STILL INVERTED...
CHROMATIC = np.array([5.0, 1.0, 1.0, 3.0, 1.0])
SLIGHT_PREFERENCE = np.array([1.3, 1.2, 1.1, 1.0, 0.9])
SLIGHT_PREFERENCE_2 = np.array([1.6, 1.4, 1.2, 1.0, 0.8])
EARTH_MOVE_APPROX = ([7.0, 3.0, 3.0, 1.0, 1.0]) 

CURRENT_WEIGHTS = SLIGHT_PREFERENCE

# try to stay in numpy for this. it chould come in handy

def closest_kpdve(kpdve_list, landmark):
    '''
    
    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        a list of numpy arrays of form KPDVE
    landmark : a numpy array (5)
        an array from whose location distances are measured.

    Returns
    -------
    np.array(5)
        the closest KDPVE (to landmark, by mod_distance) from the input list
    
    >>> closest_kpdve([[0,4,0,6,0], [11,4,6,3,8], [3,4,2,4,3], [6,5,7,5,3], [0,0,0,1,1]], np.array([0,0,0,0,0]))
    array([0, 0, 0, 1, 1])
    
    >>> closest_kpdve([[0,4,0,6,0], [11,4,6,3,1], [3,4,2,4,3], [6,5,0,5,3], [0,0,0,1,1]], np.array([5,4,0,5,3]))
    array([6, 5, 0, 5, 3])
    
    '''
    if len(kpdve_list) == 0:
        return landmark ## assume no effect

    new_list = []
    for a_kpdve in kpdve_list:
        # if there's kpd match -- this is okay but a bit sub-optimal... what if another voicing gives a better, more efficient analysis?
        # then you'd have to lop through the voicings and compare... would be more stable
        if a_kpdve[0] == landmark[0] and a_kpdve[1] == landmark[1] and a_kpdve[2] == landmark[2]:
            new_list.append(np.array(a_kpdve))
        elif a_kpdve[0] == landmark[0] and a_kpdve[1] == landmark[1]:
            new_list.append(np.array(a_kpdve))
        elif a_kpdve[0] == landmark[0]:
            new_list.append(np.array(a_kpdve))
    
    if len(new_list) >= 1:
        return np.array(sort_by_mod_distance(new_list, landmark)[0])
    
    return np.array(sort_by_mod_distance(kpdve_list, landmark)[0])
    
    
def sort_by_mod_distance(kpdve_list, landmark):
    '''
    
    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        a list of numpy arrays of form KPDVE
    landmark : a numpy array (5)
        a KPDVE array from whose location distances are measured.

    Returns
    -------
    np.array(n, 5) 
        kpdve list sorted by distance from 'landmark'
        note: this is an array of lists

    >>> sort_by_mod_distance([np.array([0,4,0,6,0]), np.array([11,4,6,3,8]), np.array([3,4,2,4,3]), np.array([6,5,7,5,3]), np.array([0,0,0,1,1])], np.array([0,0,0,0,0]))
    array([array([0, 0, 0, 1, 1]), array([0, 4, 0, 6, 0]),
           array([11,  4,  6,  3,  8]), array([3, 4, 2, 4, 3]),
           array([6, 5, 7, 5, 3])], dtype=object)
    '''
    

    if len(kpdve_list) == 0:
        return  np.array([pt_utils.MODVALS])
    param = 0
    new_list = []
    for a_kpdve in kpdve_list:
        new_list.append([a_kpdve, weighted_kpdve_distance(a_kpdve, 
                                                          landmark, 
                                                          CURRENT_WEIGHTS)])
        param += 1

    sorted_array = np.array(sorted(new_list, key=itemgetter(1)), dtype=object)

    return sorted_array[:, 0]


def mod_distance(val1, val2, mod):
    '''
    (int, int, int) -> float
    
    Returns the distance between two integers in a modular space
    
    >>> mod_distance(1, 4, 7)
    3
    
    >>> mod_distance(1, 5, 7)
    3
    
    >>> mod_distance(1, 11, 12)
    2
    
    '''
    diff = abs(val2 - val1 );
    return diff if diff < mod/2 else mod - diff;


def kpdve_distance_list(kpdve_list):
    '''
    Take a list of kpdve values, and make a list of the transition distances 
    by subtracting 

    Parameters
    ----------
    kpdve_list : ndarray(5)
        a list of kpdve values in a work or performance

    Returns
    -------
    KPDVE list of transitions (1 minus the next)
    
    >>> kpdve_distance_list(np.array([5,4,3,2,1]))
    array([-1, -1, -1, -1,  4])

    '''
    
    return np.roll(kpdve_list, -1) - kpdve_list


def kpdve_distance(KPDVE1, KPDVE2):
    '''

    Parameters
    ----------
    KPDVE1 : np.array(5)
        a harmonic location
    KPDVE2 : np.array(5)
        a harmonic location

    Returns
    -------
    float
        distance in modular space between two KPDVE vectors.
   
    >>> kpdve_distance([4, 3, 0, 0, 0], [0, 0, 0, 0, 0])
    5.0
    
    >>> kpdve_distance([4, 4, 0, 4, 3], [0, 0, 0, 4, 3])
    5.0
    
    >>> kpdve_distance([0,0,0,4,3], [11, 0, 0, 2, 4])
    2.449489742783178
    
    '''

    mods = np.zeros((5))
    
    for i in range(5):
        mods[i] = mod_distance(KPDVE1[i], KPDVE2[i], pt_utils.MODVALS[i])
    
    return np.linalg.norm(mods)


def weighted_kpdve_distance(KPDVE1, KPDVE2, wieghts):
    '''

    called by 'sort_by_mod_distance' -- on the verge of being deprecated

    Parameters
    ----------
    KPDVE1 : np.array(5)
        a harmonic location
    KPDVE2 : np.array(5)
        a harmonic location
    weights: np.array(5)
        a set of weights to change distance

    Returns
    -------
    float
        distance in modular space between two KPDVE vectors.
   
    >>> kpdve_distance([4, 3, 0, 0, 0], [0, 0, 0, 0, 0])
    5.0
    
    >>> kpdve_distance([4, 4, 0, 4, 3], [0, 0, 0, 4, 3])
    5.0
    
    >>> kpdve_distance([0,0,0,4,3], [11, 0, 0, 2, 4])
    2.449489742783178
    
    '''

    mods = np.zeros((5))
    
    for i in range(5):
        mods[i] = mod_distance(KPDVE1[i], KPDVE2[i], pt_utils.MODVALS[i])
    
    return np.linalg.norm(mods * CURRENT_WEIGHTS)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
