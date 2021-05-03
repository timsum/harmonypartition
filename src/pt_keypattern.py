import numpy as np
import pt_utils

### WARNING: NOTHING IN THIS FILE IS CHROMATIC!
### *CHROMATIC OPERATIONS CAN BE FOUND IN THE pt_musicutils.py FILE
### ALL OPERATIONS ARE BASED ON THE F-LYDIAN NOTE PARADIGM: 0b111111100000

# =================================================================
thirds_only = np.array([4])
# =================================================================
scales_and_thirds = np.array([4,2])
# =================================================================
fifths_and_scales_and_thirds = np.array([4, 2, 1])
# =================================================================
all_close_voicings = np.array([4,2,6])
# =================================================================
# with adjustments for low D and P, this may be the richest option. 
# prefers, thirds, seconds, then fifths, seconds, fourths, sixths....
# 0 is a excluded as trivial, since it cannot improve on others'
# solutions.
all_voicings = np.array([4, 1, 2, 6, 3, 5, 6])
# =================================================================

v_options = np.array([thirds_only, scales_and_thirds, fifths_and_scales_and_thirds, all_close_voicings, all_voicings], dtype=object)


def get_binary_KPDVE_note(kpdve):
    '''

    Parameters
    ----------
    kpdve
        a np.array(5) in form KPDVE

    Returns
    -------
    int
        a representation of a chord in binary (circle-of-fifths)

    7 of F Major 7 chord
    >>> get_binary_KPDVE_note(np.array([0,0,0,4,3]))
    64

    G a fifth above C as degree 1 in F lydian
    >>> get_binary_KPDVE_note(np.array([0,0,1,1,1]))
    512

    G V7 b9 -- dominant in C Harmonic minor... top note Ab
    >>> get_binary_KPDVE_note(np.array([0,4,2,4,4]))
    4

    '''

    return  pt_utils.rotate_bits_right(apply_filter_for_p(get_binary_DVE_note(kpdve[2], kpdve[3], kpdve[4]), kpdve[1]), kpdve[0])


def get_binary_KPDVE_chord(kpdve):
    '''
    return a binary pitch-class set for a given kpdve array

    Parameters
    ----------
    kpdve
        a np.array(5) in form KPDVE

    Returns
    -------
    int
        a representation of a chord in binary (circle-of-fifths)


    F Major 7 chord
    >>> get_binary_KPDVE_chord(np.array([0,0,0,4,3]))
    3264

    G a fifth above C as degree 1 in F lydian
    >>> get_binary_KPDVE_chord(np.array([0,0,2,1,1]))
    768

    Major 9 pile of fifths on Eb
    >>> get_binary_KPDVE_chord(np.array([9,0,0,1,2]))
    7

    V7 of V in C Major
    >>> get_binary_KPDVE_chord(np.array([0,1,3,4,3]))
    1424

    G V7 b9 -- dominant in C Harmonic minor...
    >>> get_binary_KPDVE_chord(np.array([0,4,2,4,4]))
    2852
    '''

    chord = 0
    for i in range(kpdve[4]+1):
        chord |= get_binary_KPDVE_note(np.array([kpdve[0], kpdve[1], kpdve[2], kpdve[3], i]))

    return  chord


def get_ordered_chord_notes(kpdve):
    '''

    Parameters
    ----------
    kpdve : np.array(5)
        a kpdve array whose notes are to be returned from the root up.

    Returns
    -------
    an array of notes, root first.
    
    >>> get_ordered_chord_notes(np.array([0,0,0,4,3]))
    array([0, 4, 1, 5])
    '''
    chord = []
    
    for i in range(kpdve[4]+1):
        chord.append(pt_utils.bit_locs(get_binary_KPDVE_note(np.array([kpdve[0], kpdve[1], kpdve[2], kpdve[3], i])))[0])

    return np.array(chord)


def get_binary_K(k):
    """
    

    Parameters
    ----------
    k : int
        a value for Key

    Returns
    -------
    int
         returns binary number representing pitch classes for a given major key.

    
    (int) -> int

 
    returns 0b111111100000
    >>> get_binary_K(0)
    4064
    

    returns 0b011111110000
    >>> get_binary_K(1)
    2032

    returns 0b111110000011
    >>> get_binary_K(10)
    3971
    """

    return pt_utils.rotate_bits_right(pt_utils.C_M_FIFTHS, k)


def get_binary_P(p):
    """
    

    Parameters
    ----------
    p : TYPE
        DESCRIPTION.

    Returns
    -------
    int
        returns distortion byte 0b100000010000 at position P
        
    returns 0b100000010000
    >>> get_binary_P(0)
    2064
    
    returns 0b010000001000
    >>> get_binary_P(1)
    1032
    
    returns 0b000001000010
    >>> get_binary_P(10)
    66
    """
 
    return pt_utils.rotate_bits_right(pt_utils.P_PARSER, p)


