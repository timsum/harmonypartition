import pt_keypattern
import pt_utils

import numpy as np
   
# ALL OF THESE FIRST SET OF FUNCTIONS RETURN BINARY NOTEGROUPS. 
# THEY ESTABLISH THE NOMINAL TONE-CENTER AS EITHER CIRCLE-FIFTHS OR CHROMATIC.
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


# ======================
# THESE FUNCTIONS RETURN ARRAYS OF CHROMATIC NOTES, MAINLY FOR CREATING CONTEXT VALUES IN THE PERFORMANCE STATE.
def scale_notes_for_KPDVE(kpdve):
    '''

    Parameters
    ----------
    kpdve : np.array(5)
        a kpdve array whose notes are to be returned from the root up.

    Returns
    -------
    all the notes in the current chord, ordered ascending
    
    >>> scale_notes_for_KPDVE(np.array([0,0,0,4,3]))
    array([ 0,  2,  4,  5,  7,  9, 11])

    # harmonic major... C
    >>> scale_notes_for_KPDVE(np.array([0,4,0,4,3]))
    array([ 0,  2,  4,  5,  7,  8, 11])
    '''

    return pt_utils.bit_locs(pt_utils.f_circle_to_c_chrom(pt_keypattern.get_binary_KP(kpdve[0], kpdve[1])))


def ordered_chord_notes_for_KPDVE(kpdve):
    '''

    Parameters
    ----------
    kpdve : np.array(5)
        a kpdve array whose notes are to be returned from the root up.

    Returns
    -------
    an array of notes, root first.
    
    >>> ordered_chord_notes_for_KPDVE(np.array([0,0,0,4,3]))
    array([5, 9, 0, 4])
    '''
    chord = []
    circle_note = 0
    chrom_note = 0

    for i in range(kpdve[4]+1):
        circle_note = pt_keypattern.get_binary_KPDVE_note(np.array([kpdve[0], kpdve[1], kpdve[2], kpdve[3], i]))
        chrom_note = pt_utils.f_circle_to_c_chrom(circle_note)
        chord.append(pt_utils.bit_locs(chrom_note)[0])

    return np.array(chord)


def ordered_scale_notes_for_KPDVE(kpdve):
    '''
    Parameters
    ----------
    kpdve : np.array(5)
        a kpdve array whose home mode notes are to be returned from the root up.

    Returns
    -------
    an array of notes, root first, going all the way through a scale.
    
    >>> ordered_scale_notes_for_KPDVE(np.array([0,0,0,4,3]))
    array([ 5,  7,  9, 11,  0,  2,  4])
    '''

    return ordered_chord_notes_for_KPDVE(np.array([kpdve[0], kpdve[1], kpdve[2], 2, 6]))
    

def unfold_ascending(note_array, mod=12):
    '''
    Parameters
    ----------
    kpdve : np.array(some size)
        a kpdve array whose home mode notes are to be returned from the root up, without folding back over into a pitch class set.

    Returns
    -------
    an array of notes, root first, going all the way through a scale.
    
    >>> unfold_ascending(np.array([ 5,  7,  9, 11,  0,  2,  4]))
    array([ 5,  7,  9, 11, 12, 14, 16])
    '''
    
    ordered_asc = np.copy(note_array)
    for i in range(len(ordered_asc) - 1):
        if ordered_asc[i+1] < ordered_asc[i]:
            ordered_asc[i+1] = ordered_asc[i+1] + mod

    return ordered_asc


# RAW CHORDS/MODES WITH A DISPLACEMENT, TO INTERACT WITH SCALE/KEY-BASED ENVIRONMENTS (e.g. FoxDot)
def get_chord_disp_tuple(kpdve):
    '''
    Parameters
    ----------
    kpdve : np.array(some size)
        a kpdve array whose chord notes are to be returned from the root up, without folding back over into a pitch class set.

    Returns
    -------
    an array of notes, root first, going all the way through a the chord, starting from zero, and taking the root as displacement (tonic).

    >>> get_chord_disp_tuple(np.array([0, 0, 0, 2, 6]))
    (array([ 0,  2,  4,  6,  7,  9, 11]), 5)
    
    FM7 (potentially) treated as a scale
    >>> get_chord_disp_tuple(np.array([0, 0, 0, 4, 3]))
    (array([ 0,  4,  7, 11]), 5)
    '''
    
    ordered = ordered_chord_notes_for_KPDVE(kpdve)
    unfolded = unfold_ascending(ordered) - ordered[0]
    disp = pt_utils.bit_locs(chrom_root_note_for_KPDVE(kpdve))[0]
    return unfolded, disp
    

