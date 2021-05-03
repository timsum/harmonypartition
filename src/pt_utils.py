import numpy as np

LEFT_BIT =          0b100000000000  # 2048
CHROMATIC_SCALE =   0b111111111111  # 4095
C_M_FIFTHS =        0b111111100000  # 4064
P_PARSER =          0b100000010000  # 2064
WHOLE_TONE =        0b101010101010  # 2730
C_DOM_b9 =          0b101000100100  # 2596 // the harmonic dominant...

MODVALS =           np.array([12, 7, 7, 7, 7])
NULL_KPDVE =        np.array([100, 100, 100, 100, 100])
CONVENTION_DIST =   np.array([1,2,3,4,1,1,0])


def chrom_circle_switch(notegroup):
    '''

    switches between a circle of fifths pattern and a chromatic pattern (commutative)
    assumes both start on the same note

    Parameters
    ----------
    notegroup : int
        a twelve-bit pitch-class set

    Returns
    -------
    int
        a twelve=bit pitch-class set

    >>> chrom_circle_switch(0b101010110101)
    4064

    >>> chrom_circle_switch(0b111111100000)
    2741

    >>> chrom_circle_switch(0b101010101010)
    2730
    '''
    
    moves = ~WHOLE_TONE & notegroup
    movesleft = rightmost_twelve(moves << 6)
    movesright = moves >> 6

    return (WHOLE_TONE & notegroup) | (movesleft | movesright)


def conv_d_distortion_vec_for_p(p):
    '''
    get a vector to add to a kpdve value to account for conventional p distortions

    Parameters
    ----------
    p : a pval
        DESCRIPTION.

    Returns
    -------
    np.array(5) of [0, 0 distortion, 0, 0]

    '''
    
    return np.array([0, 0, (7 - CONVENTION_DIST[p]) % 7, 0, 0])


# =============================================================================
# chrom/circle in bits
# =============================================================================

def c_chrom_to_f_circle(notegroup):
    '''

    take a c-based chromatic 12-bit C-D-E....B set, convert to circle of
    fifths FCGDAEB_._._

    Parameters
    ----------
    notegroup : int
         a twelve=bit pitch-class set (chromatic)

    Returns
    -------
    int
         a twelve=bit pitch-class set (circle)

    C Major Scale
    >>> c_chrom_to_f_circle(0b101011010101)
    4064

    >>> c_chrom_to_f_circle(0b101011010101)
    4064

    G Dominant 7
    >>> c_chrom_to_f_circle(0b100010010010)
    1601

    FM 7
    >>> c_chrom_to_f_circle(0b100010010001)
    1632
    '''

    return rotate_bits_right(chrom_circle_switch(notegroup), 1)


def f_circle_to_c_chrom(notegroup):
    '''

    take a circle of fifths bit set FCGDAEB_._._, convert to c-based
    chromatic 12-bit C-D-E....B set

    Parameters
    ----------
    notegroup : int
         a twelve=bit pitch-class set (circle)

    Returns
    -------
    int
         a twelve=bit pitch-class set (chromatic)

    FM 7
    >>> f_circle_to_c_chrom(0b110011000000)
    2244

    '''
    return chrom_circle_switch(rotate_bits_left(notegroup, 1))


# =============================================================================
# pentatonic transform
# =============================================================================

def pentatonic_transform(notegroup):
    '''

    takes a notegroup (usually a kp filter for a mode) and transforms it to pentatonic

    Parameters
    ----------
    notegroup : int
         any int

    Returns
    -------
    int
         a twelve=bit pitch-class set

    >>> pentatonic_transform(0b111111111111)
    0

    >>> pentatonic_transform(0b111111100000)
    3968
    '''
    inverted = ~notegroup
    print(inverted)
    return rotate_bits_right(inverted, 5)

# =============================================================================
# bit conventions around 12
# =============================================================================

def rightmost_twelve(notegroup):
    '''

    zeros out all but the leftmost 12 bits

    Parameters
    ----------
    notegroup : int
         any int

    Returns
    -------
    int
         a twelve=bit pitch-class set

    >>> rightmost_twelve(0b1111111111111111)
    4095

    >>> rightmost_twelve(0b111000000000000)
    0
    '''

    return notegroup & CHROMATIC_SCALE


