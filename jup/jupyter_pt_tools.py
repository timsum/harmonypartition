#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:55:26 2020

@author: johntimothysummers
"""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy.io.wavfile import write

import IPython.display as ipd

# from harmonypartition bundle
import pt_utils
import pt_naming_conventions
import pt_keypattern
import pt_musicutils
import harmony_state

# from previous pypartita dev
# depends also on pt_graphics... but doesn't have to...
import pt_analyzeaudio

hue = 0.27
sat = 0.9
light = 0.7

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

def numpy_array_by_circleindex(np_array):
    return np.array([(arr_val * i)/12.0 for i, arr_val in enumerate(np_array)])

def numpy_matrix_by_circleindex(np_matrix):
    return np.array([numpy_array_by_circleindex(an_array) for an_array in np_matrix])

def kpdve_heatmap(kpdve):
    '''
    takes a kpdve and turns it to a list, calling 'multiple_kpdve_heatmap'
    '''
    return multiple_kpdve_heatmap(np.reshape(kpdve, (1, 5)))

def multiple_kpdve_heatmap(kpdve_list, yticks=[], title=None):
    '''
    takes a kpdve list and turns it to a heatmap
    '''
        
    # get the binary values corresponding to the kpdve list
    states = [harmony_state.harmony_state(kpdve) for kpdve in kpdve_list]
    notegroup_list = np.array([pt_utils.c_chrom_to_f_circle(a_state.current_binary) for a_state in states])
    np_notegroup_list = np.array([pt_utils.binary_notegroup_to_numpy_array(ng) for ng in notegroup_list])
    np_notegroup_list_clr = numpy_matrix_by_circleindex(np_notegroup_list)
    
    # make a mask
    mask = 1 - np_notegroup_list
    
    # make a list of rgb tuples with sb.hls_palette()
    rgbtups =  sb.hls_palette(12, h=hue, l=light, s=sat)
    #[sb.set_hls_values(0, h=a_kpdve[2], l=a_kpdve[1], s=a_kpdve[2]) for a_kpdve in kpdve_list]
    
    # use that as a colormap in the sb heatmap 
    # seaborn.hls_palette(n_colors=12, h=0.01, s=0.9, l=0.65, as_cmap=False)¶
    
    fig, ax = plt.subplots(figsize=(6, len(np_notegroup_list)/2.0))
    ticknames = pt_naming_conventions.circle_fifth_notes()
    
    sb.set(font_scale=1.4)
    sb.heatmap(np_notegroup_list_clr,
               ax=ax,
               mask=1-np_notegroup_list,
               xticklabels=ticknames, 
               yticklabels=yticks,
               linewidths=1,
               cmap=rgbtups,
               cbar=False, 
               vmin=0,
               vmax=1)
    
    ax.set_title(title, fontsize=16)
    plt.show()

    
    

def notegroup_heatmap(notegroup, chromatic=False, title=None):
    np_notegroup = np.array([notegroup])
    return multiple_notegroup_heatmap(np_notegroup, chromatic, title=title)


def multiple_notegroup_heatmap(notegroup_list, chromatic=False, yticks=[], title=None):
    np_notegroup_list = np.array([pt_utils.binary_notegroup_to_numpy_array(ng) for ng in notegroup_list])
    np_notegroup_list_clr = numpy_matrix_by_circleindex(np_notegroup_list)
    
    fig, ax = plt.subplots(figsize=(6, len(np_notegroup_list)/2.0))
    ticknames = pt_naming_conventions.circle_fifth_notes() if chromatic == False else pt_naming_conventions.chromatic_notes()

    # for this... hm... always want it?
    
    # if it's NOT chromatic (default) everything has to be reconfigured to be analyzed...
    # y_ticknames = []
    
    sb.set(font_scale=1.4)
    sb.heatmap(np_notegroup_list_clr,
               ax=ax,
               mask=1-np_notegroup_list,
               xticklabels=ticknames, 
               yticklabels=yticks,
               linewidths=1,
               cmap=sb.husl_palette(12, h=hue, l=light, s=sat),
               cbar=False, 
               vmin=0,
               vmax=1)
    
    ax.set_title(title, fontsize=16)
    plt.show()
    
    return np_notegroup_list


# def kpdve_notegroup_graph(notegroup_list, title):
#     '''
#     takes a notegroup list (from an analysis and graphs it above key, pattern, and degree)
#     '''
#     np_notegroup_list = np.array([pt_utils.binary_notegroup_to_numpy_array(ng) for ng in notegroup_list])
#     np_notegroup_list_clr = numpy_matrix_by_circleindex(np_notegroup_list)

#     # flip it horizontal
#     np_notegroup_list = np_notegroup_list.T
#     np_notegroup_list_clr = np_notegroup_list_clr.T
    
#     np_notegroup_list = np.flipud(np_notegroup_list)
#     np_notegroup_list_clr = np.flipud(np_notegroup_list_clr)
    
#     sb.heatmap(np_notegroup_list_clr,
#                ax=ax,
#                mask=1-np_notegroup_list,
#                xticklabels=xticks, 
#                yticklabels=yticks, 
#                cbar=False, 
#                cmap=sb.husl_palette(12, h=hue, l=light, s=sat),
#                vmin=0,
#                vmax=1)
    
#     ax.set_title(title, fontsize=16)
#     plt.show()   

def horizontal_notegroup_heatmap(notegroup_list, chromatic=False, xticks=[], title=None):
    np_notegroup_list = np.array([pt_utils.binary_notegroup_to_numpy_array(ng) for ng in notegroup_list])
    np_notegroup_list_clr = numpy_matrix_by_circleindex(np_notegroup_list)

    # flip it horizontal
    np_notegroup_list = np_notegroup_list.T
    np_notegroup_list_clr = np_notegroup_list_clr.T
    
    np_notegroup_list = np.flipud(np_notegroup_list)
    np_notegroup_list_clr = np.flipud(np_notegroup_list_clr)


    fig, ax = plt.subplots(figsize=(17, 3))
    yticks = pt_naming_conventions.circle_fifth_notes() if chromatic == False else pt_naming_conventions.chromatic_notes()
    yticks.reverse()
    # for this... hm... always want it?
    
    # if it's NOT chromatic (default) everything has to be reconfigured to be analyzed...
    # y_ticknames = []
    
    
    sb.heatmap(np_notegroup_list_clr,
               ax=ax,
               mask=1-np_notegroup_list,
               xticklabels=xticks, 
               yticklabels=yticks, 
               cbar=False, 
               cmap=sb.husl_palette(12, h=hue, l=light, s=sat),
               vmin=0,
               vmax=1)
    
    ax.set_title(title, fontsize=16)
    plt.show()
    
    return np_notegroup_list

# def heatmap_for_midi_file(filename, key_orientation=np.array([0,0,0,4,3])):
#     bin_a, kpdve_a = pt_analyzeaudio.analyze_notation_file(filename, key_orientation)
#     bin_seq = [pt_keypattern.get_binary_KPDVE_chord(a_kpdve) for a_kpdve in kpdve_a]
#     # funcs = [pt_naming_conventions.chord_function_in_key(a_kpdve) for a_kpdve in kpdve_a]
#     return horizontal_notegroup_heatmap(bin_seq)
    
#     # return bin_a

# def d_val_heatmap():
#     # should go dark for higher d vals 
#     pass
    

# =============================================================================
# NEGATIVIZE
# =============================================================================

def negativize(a_kpdve):
    k = (a_kpdve[0] + 9) % 12
    p = 3 if a_kpdve[2] == 2 else 0
    d = 7 - a_kpdve[2]
    v = 7 - a_kpdve[3]
    e = a_kpdve[4]
    return np.array([k,p,d,v,e])

# =============================================================================
# NEW STANDARD HEATMAP
# =============================================================================

    
def heatmap_col_mask_for_kpdve_bin(a_kpdve, ng):
    k = (pt_utils.single_bit_loc(pt_musicutils.circle_conv_lyd_center_for_KPDVE(a_kpdve))) % 12
    p = (pt_utils.single_bit_loc(pt_musicutils.circle_conv_tonic_for_KPDVE(a_kpdve))) % 12
    d = (pt_utils.single_bit_loc(pt_musicutils.circle_root_note_for_KPDVE(a_kpdve))) % 12
    e = (pt_utils.single_bit_loc(pt_musicutils.circle_ext_note_for_KPDVE(a_kpdve))) % 12

    kpd_part = [k, p, d]
    msk_lin = [1]
    
    ng_circ = pt_utils.c_chrom_to_f_circle(ng) 
    bin_notes = pt_utils.binary_notegroup_to_numpy_array(ng_circ)
    
    notes = list(bin_notes * np.array([i for i in range(12)]))
    mask = np.array([0,0,0] + (msk_lin * 2) + list(1-bin_notes))

    full_column = np.array(kpd_part + (msk_lin * 2) + notes)
    return full_column, mask

def data_and_mask_for_kpdve_a_bin_a_heatmap(kpdve_a, bin_a):
    heatmap = []
    mask = []
    for k, b in zip(kpdve_a, bin_a):
        col, msk = heatmap_col_mask_for_kpdve_bin(k, b)
        heatmap.append(np.flipud(col))
        mask.append(np.flipud(msk))

    return np.array(heatmap).T, np.array(mask).T

def bin_a_kpdve_a_heatmap(bin_a, kpdve_a, title=None):
    data, mask = data_and_mask_for_kpdve_a_bin_a_heatmap(kpdve_a, bin_a)

    hue = 0.27
    sat = 1.0
    light = 0.8
    fig, ax = plt.subplots(figsize=(17, 3))

    spacer_tick = ["=="]
    yticks = ["k", "p", "d"] + spacer_tick * 2 + pt_naming_conventions.circle_fifth_notes()
    yticks = yticks[::-1]
    sb.heatmap(data,
               ax=ax,
               mask=mask,
               cbar=False, 
               cmap=sb.husl_palette(12, h=hue, l=light, s=sat),
               xticklabels=[], 
               yticklabels=yticks,
               vmin=0,
               vmax=11)
    
    ax.set_facecolor("black")
    ax.set_title(title, fontsize=16)
    plt.show()
# =============================================================================
# CHROMA TOOLS
# =============================================================================

def switch_chroma(chroma):
    chr_switched = np.zeros(chroma.shape)
    
    for i in range(12):
        chr_switched[i] = chroma[(i * 7) % 12] # +1 gets f to the bottom...
    
    return np.roll(chr_switched, 1, axis=0)

    
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