def get_mode_disp_tuple(kpdve):
    '''
    Parameters
    ----------
    kpdve : np.array(some size)
        a kpdve array whose chord notes are to be returned from the root up, without folding back over into a pitch class set.

    Returns
    -------
    an array of notes, root first, going all the way through a the chord, starting from zero, and taking the root as displacement (tonic).

    F LYDIAN for next two cases.
    >>> get_mode_disp_tuple(np.array([0, 0, 0, 2, 6]))
    (array([ 0,  2,  4,  6,  7,  9, 11]), 5)
    
    >>> get_mode_disp_tuple(np.array([0, 0, 0, 4, 3]))
    (array([ 0,  2,  4,  6,  7,  9, 11]), 5)

    '''
    
    full_scale = np.array([kpdve[0], kpdve[1], kpdve[2], 2, 6])
    return get_chord_disp_tuple(full_scale)


def get_tonic_mode_disp_tuple(kpdve):
    '''
    Parameters
    ----------
    kpdve : np.array(some size)
        a kpdve array whose conventional mode (melodic minor, e.g.) root up, without folding back over into a pitch class set.

    Returns
    -------
    an array of notes, root first, going all the way through a the mode, starting from zero, and taking the root as displacement (tonic).

    C MAJOR for next two cases.
    >>> get_tonic_mode_disp_tuple(np.array([0, 0, 0, 2, 6]))
    (array([ 0,  2,  4,  5,  7,  9, 11]), 0)
    
    >>> get_tonic_mode_disp_tuple(np.array([0, 0, 0, 4, 3]))
    (array([ 0,  2,  4,  5,  7,  9, 11]), 0)
    
    G MAJOR
    >>> get_tonic_mode_disp_tuple(np.array([1, 0, 0, 4, 3]))
    (array([ 0,  2,  4,  5,  7,  9, 11]), 7)
    
    G MAJOR (as Dominant)
    >>> get_tonic_mode_disp_tuple(np.array([0, 1, 0, 4, 3]))
    (array([ 0,  2,  4,  5,  7,  9, 11]), 7)
    
    G MAJOR (as Dominant)
    >>> get_tonic_mode_disp_tuple(np.array([0, 1, 2, 4, 3]))
    (array([ 0,  2,  4,  5,  7,  9, 11]), 7)

    '''
    conv_scale = np.array([kpdve[0], kpdve[1], pt_utils.CONVENTION_DIST[kpdve[1]], 2, 6])
    return get_mode_disp_tuple(conv_scale)


# ======================
# get an integer to codify functions within a key (e.g. IV, V, etc.)
def circle_conv_function_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns a number 0-6 for function (relative to conventional tonic)

    F_M7 -> CM conventional
    >>> circle_conv_function_for_KPDVE(np.array([0,0,0,4,3]))
    6

    F#_M7
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

def scale_conv_degree_for_KPDVE(kpdve):
    '''
    np.array(5) -> int

    returns a number 0-6 for function (relative to conventional tonic)

    F_M7 -> as subdominant
    >>> scale_conv_degree_for_KPDVE(np.array([0,0,0,4,3]))
    3

    F#_M7 --> as mediant
    >>> scale_conv_degree_for_KPDVE(np.array([0,1,0,4,3]))
    6
    
    Bb M7 as dominant
    >>> scale_conv_degree_for_KPDVE(np.array([11,0,2,4,3]))
    4
    
    Bb M7 as tonic
    >>> scale_conv_degree_for_KPDVE(np.array([11,1,2,4,3]))
    0
    '''
    
    return (circle_conv_function_for_KPDVE(kpdve) * kpdve[3]) % 7


if __name__ == '__main__':
    import doctest
    doctest.testmod()

