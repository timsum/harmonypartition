#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:55:26 2020

@author: johntimothysummers
"""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

import IPython.display as ipd

# from harmonypartition bundle
import pt_utils
import pt_naming_conventions
import pt_keypattern

# from previous pypartita dev
# depends also on pt_graphics... but doesn't have to...
import partita_music21


def notegroup_heatmap(notegroup, chromatic=False, title=None):
    np_notegroup = np.array([notegroup])
    multiple_notegroup_heatmap(np_notegroup, chromatic)


def multiple_notegroup_heatmap(notegroup_list, chromatic=False, yticks=[], title=None):
    np_notegroup_list = np.array([pt_utils.binary_notegroup_to_numpy_array(ng) for ng in notegroup_list])
    
    fig, ax = plt.subplots(figsize=(12, len(np_notegroup_list)))
    ticknames = pt_naming_conventions.circle_fifth_notes() if chromatic == False else pt_naming_conventions.chromatic_notes()

    # for this... hm... always want it?
    
    # if it's NOT chromatic (default) everything has to be reconfigured to be analyzed...
    # y_ticknames = []
    
    
    sb.set(font_scale=1.4)
    sb.heatmap(np_notegroup_list,
               ax=ax,
               xticklabels=ticknames, 
               yticklabels=yticks,
               linewidths=1,
               cbar=False, 
               vmin=0)
    
    ax.set_title(title, fontsize=16)
    plt.show()


def horizontal_notegroup_heatmap(notegroup_list, chromatic=False, xticks=[], title=None):
    np_notegroup_list = np.array([pt_utils.binary_notegroup_to_numpy_array(ng) for ng in notegroup_list])
    np_notegroup_list = np_notegroup_list.T
    np_notegroup_list = np.flipud(np_notegroup_list)
    
    
    fig, ax = plt.subplots(figsize=(17, 3))
    yticks = pt_naming_conventions.circle_fifth_notes() if chromatic == False else pt_naming_conventions.chromatic_notes()
    yticks.reverse()
    # for this... hm... always want it?
    
    # if it's NOT chromatic (default) everything has to be reconfigured to be analyzed...
    # y_ticknames = []
    
    
    sb.heatmap(np_notegroup_list,
               ax=ax,
               xticklabels=xticks, 
               yticklabels=yticks, 
               cbar=False, 
               vmin=0)
    
    ax.set_title(title, fontsize=16)
    plt.show()

def heatmap_for_midi_file(filename, key_orientation=np.array([0,0,0,4,3])):
    bin_a, kpdve_a = partita_music21.analyze_notation_file(filename, key_orientation)
    bin_seq = [pt_keypattern.get_binary_KPDVE_chord(a_kpdve) for a_kpdve in kpdve_a]
    # funcs = [pt_naming_conventions.chord_function_in_key(a_kpdve) for a_kpdve in kpdve_a]
    horizontal_notegroup_heatmap(bin_seq)
    return bin_a

def d_val_heatmap():
    # should go dark for higher d vals 
    pass
    
# =============================================================================
# CHROMA TOOLS
# =============================================================================

def switch_chroma(chroma):
    chr_switched = np.zeros(chroma.shape)
    
    for i in range(12):
        chr_switched[i] = chroma[(i * 7) % 12] # +1 gets f to the bottom...
    
    return np.roll(chr_switched, 1, axis=0)


def freq_for_chrom_pitchnum(pitchnum, from_middle_c=0):
    '''
    Returns a frequency value in the octave above middle C for a chromatic number 0-11
    '''
    middle_c_freq = 262
    return middle_c_freq * pow(2, pitchnum/12) * pow(2, from_middle_c)


def freq_for_circle_pitch_num(pitchnum):
    '''
    get a pure 3/2 ratio pitch

    '''
    # DO THIS LATER!!!
    
# =============================================================================
# WAVES
# =============================================================================
    
def notegroup_wavepile(notegroup, Fs=4000, duration=2, chromatic=False, from_middle_c=0):
    ng = notegroup
    if (chromatic == False):
        ng = pt_utils.f_circle_to_c_chrom(ng)
        
    notenums = pt_utils.bit_locs(ng)
    t = np.linspace(0, duration, int(Fs * duration))

    signal = np.zeros_like(t)
    for a_note in notenums:
        signal = signal + np.sin(2 * np.pi * freq_for_chrom_pitchnum(a_note, from_middle_c=from_middle_c) * t)
        
    return signal


def notegroup_wavestep(notegroup, Fs=4000, duration=2, chromatic=False, from_middle_c=0):
    ng = notegroup
    if (chromatic == False):
        ng = pt_utils.f_circle_to_c_chrom(ng)
        
    notenums = pt_utils.bit_locs(ng)
    
    stepdur = duration/len(notenums)
    steplength = int(Fs * stepdur)
    
    t_whole = np.linspace(0, duration, int(Fs * duration))
    t = np.linspace(0, stepdur, steplength)

    signal = np.zeros_like(t_whole)
    for i, a_note in enumerate(notenums):
        signal[i*steplength:(i+1)*steplength] = np.sin(2 * np.pi * freq_for_chrom_pitchnum(a_note, from_middle_c=from_middle_c) * t)
        
    return signal


def link_wavepile_sequences(notegroup_list, Fs=4000, duration=2, chromatic=False, from_middle_c=0):
    '''
    return a wave file with the signals in sequence

    Parameters
    ----------
    notegroup_list : TYPE
        DESCRIPTION.
    duration : TYPE
        DESCRIPTION.
    Fs : TYPE
        DESCRIPTION.

    Returns
    -------
    a sequence of chords spread evenly over duration

    '''
    
    # set the length of each segment
    stepdur = duration/len(notegroup_list)
    
    # get a signal of that length for each notegroup
    signal = np.empty(0)
    
    for i, a_notegroup in enumerate(notegroup_list):
        signal = np.concatenate((signal, notegroup_wavepile(a_notegroup, Fs=Fs, duration=stepdur, chromatic=chromatic, from_middle_c=from_middle_c)), axis=0)

    return signal

def link_wavestep_sequences(notegroup_list, Fs=4000, duration=2, chromatic=False, from_middle_c=0):
    '''
    return a wave file with the signals in sequence

    Parameters
    ----------
    notegroup_list : TYPE
        DESCRIPTION.
    duration : TYPE
        DESCRIPTION.
    Fs : TYPE
        DESCRIPTION.

    Returns
    -------
    a sequence of chords spread evenly over duration

    '''
    
    # set the length of each segment
    stepdur = duration/len(notegroup_list)
    
    # get a signal of that length for each notegroup
    signal = np.empty(0)
    
    for i, a_notegroup in enumerate(notegroup_list):
        signal = np.concatenate((signal, notegroup_wavestep(a_notegroup, Fs=Fs, duration=stepdur, chromatic=chromatic, from_middle_c=from_middle_c)), axis=0)

    return signal

    