def rotate_bits_right(notegroup, shiftcount):
    '''

    returns 12 bit rotation to the right.  negative rotates to the left

    Parameters
    ----------
    notegroup : int
         a twelve=bit pitch-class set
    shiftcount : int
        the amount to circularly shift the notegroup

    Returns
    -------
    int
         a twelve=bit pitch-class set

    >>> rotate_bits_right(0b111111100000, 3)
    508

    '''

    netshift = shiftcount % 12
    if netshift == 0:
        return notegroup

    return rightmost_twelve((notegroup >> netshift) | (notegroup << (12-netshift)))


def rotate_bits_left(notegroup, shiftcount):
    '''
    circular bit shift over leftmost twelve bits

    Parameters
    ----------
    notegroup : int
        a 12-bit pitch-class set.
    shiftcount : int
        the number of bits to shift the notegroup

    Returns
    -------
    int
       a twelve-bit pitch-class set

    >>> rotate_bits_left(0b111111100000, 3)
    3847
    '''

    netshift = shiftcount % 12
    if netshift == 0:
        return notegroup

    return rightmost_twelve((notegroup << netshift) | (notegroup >> (12-netshift)))


def bit_locs(notegroup):
    '''
    returns the locations of bits in a 12-bit pitch-class set

    Parameters
    ----------
    notegroup : int
        a twelve=bit pitch-class set

    Returns
    -------
    np.array(list_length)
        a list of the bit locations in a pitch-class set

    >>> bit_locs(0b10)
    array([10])

    >>> bit_locs(0b110011000000)
    array([0, 1, 4, 5])

    >>> bit_locs(0b110011)
    array([ 6,  7, 10, 11])
    '''

    locs = []
    for i in range(12):
        if LEFT_BIT & notegroup == LEFT_BIT:
            locs.append(i)
        notegroup <<= 1
    return np.array(locs)


def bit_count(notegroup):
    '''
    returns the number of 1 bits in a 12-bit pitch-class set

    Parameters
    ----------
    notegroup : int
         a twelve=bit pitch-class set

    Returns
    -------
    int
        the number of 1 bits (out of twelve)

    >>> bit_count(0b10)
    1

    >>> bit_count(0b110011000000)
    4

    >>> bit_count(0b0)
    0
    '''

    notes = 0
    for i in range(12):
        if LEFT_BIT & notegroup == LEFT_BIT:
            notes = notes + 1
        notegroup <<= 1
    return notes


def single_bit_loc(notegroup):
    if bit_count(notegroup) > 0:
        return bit_locs(notegroup)[0]

    return -1


def binary_note_for_chord(notegroup_array):
    '''
    given a list of integers for pitches in a chord (can be midi or
    pitch-class-set), return the 12-bit pitch-class-set representation

    Parameters
    ----------
    notegroup_array : np.array(n)
        a list of pitch classes

    Returns
    -------
    binary notegroup

    '''

    notegroup = 0
    for an_int in notegroup_array:
        notegroup |= binary_note_at_loc(an_int)

    return notegroup


def binary_note_at_loc(noteloc):

    '''
    return a note in the form 0b000000010000 for an integer request (equivalent to 2^(11-n)    

    Parameters
    ----------
    noteloc : int 0-11
        the location of a note in a 12-bit pitch-class set

    Returns
    -------
    int
        a 12-bit pitch-claass set with a 1 at 'loc'

    >>> binary_note_at_loc(0)
    2048

    >>> binary_note_at_loc(11)
    1

    >>> binary_note_at_loc(8)
    8
    '''

    return LEFT_BIT >> (noteloc % 12)


# KPDVE ARITHMETIC
def kpdve_add(kpdve1, kpdve2):
    '''
    vector summation in modular space

    Parameters
    ----------
    kpdve1 : a kpdve value
        any path in kpdve space (chord or distortion)
    kpdve2 : a kpdve value
        any path in kpdve space (chord or distortion

    Returns
    -------
    np.array(5)

    >>> kpdve_add(np.array([4,4,4,4,4]), np.array([8,3,3,3,3]))
    array([0, 0, 0, 0, 0])

    '''

    return (kpdve1 + kpdve2) % MODVALS
    

def kpdve_random():
    '''
    
    Returns
    -------
    a random valid KPDVE vector

    '''

    result = np.zeros(5, dtype=int)

    for i in range(5):
        result[i] = np.random.randint(0, MODVALS[i])

    return result

