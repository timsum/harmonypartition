#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:47:41 2020

@author: timsummers
"""

import numpy as np
import librosa

import harmony_state
import pt_utils
import pt_musicutils

import matplotlib.pyplot as plt
from matplotlib import gridspec as gridspec
import seaborn as sb




def graph_audio_file(filename, key_orientation=np.array([0,0,0,4,3]), chroma_threshold=0.5, filter_chroma=True):
    y, sr, X, bin_a, kpdve_a, chroma_a = assemble_audio_kpdve_analysis(filename, key_orientation, chroma_threshold=chroma_threshold, filter_chroma=filter_chroma)
    graph_waveform_kpdve_combo(y, sr, bin_a, kpdve_a)
    

def assemble_audio_kpdve_analysis(filename, key_orientation=np.array([0,0,0,4,3]), chroma_threshold=0.5, filter_chroma=True):
    y, sr, chroma_a = chroma_analyze_audiofile(filename, 
                                               hop_length=2048, 
                                               filter_chroma=filter_chroma)

    bin_a, kpdve_a = analyze_chroma_list(chroma_a, 
                                         threshold=chroma_threshold,
                                         key_orientation=key_orientation)

    X = librosa.stft(y)

    return y, sr, X, bin_a, kpdve_a, chroma_a


def kpdve_analyze_audiofile(filename, key_orientation=np.array([0,0,0,4,3]), chroma_threshold=0.5, filter_chroma=True):
    _, _, _, bin_a, kpdve_a, _ = assemble_audio_kpdve_analysis(filename, key_orientation, chroma_threshold=chroma_threshold, filter_chroma=filter_chroma)
    return bin_a, kpdve_a


# CHROMA TOOLS
# 1AB
def chroma_list_to_binary_list(a_chroma, threshold=0.5):
    '''

    Parameters
    ----------
    a_chroma : np_array(chroma.size)
        a chroma analysis of an audio file

    Returns
    -------
    bin_chroma :
        the same reduced to a list of 12-bit integers 
        (chromatic pitch class set)
        a single list of numbers

    '''

    bin_chroma = np.zeros(a_chroma.shape[1], dtype=int)

    for i in range(a_chroma.shape[1]):
        notegroup = 0
        count = 0
        bin_chroma[i] = chroma_to_binary_value(a_chroma[:, i], threshold)

    return bin_chroma

# 1AC
def chroma_to_binary_value(chroma_stripe, threshold=0.5):
    '''
    Make a binary notegroup value out of a single chroma vector

    Parameters
    ----------
    chroma : np.array(12, 1)
        12 values of the chromatic scale, mesured 0-1

    Returns
    -------
    12-bit notegroup integer

    '''
    notegroup = 0
    count = 0
    
    for a_val in chroma_stripe:
        if a_val > threshold :
            notegroup |= pt_utils.LEFT_BIT >> count
        count += 1
    return notegroup

# 1AA
def analyze_chroma_list(chroma, threshold=0.5, key_orientation=np.array([0,0,0,4,2])):
    '''
    given the chroma list of a mp3 file, perform a matching KPDVE analysis

    Parameters
    ----------
    chroma :
        a chroma list from an audio file
    threshold (optional):
        the intensity beyond which a chroma gets marked as a 'yes'

    Returns
    -------
    binary, and KPDVE analyses as tuple

    '''

    h = harmony_state.harmony_state(start_kpdve=key_orientation)

    # make a binary version for particular naming -- binary chroma is a single 12-bit integer
    binary_chroma = chroma_list_to_binary_list(chroma, threshold)
    kpdve_chroma = np.zeros((binary_chroma.shape[0], 5), dtype=int)

    for i, ng in np.ndenumerate(binary_chroma):
        h.change_notegroup(ng)
        kpdve_chroma[i] = h.current_kpdve.copy()
    
    return binary_chroma, kpdve_chroma

# =============================    
# 1A GET AUDIO TO ANALYZABLE FORM
def chroma_analyze_audiofile(filename, hop_length=1024, filter_chroma=True):
    '''
    

    Parameters
    ----------
    filename : an audio file 
        file must be of Librosa accepted ty     pe.
    hop_length : int, optional
        fourier transform hop. The default is 1024.
    key_orientation : ndarray(5), a valid KPDVE location, optional
        for starting the analysis, a location indicating key. The default is np.array([0,0,0,4,2]).
    filter_chroma : bool, optional
        do k-neighbor filtering in librosa. The default is True.

    Returns
    -------
    tuple: y, sr, chroma_a
    '''
    
    y, sr = librosa.load(filename)
    # chroma_a = librosa.feature.chroma_cqt(y=y,
    #                                       sr=sr,
    #                                       bins_per_octave=12*3,
    #                                       hop_length=hop_length)
    
    chroma_a = librosa.feature.chroma_stft(y=y,
                                          sr=sr)

    if (filter_chroma):
        chroma_a = np.minimum(chroma_a,
                              librosa.decompose.nn_filter(chroma_a,
                                                          aggregate=np.mean,
                                                          metric='cosine'))
        
    return y, sr, chroma_a


def graph_chroma(chroma_a):
    fig = plt.figure(frameon=False, figsize=(12, 1))
    sb.heatmap(chroma_a,
               xticklabels=False,
               yticklabels=False,
               cbar=False)
    

def graph_waveform_kpdve_combo(y, sr, bin_a, kpdve_a):
    # PYPLOT
    # FIGSIZE IS HERE ADJUSTED TO BEST SHOW ON JUPYTER. NO FIGSIZE IS BEST FOR WEB
    fig = plt.figure(frameon=False, figsize=(12, 2))
#    fig = plt.figure(frameon=False)

    plt.style.use('dark_background')

    g_spec = gridspec.GridSpec(nrows=50, ncols=1, figure=fig)
    g_spec.update(wspace=0, hspace=0)

    ax_wave = fig.add_subplot(g_spec[:25, :])
    librosa.display.waveplot(y=y, sr=sr, x_axis=None)
    
    plt.subplots_adjust(0,0,1,1,0,0)
    for ax in fig.axes:
        ax.axis('off')
        ax.margins(0,0)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        
    ax_kpdve_ve = fig.add_subplot(g_spec[25:, :])
    graphable = kpdve_list_to_heatmap_graphable(kpdve_a).T
    graphable = np.flip(graphable, axis=0)
    sb.heatmap(graphable,
               ax=ax_kpdve_ve,
               xticklabels=False,
               yticklabels=False, 
                      cmap='hsv', 
                      cbar=False, 
                      vmin=0)
    
    plt.show()
            
def kpdve_list_to_heatmap_graphable(kpdve_list):
    return np.array([KPDVE_to_heatmap_display(a_kpdve) for a_kpdve in kpdve_list])

# HEATMAP SIMPLE
def KPDVE_to_heatmap_display(a_kpdve):
    '''
    returns a vector of length 4 with [K,P, D, E ordered chord notes... up to 7] 
    THIS IS FOR HEATMAP REPRESENTATIONS

    Parameters
    ----------
    a_kpdve : ndarray(5)
        a kpdve location .

    Returns
    -------
    a segment in a series of values for a readable heatmap of pitches
    
    '''
    
    k = (pt_utils.single_bit_loc(pt_musicutils.circle_conv_lyd_center_for_KPDVE(a_kpdve)) + 11) % 12
    p = (pt_utils.single_bit_loc(pt_musicutils.circle_conv_tonic_for_KPDVE(a_kpdve)) + 11) % 12
    d = (pt_utils.single_bit_loc(pt_musicutils.circle_root_note_for_KPDVE(a_kpdve)) + 11) % 12
    e = (pt_utils.single_bit_loc(pt_musicutils.circle_ext_note_for_KPDVE(a_kpdve)) + 11) % 12
    kpde = np.array([k, p, d, d,d,d,d,d,d,d,d,d,d,d,d,d, e]) # separate the hidden state measurements for visual clarity

    return kpde