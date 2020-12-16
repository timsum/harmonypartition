# AT THE MOMENT, THESE SHOUD BE MAINLY FOR DEBUGGING AND QUICK TESTS.
# BUT SOME STANDARDAIZATION OF VOCABULARY SHOULD PROVE USEFUL

# however,  IT IS IMPORTANT TO NOTE THAT JUST PARSING A BINARY NOTE
# GROUP CAN'T ACCOUNT FOR ENHARMONICS IN A GOOD WAY. THIS DOES ADDRESS THAT ISSUE.

import numpy as np
import pt_utils
import pt_keypattern


ACCIDENTALS = ["FB", "b", "", "#", "x"]
CIRCLE_NOTENAMES = ["F", "C", "G", "D", "A", "E", "B"]
CANONICSTARTPOINT = 14
CIRCLE_NOTENAMES_5_OCT = []
for ax in ACCIDENTALS:
    for nn in CIRCLE_NOTENAMES:
        CIRCLE_NOTENAMES_5_OCT.append(nn + ax)

PATTERN_CONVENTIONAL_NAMES = ["Major (tonic)",
                              "Major (dominant)",
                              "Melodic Minor",
                              "Harmonic Minor",
                              "Harmonic Major",
                              "Parallel Minor",
                              "Major (subdominant)"]
MODE_NAMES = ["Lydian", "Ionian", "Mixolydian", "Dorian",
              "Aeolian", "Phrygian", "Locrian"]
PATTERN_DISTORTION_NAMES = ["", "#1", "#5", "#2", "b3", "b7", "b4"]
MODE_NUMERALS = ["I", "V", "II", "VI", "III", "VII", "IV"]
VOICING_NAMES = ["1son", "5ths", "2nds", "6ths", "3rds", "7ths", "4ths"]
EXTENSION_NAMES = ["One", "Two", "Three", "Four", "Five", "Six", "Seven"]

# INDICES FOR NOTE NAMING (TOOLS FOR FUNCTIONS BELOW)
def note_index_for_K(k):
    '''

    Parameters
    ----------
    k : int
        k number

    Returns
    -------
    int
        index in the l.


    returns the strict lydian note index for a key area
    '''

    return index_for_PDVE_loc_in_key(0, k)


def index_for_PDVE_loc_in_key(loc, k):
    '''
    
    Parameters
    ----------
    loc : int
        the result of a bit-displacement from PDVE.
    k : int
        index of key

    Returns
    -------
    int
        the index of a note name in the big spiral of fifths.

    returns an index in the CIRCLE_NOTENAMES_5_OCT
    'loc' is figured from PDVE values

    >>> index_for_PDVE_loc_in_key(0, 0)
    14

    '''

    flatsideKey = -12 if k > 6 else 0
    return CANONICSTARTPOINT + k + flatsideKey + loc


# NOTE NAMES
def note_name_index_for_KPDVE(kpdve):
    '''

    The central function for finding index of note names in the
    big spiral of fifths.

    Parameters
    ----------
    kpdve : np.array(5)
        A KPDVE value

    Returns
    -------
    int
        index for a note in the big spiral of fifths

    >>> note_name_index_for_KPDVE([0,0,0,0,0])
    14

    >>> note_name_index_for_KPDVE([0,1,0,0,0])
    21

    >>> note_name_index_for_KPDVE([0,2,0,0,0])
    14
    '''

    pat = kpdve[1]
    deg = (kpdve[2] + kpdve[3] * kpdve[4]) % 7

    if pat > 0:
        if deg == pat - 1 and pat < 4:
            deg += 7
        if deg == pat and pat >= 4:
            deg += -7

    return index_for_PDVE_loc_in_key(deg, kpdve[0])

# ===================================

def note_name_for_kpdve(kpdve):
    '''

    The central function for note naming.
    Returns the name of the note at a KPDVE location

    Parameters
    ----------
    kpdve : np.array(5)
        a KPDVE value

    Returns
    -------
    string
        a note name for this kpdve position

    >>> note_name_for_kpdve([0,0,0,0,0])
    'F'

    >>> note_name_for_kpdve([0,1,1,0,0])
    'C'

    >>> note_name_for_kpdve([1,1,1,0,0])
    'G'

    '''

    return CIRCLE_NOTENAMES_5_OCT[note_name_index_for_KPDVE(kpdve)]

