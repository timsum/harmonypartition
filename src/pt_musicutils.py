import pt_keypattern
import pt_utils

import numpy as np
   
# ALL OF THESE FUNCTIONS RETURN BINARY NOTEGROUPS. THEY ESTABLISH THE NOMINAL TONE-CENTER AS EITHER CIRCLE-FIFTHS OR CHROMATIC
# (THAT COULD BE A PARAMETER, BUT PERHAPS IT IS BETTER TO BE EXPLICIT)
def circle_ext_note_for_KPDVE(kpdve):
    '''
    np.array(5) -> int 

    returns the position in a pitch class set of the top of a chord

    F_M7
    >>> circle_ext_note_for_KPDVE(np.array([0,0,0,4,3]))
    64

    Bb M7
    >>> circle_ext_note_for_KPDVE(np.array([11,0,0,4,3]))
    128
    '''

    return pt_keypattern.get_binary_KPDVE_note(np.array([kpdve[0], kpdve[1], kpdve[2], kpdve[3], kpdve[4]]))


def chrom_ext_note_for_KPDVE(kpdve):
    '''
    np.array(5) -> int 

    returns the position in a pitch class set of the top of a chord

    F_M7
    >>> chrom_ext_note_for_KPDVE(np.array([0,0,0,4,3]))
    128

    Bb M7
    >>> chrom_ext_note_for_KPDVE(np.array([11,0,0,4,3]))
    4
    '''

    return pt_utils.f_circle_to_c_chrom(circle_ext_note_for_KPDVE(kpdve))


def circle_root_note_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns the position in a pitch class set of the root of a chord

    F_M7
    >>> circle_root_note_for_KPDVE(np.array([0,0,0,4,3]))
    2048

    Bb M7
    >>> circle_root_note_for_KPDVE(np.array([11,0,0,4,3]))
    1
    '''

    return pt_keypattern.get_binary_KPDVE_note(np.array([kpdve[0], kpdve[1], kpdve[2], 0, 0]))


def chrom_root_note_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns the position in a pitch class set of the root of a chord

    F_M7
    >>> chrom_root_note_for_KPDVE(np.array([0,0,0,4,3]))
    64

    Bb M7
    >>> chrom_root_note_for_KPDVE(np.array([11,0,0,4,3]))
    2
    '''

    return pt_utils.f_circle_to_c_chrom(circle_root_note_for_KPDVE(kpdve))


def circle_conv_lyd_center_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns the position in a pitch class set of the tonic of a conventional key

    F_M7 -> CM conventional
    >>> circle_conv_tonic_for_KPDVE(np.array([0,0,0,4,3]))
    1024

    Bb M7 -> conventional
    >>> circle_conv_tonic_for_KPDVE(np.array([11,0,0,4,3]))
    2048
    '''

    return circle_conv_tonic_for_KPDVE(np.array([kpdve[0], 0, 0, 0, 0]))


def circle_conv_tonic_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns the position in a pitch class set of the tonic of a conventional key

    F_M7 -> CM conventional
    >>> circle_conv_tonic_for_KPDVE(np.array([0,0,0,4,3]))
    1024

    Bb M7 -> conventional
    >>> circle_conv_tonic_for_KPDVE(np.array([11,0,0,4,3]))
    2048
    '''

    return circle_root_note_for_KPDVE(np.array([kpdve[0], kpdve[1], pt_utils.CONVENTION_DIST[kpdve[1]], 0, 0]))


def chrom_conv_tonic_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns the position in a pitch class set of the root of a chord

    F_M7
    >>> chrom_root_note_for_KPDVE(np.array([0,0,0,4,3]))
    64

    Bb M7
    >>> chrom_root_note_for_KPDVE(np.array([11,0,0,4,3]))
    2
    '''

    return pt_utils.f_circle_to_c_chrom(circle_conv_tonic_for_KPDVE(kpdve))


# an integer to codify function
def circle_conv_function_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns a number 0-6 for function (relative to conventional tonic)

    F_M7 -> CM conventional
    >>> circle_conv_function_for_KPDVE(np.array([0,0,0,4,3]))
    6

    F_M7
    >>> circle_conv_function_for_KPDVE(np.array([0,1,0,4,3]))
    5
    
    Bb M7
    >>> circle_conv_function_for_KPDVE(np.array([11,0,2,4,3]))
    1
    
    Bb M7
    >>> circle_conv_function_for_KPDVE(np.array([11,1,2,4,3]))
    0
    '''
    
    pitchval = pt_utils.single_bit_loc(circle_root_note_for_KPDVE(kpdve))
    pitchval -= pt_utils.single_bit_loc(circle_conv_tonic_for_KPDVE(kpdve))
    
    return pitchval % 7


if __name__ == '__main__':
    import doctest
    doctest.testmod()