def get_binary_KP(k, p):
    '''
    (int, int) -> int

    Apply the P displacement P(x) to the C Major grouping and return adjusted for key
    P must be between 0 and 6

    P allows all twelve notes to be part of a major key

    0 returns unaffected K
    1-3 return K^get_binary_p(p-1)
    4-6 return K^get_binary_p(p+5)

    this means  0:C Major
    (for CM)    1:G Major (Dominant)
                2:D Melodic Minor
                3:A Harmonic Minor (relative minor)
                4:C Harmonic Major
                5:C Melodic Minor (parallel minor)
                6:F Major (subdominant) 

    returns 0b111111100000
    >>> get_binary_KP(0, 0)
    4064

    returns 0b011111110000
    >>> get_binary_KP(0, 1)
    2032

    returns 0b010111110100
    >>> get_binary_KP(1, 2)
    1524

    returns 0b111111100000 CM as dominant
    >>> get_binary_KP(11, 1)
    4064

    returns 0b111111100000 CM as subdominant
    >>> get_binary_KP(1, 6)
    4064
    '''

    if p == 0:
        return get_binary_K(k)
    
    result = pt_utils.rotate_bits_right(apply_filter_for_p(pt_utils.C_M_FIFTHS, p), k)

    return result


# right now for demonstration purposes... doesn't *quite* account for un-wrinkled modes.
def raw_kp_voxel():
    keys = [get_binary_K(k) for k in range(12)]
    patterns = [get_binary_P(p) for p in range(12)]

    return np.array([[k ^ p for p in patterns] for k in keys])
    
# Main Call from Partita
def get_KPDVE_list_for_notegroup(notegroup, v_opt=-1):
    '''
    
    
    Parameters
    ----------
    notegroup : a twelve-bit integer for a circle-based pitch-class set

    Returns
    -------
    a Numpy array of form [[K1,P1,D1,V1,E1] ... [Kn, Pn, Dn, Vn, Dn]]

    
    F Major 7
    >>> get_KPDVE_list_for_notegroup(0b110011000000)
    array([[ 0,  0,  0,  4,  3],
           [ 0,  3,  0,  4,  3],
           [ 0,  6,  0,  4,  3],
           [ 1,  6,  6,  4,  3],
           [10,  1,  2,  4,  3],
           [11,  0,  1,  4,  3],
           [11,  1,  1,  4,  3],
           [11,  4,  1,  4,  3]])

    G Dominant 7 b9 #2
    >>> get_KPDVE_list_for_notegroup(0b101100100101)
    array([[9, 4, 5, 4, 5]])
    
    No Match
    >>> get_KPDVE_list_for_notegroup(0b11111111)
    array([[12,  7,  7,  7,  7]])
    
    '''

    kp_list = get_KP_list_for_notegroup(notegroup)
    
    # this is the point to check for bitonality
    
    if len(kp_list) == 0:
        return(np.array([pt_utils.MODVALS]))
 
    return KP_list_to_KPDVE_list(kp_list, notegroup, v_opt)


# THIS IS THE POINT WHERE THE PENTATONIC LIST HAS TO HAPPEN? 
def get_KP_list_for_notegroup(notegroup, pentatonic=False):
    '''

    Parameters
    ----------
    notegroup : a twelve-bit integer for a circle-based pitch-class set

    Returns
    -------
    a Numpy array of form [K,P,D,V,E]

 
    G Dominant 7 b9 #2
    >>> get_KP_list_for_notegroup(0b101100100101)
    array([[9, 4, 0, 0, 0]])
    
    No Match
    >>> get_KP_list_for_notegroup(0b11111111)
    array([], dtype=float64)

    '''
    
    kp_list = []
    
    for i in range(pt_utils.MODVALS[0]):
        for j in range(pt_utils.MODVALS[1]):
            kp_temp = get_binary_KP(i, j)
            if pentatonic == True:
                kp_temp = pt_utils.pentatonic_transform(kp_temp)
            if notegroup | kp_temp == kp_temp:
                kp_list.append([i, j, 0, 0, 0])
      
    return np.array(kp_list)


def KP_list_to_KPDVE_list(kp_list, notegroup, v_opt=0):
    '''

    Parameters
    ----------
    kp_list : np.array of KPDVE values
        
    notegroup : a twelve-bit integer for a circle-based pitch-class set
    
    v_opt : int, optional
        restrict voicing loops to thirds (see global options)

    Returns
    -------
    kpdve_list (array of np.array(5))
    
    >>> 

    '''

    kpdve_list = kp_list.copy()

    for kp in kpdve_list:
        kp += DVE_vals_for_CM_notegroup(undo_KP_to_analyze(notegroup, kp[0], kp[1]), v_opt)
    
    return kpdve_list