# ===================================

def chord_note_names_for_KPDVE(kpdve):
    '''
    ([int] -> [str])

    return a list of notes in a chord

    >>> chord_note_names_for_KPDVE([0,0,0,2,6])
    ['F', 'G', 'A', 'B', 'C', 'D', 'E']

    >>> chord_note_names_for_KPDVE([0,1,0,2,6])
    ['F#', 'G', 'A', 'B', 'C', 'D', 'E']

    >>> chord_note_names_for_KPDVE([0,1,3,4,3])
    ['D', 'F#', 'A', 'C']

    D 7b9
    >>> chord_note_names_for_KPDVE([10,3,5,4,4])
    ['D', 'F#', 'A', 'C', 'Eb']

    '''
    notenames = []
    for i in range(kpdve[4] + 1):
        notenames.append(note_name_for_kpdve([kpdve[0], kpdve[1],
                                              kpdve[2], kpdve[3], i]))

    return notenames

def scale_note_names_for_KPDVE(kpdve):
    '''
    ([int] -> [str])

    return a list of notes in a chord

    >>> scale_note_names_for_KPDVE([0,0,0,4,3])
    ['F', 'G', 'A', 'B', 'C', 'D', 'E']

    >>> scale_note_names_for_KPDVE([0,1,0,3,5])
    ['F#', 'G', 'A', 'B', 'C', 'D', 'E']

    '''
    
    scale_kpdve = [kpdve[0], kpdve[1], kpdve[2], 2, 6]
    notenames = []
    for i in range(scale_kpdve[4] + 1):
        notenames.append(note_name_for_kpdve([scale_kpdve[0], scale_kpdve[1],
                                              scale_kpdve[2], scale_kpdve[3], i]))

    return notenames



def circle_fifth_notes(k=0):
    '''
    
    Parameters
    ----------
    k : int, optional
        the circle of fifths starting at F or equivalent for a given key. The default is 0.

    Returns
    -------
    A list of 12 note names.
    
    >>> circle_fifth_notes()
    ['F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'Eb', 'Bb']

    '''
    
    circle_names = []
    for i in range(12):
        flatside = -12 if i > 9 else 0
        circle_names.append(CIRCLE_NOTENAMES_5_OCT[index_for_PDVE_loc_in_key(i + flatside, k)])
        
    circle_key_adjusted = [circle_names[(i - k)%12] for i in range(12)]
    return circle_key_adjusted


def chromatic_notes(k=0):
    circle = circle_fifth_notes(k=k)
    return [circle[(i*7+1)%12] for i in range(12)]


def chord_root_name_for_KPDVE(kpdve):
    '''
    Get the root of a chord from the KPDVE

    Parameters
    ----------
    kpdve : np.array(5)
        a path to the root of a chord

    Returns
    -------
    str
        the name of the note at the root of the chord


    >>> chord_root_name_for_KPDVE([0,0,0,2,6])
    'F'

    >>> chord_root_name_for_KPDVE([0,1,0,2,6])
    'F#'

    >>> chord_root_name_for_KPDVE([0,1,3,4,3])
    'D'

    D 7b9
    >>> chord_root_name_for_KPDVE([10,3,5,4,4])
    'D'
    '''

    return note_name_for_kpdve([kpdve[0], kpdve[1], kpdve[2], 0, 0])


def chord_function_in_key(kpdve):
    '''
    for a kpdve val, return a string description:, e.g. "I of C Major"", or "II of
    A Minor"", etc.
    
    Account for all conventional distortions...
    
    Parameters
    ----------
    kpdve : TYPE
        an np.array(5) kpdve location

    Returns
    -------
    function string.

    # >>> chord_function_in_key(np.array([0,0,1,4,3]))
    # 'I'
    
    # >>> chord_function_in_key(np.array([0,1,2,4,3]))
    # 'I'
    
    # >>> chord_function_in_key(np.array([0,2,3,4,3]))
    # 'I'
    
    # >>> chord_function_in_key(np.array([0,3,4,4,3]))
    # 'I'
    
    # >>> chord_function_in_key(np.array([0,4,1,4,3]))
    # 'I'

    # >>> chord_function_in_key(np.array([0,5,1,4,3]))
    # 'I'
    
    # >>> chord_function_in_key(np.array([0,6,0,4,3]))
    # 'I'
    

    '''
    
    conv_kpdve = pt_utils.kpdve_add(kpdve, pt_utils.conv_d_distortion_vec_for_p(kpdve[1]))
    
    # get the chord roman numeral
    chord_numeral = '{:>2}'.format(MODE_NUMERALS[conv_kpdve[2]])
    
    return chord_numeral


