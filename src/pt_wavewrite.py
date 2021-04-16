import pt_utils
import numpy as np

from scipy.io.wavfile import write

just_freqs = np.array([1.0,
             1.5,  
             1.125,  
             1.6875,  
             1.265625,  
             1.8984375,  
             1.423828125,  
             1.06787109375,  
             1.601806640625,  
             1.20135498046875,  
             1.802032470703125,  
             1.3515243530273438])

# =============================================================================
# NOTEGROUPS TO WAV FILES, IN 
# =============================================================================

# A SINGLE PILE OF FREQUENCIES FROM A NOTEGROUP
def notegroup_wavepile(notegroup, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal", shepard=False):
    ng = notegroup
    
    if (chromatic == False):
        ng = pt_utils.f_circle_to_c_chrom(ng)
        
    notenums = pt_utils.bit_locs(ng)
        
    return ordered_notegroup_wavepile(notenums, Fs=Fs, duration=duration, chromatic=chromatic, from_middle_c=from_middle_c, temperament=temperament, shepard=shepard)

# A SINGLE PILE OF FREQUENCIES FROM A SET OF INTEGERS 0-11

def ordered_notegroup_wavepile(notenums, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal", shepard=False):    
    freqs = []
    
    for a_note in notenums:
        p_class = a_note
        freqs.append(freq_for_chrom_pitchnum(p_class, from_middle_c=from_middle_c, temperament=temperament))
        if (shepard == True):
            freqs.append(freq_for_chrom_pitchnum(p_class, from_middle_c=from_middle_c-2, temperament=temperament))
            freqs.append(freq_for_chrom_pitchnum(p_class, from_middle_c=from_middle_c-1, temperament=temperament))

    return pile_freq_sequence(freqs, Fs=Fs, duration=duration)


# A SINGLE SEQUENCE OF FREQUENCIES FROM A NOTEGROUP

def notegroup_wavestep(notegroup, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal"):
    ng = notegroup
    
    if (chromatic == False):
        ng = pt_utils.f_circle_to_c_chrom(ng)
        
    notenums = pt_utils.bit_locs(ng)
        
    return ordered_notegroup_wavestep(notenums, Fs=Fs, duration=duration, chromatic=chromatic, from_middle_c=from_middle_c, temperament=temperament)

# A SINGLE SEQUENCE OF FREQUENCIES FROM A SET OF INTEGERS 0-11

def ordered_notegroup_wavestep(notenums, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal", shepard=False):
    freqs = []
    for a_note in notenums:
        freqs.append(freq_for_chrom_pitchnum(a_note, from_middle_c=from_middle_c, temperament=temperament))
        if (shepard == True):
            freqs.append(freq_for_chrom_pitchnum(a_note, from_middle_c=from_middle_c-2, temperament=temperament))
            freqs.append(freq_for_chrom_pitchnum(a_note, from_middle_c=from_middle_c-1, temperament=temperament))
            
    return link_freq_sequence(freqs, duration=duration)

#========================================
# LINKED SEQUENCES -- 'ORDERED' IS PITCH CLASS NUMBERS, NOT BINARY 'NOTEGROUPS'

def link_wavepile_sequences(notegroup_list, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal", shepard=False):
    '''
    return a wave file with the signals in sequence

    Returns
    -------
    a sequence of chords spread evenly over duration

    '''
    
    # set the length of each segment
    stepdur = duration/len(notegroup_list)
    
    # get a signal of that length for each notegroup
    signal = np.empty(0)
    
    for i, a_notegroup in enumerate(notegroup_list):
        signal = np.concatenate((signal, notegroup_wavepile(a_notegroup, Fs=Fs, duration=stepdur, chromatic=chromatic, from_middle_c=from_middle_c, temperament=temperament, shepard=shepard)), axis=0)

    return signal


def link_ordered_wavepile_sequences(notegroup_list, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal"):
    '''
    return a wave file with the signals in sequence


    Returns
    -------
    a sequence of chords spread evenly over duration

    '''
    
    # set the length of each segment
    stepdur = duration/len(notegroup_list)
    
    # get a signal of that length for each notegroup
    signal = np.empty(0)
    
    for i, a_notegroup in enumerate(notegroup_list):
        signal = np.concatenate((signal, ordered_notegroup_wavepile(a_notegroup, Fs=Fs, duration=stepdur, chromatic=chromatic, from_middle_c=from_middle_c, temperament=temperament)), axis=0)

    return signal


def link_wavestep_sequences(notegroup_list, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal"):
    '''
    return a wave file with the notegroup signals in sequence

    Returns
    -------
    a sequence of chords spread evenly over duration

    '''
    
    # set the length of each segment
    stepdur = duration/len(notegroup_list)
    
    # get a signal of that length for each notegroup
    signal = np.empty(0)
    
    for i, a_notegroup in enumerate(notegroup_list):
        signal = np.concatenate((signal, notegroup_wavestep(a_notegroup, Fs=Fs, duration=stepdur, chromatic=chromatic, from_middle_c=from_middle_c, temperament=temperament)), axis=0)

    return signal


def link_ordered_wavestep_sequences(notegroup_list, Fs=44100, duration=2, chromatic=False, from_middle_c=0, temperament="equal"):
    '''
    return a wave file with the signals in sequence

    Returns
    -------
    a sequence of chords spread evenly over duration

    '''
    
    # set the length of each segment
    stepdur = duration/len(notegroup_list)
    
    # get a signal of that length for each notegroup
    signal = np.empty(0)
    
    for i, a_notegroup in enumerate(notegroup_list):
        signal = np.concatenate((signal, ordered_notegroup_wavestep(a_notegroup, Fs=Fs, duration=stepdur, chromatic=chromatic, from_middle_c=from_middle_c, temperament=temperament)), axis=0)

    return signal

#========================================
# RAW FREQUENCY FUNCTIONS
def freq_for_chrom_pitchnum(pitchnum, from_middle_c=0, temperament="equal"):
    '''
    Returns a frequency value in the octave above middle C for a chromatic number 0-11
    '''
    
    p_num = pitchnum
    
    middle_c_freq = 262
    if (temperament == "just"):
        base_freq = just_freqs[(p_num * 7)  % 12]
    else:
        base_freq =  pow(2, p_num/12) 
    return middle_c_freq * base_freq * pow(2, from_middle_c)


def freq_4_note(a_note, from_middle_c=0, temperament="equal"):
    return 2 * np.pi * freq_for_chrom_pitchnum(a_note, from_middle_c=from_middle_c, temperament=temperament)

# FREQUENCY TO SIGNAL-OF-LENGTH FUNCTIONS
def signal_4_freq(freq, Fs=44100, duration=2, in_out_env=True, amp=1.0, phi=0.0):
    t = np.linspace(0, duration, int(Fs * duration))
    signal = amp * np.sin((2 * np.pi * freq) * t + phi) 
    
    if in_out_env == True:
        ramp_len = 40
        ramp = np.linspace(0, 1, num=ramp_len)
        signal[0:ramp_len] *= ramp
        signal[len(signal)-ramp_len:] *= ramp[::-1]

    return signal

def link_freq_sequence(freqs, duration=2):
    stepdur = duration/len(freqs)
    signal = np.empty(0)
    
    for a_freq in freqs:
        signal = np.concatenate((signal, signal_4_freq(a_freq, duration=stepdur)), axis=0)
        
    return signal

def pile_freq_sequence(freqs, Fs=44100, duration=2):
    t = np.linspace(0, duration, int(Fs * duration))
    signal = np.zeros_like(t)
    
    for a_freq in freqs:
        signal += signal_4_freq(a_freq, duration=duration)
        
    return signal

# numpy sequence becomes wave file.
def norm_wave_write(seq, filename, sr=44100):
    # normalize the sum of the waves...
    seq /= seq.max()*1.5
    write(filename, sr, seq)