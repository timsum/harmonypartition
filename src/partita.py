import numpy as np

import pt_utils
import pt_keypattern
import pt_kpdve_list_optimize


# =============================================================================
# MIDI and notegroup input for KPDVE output
# =============================================================================

def analyze_binary_input_for_closest_KPDVE(notegroup, kpdve, v_opt=0):
    '''

    Parameters
    ----------
    notegroup : int
        takes a binary-encoded pitch class set (chromatic: 0b10001001001)
    kpdve : np.array(5)
        the previous kpdve result

    Returns
    -------
    np.array(5) (int)
        geometrically most proximate KPDVE analysis, compared with previous

    C Major 7 Chord as first degree in F Lydian
    >>> analyze_binary_input_for_closest_KPDVE(0b100010010001, np.array([0,0,0,0,0]))
    array([0, 0, 1, 4, 3])

    >>> analyze_binary_input_for_closest_KPDVE(560, np.array([0,0,0,0,0]))
    array([0, 1, 2, 4, 3])
    
    >>> analyze_binary_input_for_closest_KPDVE(0b110001001000, np.array([8,4,0,4,3]))
    array([8, 3, 0, 4, 3])
    
    '''

    return pt_kpdve_list_optimize.closest_kpdve(analyze_binary_note_input(notegroup, v_opt=v_opt), kpdve)

    # THIS IS VERY PROBLMATIC. WHAT TO DO WITH INVALID ENTRY...
    # if np.array_equal(new_kpdve, pt_utils.MODVALS):
    #     return kpdve
    # else:
    #     return new_kpdve

def analyze_midi_note_input_for_closest_KPDVE(midinote_list, kpdve, v_opt=0):
    '''

    Parameters
    ----------
    midinote_list : [int]
        a list of integers containing a list of MIDI notes (0-128)

    Returns
    -------
      np.array(int)
        geometrically most proximate KPDVE analysis, compared with previous

    C Major 7 Chord as first degree in F Lydian   
    >>> analyze_midi_note_input_for_closest_KPDVE([60, 64, 67, 71], np.array([0,0,0,0,0]))
    array([0, 0, 1, 4, 3])


    '''

    notegroup = 0
    for midi_note in midinote_list:
        notegroup |= pt_utils.LEFT_BIT >> (midi_note % 12)
            
    return analyze_binary_input_for_closest_KPDVE(notegroup, kpdve, v_opt=v_opt)

# =============================================================================
# unoptimized KPDVE list
#  for now, these are the options for the v value. It seems to make almost no difference which is chosen, and thirds 
# seem to work just fine.  For now: v_opt=0 until a later date.
# v_options = np.array([thirds_only, scales_and_thirds, fifths_and_scales_and_thirds, all_close_voicings, all_voicings])
# =============================================================================

def analyze_binary_note_input(notegroup, v_opt=0):
    '''
    takes a chromatic pitch class set (derived from MIDI numbering (0-128) % 12), represented in binary like a piano keyboard:
    C D EF G A B
    100011000100 = F Major 7

    Parameters
    ----------
    notegroup : int
        a chromatic pitch class set (derived from MIDI numbering (0-128) % 12), represented in binary like a piano keyboard:
      C D EF G A B
    v_opt : int (index)
        selects from voicing options in keypattern.py.
        default: all voicings (often increases stability, though costs in speed.  Live audio should probably stick to thirds)
        
    Returns
    -------
    np.array(listlength x 5)
        returns kpdve list as np.array

    >>> analyze_binary_note_input(0)
    array([[12,  7,  7,  7,  7]])

    >>> analyze_binary_note_input(0b100011000100)
    array([[ 0,  0,  0,  4,  3],
           [ 0,  3,  0,  4,  3],
           [ 0,  6,  0,  4,  3],
           [ 1,  6,  6,  4,  3],
           [10,  1,  2,  4,  3],
           [11,  0,  1,  4,  3],
           [11,  1,  1,  4,  3],
           [11,  4,  1,  4,  3]])

    '''

    if notegroup == 0:
        return np.array([pt_utils.MODVALS])
    # convert the input to circle of fifths mode and analyze
    return pt_keypattern.get_KPDVE_list_for_notegroup(pt_utils.c_chrom_to_f_circle(notegroup), v_opt=v_opt)