def conv_tonic_name_for_kpdve(kpdve):
    conv_kpdve = pt_utils.kpdve_add(kpdve, pt_utils.conv_d_distortion_vec_for_p(kpdve[1]))
    conv_tonic = np.array([conv_kpdve[0], conv_kpdve[1], pt_utils.CONVENTION_DIST[kpdve[1]], 0, 0])
    return note_name_for_kpdve(conv_tonic)

# text descriptions for state (first more visual, second more verbal.)
def kpdve_stream_string(kpdve, notegroup):
    '''
    info optimized for seeing terminal process.



    >>> kpdve_stream_string(np.array([0,0,0,4,2]), 0b110010000000)
    '0x0022c80 <--> 111111100000 :    C Major (tonic)    === 110010000000 : F as IV  '

    '''

    hexstring = "0x" + hex(pt_utils.minimal_bin_kpdve(notegroup, kpdve))[2:].zfill(7)
    description_string =  hexstring + " <--> "
    kpstring = format(pt_keypattern.get_binary_KP(kpdve[0], kpdve[1]), "b").zfill(12)
    #description_string += "mode : " 
    description_string += kpstring + " : " 
    tonicstring = conv_tonic_name_for_kpdve(kpdve).rjust(4)
    patternstring = PATTERN_CONVENTIONAL_NAMES[kpdve[1]].ljust(16)
    description_string += tonicstring + " " + patternstring
    description_string += " === "
    description_string += format(pt_keypattern.get_binary_KPDVE_chord(kpdve), "b").zfill(12) + " : " 
    #description_string += "chord: "
    description_string += chord_root_name_for_KPDVE(kpdve) + " as "  + chord_function_in_key(kpdve).ljust(4)
    
    return description_string


def kpdve_description_info(kpdve):
    '''
    
    A summary of all available information for a kpdve value

    Parameters
    ----------
    kpdve : np.array(5)
        a KPDVE value

    Returns
    -------
    string
        All working types of string description output, formatted

# =============================================================================
#     >>> kpdve_description_info(np.array([0,0,0,4,3]))
#     "lydian base: F ... lydian distortion:  ... pattern name: Tonic Major ... root: F ... undistorted mode: Lydian ... underlying function: IV ... voicing: 3rds ... chord notes: ['F', 'A', 'C', 'E']"
#      
#     >>> kpdve_description_info(np.array([0,1,1,4,3]))
#     "lydian base: F ... lydian distortion: #1 ... pattern name: Dominant Major ... root: C ... undistorted mode: Ionian ... underlying function: I ... voicing: 3rds ... chord notes: ['C', 'E', 'G', 'B']"
#     
#     D 7b9
#     >>> kpdve_description_info(np.array([10,3,5,4,4]))
#     "lydian base: Eb ... lydian distortion: #2 ... pattern name: Harmonic Minor ... root: D ... undistorted mode: Phrygian ... underlying function: III ... voicing: 3rds ... chord notes: ['D', 'F#', 'A', 'C', 'Eb']"
#     
# =============================================================================
    '''

    # description_string = "lydian base: " + note_name_for_kpdve([kpdve[0], 0, 0, 0, 0]) + " ... "
    # description_string += "lydian distortion: " + PATTERN_DISTORTION_NAMES[kpdve[1]] + " ... "
    description_string = "pattern name: " + PATTERN_CONVENTIONAL_NAMES[kpdve[1]] + " : "
    description_string += "root: " + chord_root_name_for_KPDVE(kpdve) + " : "
    # description_string += "undistorted mode: " + MODE_NAMES[kpdve[2]] + " " "
    description_string += "underlying function: " + MODE_NUMERALS[kpdve[2]] + " : "
    # description_string += "voicing: " + VOICING_NAMES[kpdve[3]] + " ... "
    description_string += "chord notes: " + str(chord_note_names_for_KPDVE(kpdve))

    return description_string


if __name__ == '__main__':
    import doctest
    doctest.testmod()