def DVE_vals_for_CM_notegroup(notegroup, v_opt=-1):
    '''
    take a notegroup which has been switched to the c major paradigm.
    find root position by testing all notes as possible D.  Choose the most efficient.

    Parameters
    ----------
    notegroup : int
        pitch class set (circle-fifths-based).
    v_opt : int, optional
        restrict voicing loops to thirds (see global options). The default is 0.

    Returns
    -------
    np.array(n, 5)
        ([0,0,d, v_opt ,e])


    >>> DVE_vals_for_CM_notegroup(0b110011000000)
    array([0, 0, 0, 4, 3])
    '''

    v_vals = v_options[v_opt]
    minsteps = 7
    
    d = 7
    v = 4
    e = pt_utils.bit_count(notegroup)

    for notevalue in pt_utils.bit_locs(notegroup):
        for v_val in v_vals:
            steps_temp = num_steps_to_DVE_match_at_D(notegroup, notevalue, v_val)
            if steps_temp < minsteps or (steps_temp == minsteps and notevalue < d):
                minsteps = steps_temp
                d = notevalue
                v = v_val
                e = steps_temp
            


    return np.array([0, 0, d, v, e])


def num_steps_to_DVE_match_at_D(notegroup, d, v = 4):
    '''
    (int, int, int) -> int

    return the number of steps it takes for a growing tower of intervals can contain all the notes of a chord

    F 5 chord
    >>> num_steps_to_DVE_match_at_D(0b110010000000, 0, 4)
    2

    F 7 chord
    >>> num_steps_to_DVE_match_at_D(0b110011000000, 0, 4)
    3
    
    F 9 chord (no 5) 
    >>> num_steps_to_DVE_match_at_D(0b101011000000, 0, 4)
    4
    '''

    count = 0
    tower_byte = pt_utils.binary_note_at_loc(d)

    while tower_byte & notegroup != notegroup and count < 7:
        count += 1
        tower_byte |= pt_utils.binary_note_at_loc(DVE_linear_eq(d, v, count))

    return count


def get_binary_DVE_note(d, v, e):
    '''
    (int, int, int)  -> int

    return the note at the end of the tunnel: a single bit, at the last extension of the DVE sequence
    this function takes care of the case for c major (where all transformations occur)

    >>> get_binary_DVE_note(0, 0, 0)
    2048

    return the fifth above D (A)
    >>> get_binary_DVE_note(3, 4, 2)
    128

    '''

    return pt_utils.rotate_bits_right(pt_utils.LEFT_BIT, DVE_linear_eq(d, v, e))


# --------------------------
def DVE_linear_eq(d, v, e):
    '''

    Parameters
    ----------
    d : int
        degree value in KPDVE.
    v : int
        voicing value in KPDVE.
    e : int
        extension value in KPDVE.

    Returns
    -------
    int
        for a notegroup reduced to C Major, the index of the last output note 
        in a KPDVE encoding 

    '''
    return (d + v * e) % 7
# --------------------------


def get_binary_DVE_chord(d, v, e):
    '''

    Parameters
    ----------
    d : int
        degree value in KPDVE.
    v : int
        voicing value in KPDVE.
    e : int
        extension value in KPDVE.
        
    Returns
    -------
     int
        a chord from root to last extension, encoded as 12-bit pitch-class set 
                   
    F Major 7 Chord
    >>> get_binary_DVE_chord(0, 4, 3)
    3264

    '''

    notegroup_cM = 0
    for i in range(e+1):
        notegroup_cM |= get_binary_DVE_note(d, v, i)

    return notegroup_cM


def apply_filter_for_p(notegroup_cM, p):
    '''
    (int, int) -> int

    takes a notegroup in c major and applies a p value -- raises or lowers a note by a half step with XOR operation

    >>> apply_filter_for_p(0b111111100000, 0)
    4064

    >>> apply_filter_for_p(0b111111100000, 1)
    2032

    >>> apply_filter_for_p(0b111101100100, 4)
    4064
    '''

    if (p == 0):
        return notegroup_cM

    p_filter = get_binary_P(conventional_p_filter_index(p))

    if ((notegroup_cM & p_filter) == 0):
        return notegroup_cM

    return p_filter ^ notegroup_cM


def conventional_p_filter_index(p):
    '''
    (int) -> int

    adjust the p index (a number from 1-6) to reflect 1-3 -> sharp side 4-6 -> flat side

    >>> conventional_p_filter_index(6)
    11

    >>> conventional_p_filter_index(1)
    0

    >>> conventional_p_filter_index(0)
    -1
    '''

    if p > 0:
        return p - 1 if p < 4 else p + 5

    return -1


def undo_KP_to_analyze(notegroup, k, p):
    '''
    (int, int, int) -> int

    to find DVE, undo the KP transformations in  known group.
    this preparation allows for a single parsing tower (or set) to find DVE values.

    first undo the K shift, then undo the P

    >>> undo_KP_to_analyze(0b111111100000, 0, 0)
    4064

    >>> undo_KP_to_analyze(0b111111100000, 11, 1)
    4064

    >>> undo_KP_to_analyze(0b101111101000, 0, 2)
    4064

    >>> undo_KP_to_analyze(0b001011111010, 2, 2)
    4064

    '''
    # if p == 0 or no note must be lowered/raised... 
    notegroup_cM = pt_utils.rotate_bits_left(notegroup, k)
    return apply_filter_for_p(notegroup_cM, p)


if __name__ == "__main__":
    import doctest
    doctest.testmod()