# =============================================================================
# get a notegroup for a kpdve value
# =============================================================================

def chord_for_KPDVE_input(a_kpdve):
    '''

    Parameters
    ----------
    a_kpdve : np.array(5) as kpdve
        a kpdve value

    Returns
    -------
    int
        representative chord for a KPDVE value
        binary representation of form (C D EF G A B) in 12 bits

    F Major 7
    >>> chord_for_KPDVE_input(np.array([0,0,0,4,3]))
    2244

    C Dominant 7
    >>> chord_for_KPDVE_input(np.array([11,0,2,4,3]))
    2194
 
    '''

    return pt_utils.f_circle_to_c_chrom(pt_keypattern.get_binary_KPDVE_chord(a_kpdve))

# =============================================================================
# # # =============================================================================
# # #  Maximal optimized in/out -- probably more effective is to put this in the reader...
# # # =============================================================================
# =============================================================================

def binary_pairing_for_note_input(notegroup):
    '''

    Parameters
    ----------
    notegroup : int
        a chromatic pitch class set C D EF G A B

    Returns
    -------
    RxxxKKKKPPPDDDVVVEEEC-D-EF-G-A-B
        a note group paired with a context

    '''

    bin_kpdve = pt_utils.KPDVE_to_binary_encoding(analyze_binary_input_for_closest_KPDVE(notegroup))
    return pt_utils.binary_encoded_context_chord_pair(bin_kpdve, notegroup)


def binary_pairing_for_KPDVE_input(kpdve):
    '''

    Parameters
    ----------
    kpdve : np.array
        a kpdve context    

    Returns
    -------
    RxxxKKKKPPPDDDVVVEEEC-D-EF-G-A-B
        a note group paired with a context

    '''

    notegroup = chord_for_KPDVE_input(kpdve)
    return pt_utils.binary_encoded_context_chord_pair(pt_utils.KPDVE_to_binary_encoding(kpdve), notegroup)

# # # =============================================================================
# ============= HELPER AND TEST====================================================

def opening_sample_list_analysis(notegroup_list, chomp_pct=10, sample_pct=10):
    '''
    Take the first 5% samples of the notegroup list, analyze them, and return an 
    average KPDVE value. Use random integers as reference KPDVE values 
    
    For finding a reasonable starting point for sequential
    list analysis

    Parameters
    ----------
    notegroup_list : np.array(n)
        DESCRIPTION.

    Returns
    -------
    np.array(5)

    '''

    avg_kpdve = np.zeros(5)
    
    # chomp the first 10% (chomp_pct)
    opening_chomp_size = np.floor_divide(notegroup_list.shape[0], chomp_pct) + 1
    first_n_pct_sample = notegroup_list[0:opening_chomp_size]

    # sample 10% of the first 10%
    sample_size = np.floor_divide(first_n_pct_sample.shape[0], sample_pct) + 1
    sample_notegroups = np.random.choice(first_n_pct_sample, sample_size)

    # choose randomly from within each kpdve list result
    for ng in sample_notegroups:
        kpdve_list = analyze_binary_note_input(ng)
        # competing techniques
        # 1) sample from KPDVE list at random (not good on WTC CM)            
        # avg_kpdve += kpdve_list[np.random.randint(kpdve_list.shape[0])]
        # 2) sort for lowest P value (least entropy) and take the first
        avg_kpdve += kpdve_list[np.argsort(kpdve_list[:, 1])][0]
    
    avg_kpdve = avg_kpdve / sample_size
    
    return avg_kpdve.astype(int)


def test_analysis():
    '''

    Returns
    -------
    None.

    '''

    for i in range(0b1111111111):
        result = analyze_binary_input_for_closest_KPDVE(i, pt_utils.MODVALS)
        print(result)
        print("===")


if __name__ == '__main__':
    import doctest
    doctest.testmod()



    