# =============================================================================
# 
# KPDVE ENCODING
def  KPDVE_to_binary_encoding(aKPDVE):
    '''
    
    Parameters
    ----------
    aKPDVE : np.array(5)
        

    Returns
    -------
    integer
        a 16-bit encoded kpdve number
        
    KPDVE_to_binary_encoding(np.array([0,0,0,4,3]))
    35

    '''

    encodedByte = np.int(0);
    
    for an_int in aKPDVE:
        encodedByte = encodedByte << 3
        encodedByte = np.int(an_int) | encodedByte
    
    return encodedByte;    


def binary_encoding_to_KPDVE(enc_kpdve):
    '''

    Parameters
    ----------
    enc_kpdve : int
        a 16-bit kpdve encoding.

    Returns
    -------
    np.array(5)
        the encoded values as numpy array

    >>> binary_encoding_to_KPDVE(0b100011)
    array([0, 0, 0, 4, 3])

    '''
    result = np.zeros(5, dtype=int)
    for i in range(4):
        result[4 - i] = np.int(enc_kpdve & 0b111)
        enc_kpdve >>= 3;
    result[0] = enc_kpdve;

    return result


def minimal_bin_kpdve(notegroup, kpdve):
    '''
    returns a uint32 for notes and harmony

    Parameters
    ----------
    notegroup : int
        a binary notegroup (chromatic).
    kpdve : ndarray(5)
        a kpdve encoding.

    Returns
    -------
    Returns
    -------
    numpy uint32 containing 28-bit encoding of the two values 
        for transmission and analysis: KKKKPPPDDDVVVEEEC-D-EF-G-A-B  
        a musical pixel
        
    >>> minimal_bin_kpdve(0b100011000100, np.array([0,0,0,4,3]))
    145604
    '''
    
    context = KPDVE_to_binary_encoding(kpdve)
    return np.uint32(binary_encoded_context_chord_pair(context, notegroup))


def bin_kpdve_from_minimal(encoded_bkpdve):
    '''
    takes the minimal encoding and converts to int notegroup and numpy kpdve

    Parameters
    ----------
    encoded_bkpdve : int
        0bKKKKPPPDDDVVVEEE concatenated with 0bC-D-EF-G-A-B

    Returns
    -------
    integer (binary notegroup) and np.array(5)
    
    >>> bin_kpdve_from_minimal(145604)
    (2244, array([0, 0, 0, 4, 3]))

    '''
    
    chord = encoded_bkpdve & CHROMATIC_SCALE
    context = binary_encoding_to_KPDVE(encoded_bkpdve >> 12)
    
    return chord, context
    

def binary_encoded_context_chord_pair(context, chord):
    '''

    Parameters
    ----------
    context : int of kpdve binary encoding
        0bKKKKPPPDDDVVVEEE
    chord : int of chromatic ptich class set binary encoding
        0bC-D-EF-G-A-B

    Returns
    -------
    28-bit encoding of the two values
        for transmission and analysis: KKKKPPPDDDVVVEEEC-D-EF-G-A-B  
        a musical pixel

    '''

    return (context << 12) | chord


def numpy_array_to_binary_notegroup(numpy_pclassset):
    '''
    take a 12 int numpy arrat of pitch class sets, return as int.

    Input
    -----
    np.array(5)
        pitch class set as an array [0:11] Any number
        greater than 0 becomes true...

    Returns
    -------
    int.
        a binary pitch-class set (chromatic)

    >>> 
    _to_binary_notegroup(np.array([1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]))
    3640
    '''

    bool_arr = numpy_pclassset > 0
    notegroup = 0
    for i, tf in enumerate(bool_arr):
        if tf:
            notegroup |= binary_note_at_loc(i)

    return notegroup


def binary_notegroup_to_numpy_array(notegroup):
    '''
    take a 12 int numpy array of pitch class sets, return as int.

    Input
    -------
    int.
        a binary pitch-class set (chromatic)

    Returns
    -------
    np.array(5)
        pitch class set as an array [0:11] Any number
        greater than 0 becomes true...

    >>> binary_notegroup_to_numpy_array(0b111000111000)
    array([1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0])

    '''

    np_array = np.zeros(12, dtype=int)

    for i in range(12):
        if (notegroup & LEFT_BIT) > 0:
            np_array[i] = 1
        notegroup <<= 1

    return np_array


def numpy_chrom_to_circle(a_chroma):
    circle_a = np.array([a_chroma[(i*7)%12] for i in range(12)])
    return np.roll(circle_a, 1)


def numpy_circle_to_chrom(circle_a):
    chrom_a = np.roll(circle_a, -1)
    return np.array([chrom_a[(i*7)%12] for i in range(12)])


if __name__ == "__main__":
    import doctest
    doctest.testmod()