#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 23:41:18 2020

@author: johntimothysummers
"""


import numpy as np

import pt_utils
import pt_kpdve_list_optimize
import pt_musicutils
import pt_keypattern

from matplotlib import pyplot as plt
from matplotlib import colors as clr
from matplotlib import cm
from matplotlib import gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D

import librosa
import librosa.display


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
    ndarray(9).
    
    >>> KPDVE_as_array_of_notes([0,0,0,4,3])
    array([1, 1, 0, 5])
    '''
    
    k = pt_utils.single_bit_loc(pt_musicutils.circle_conv_lyd_center_for_KPDVE(a_kpdve))
    p = pt_utils.single_bit_loc(pt_musicutils.circle_conv_tonic_for_KPDVE(a_kpdve))
    d = pt_utils.single_bit_loc(pt_musicutils.circle_root_note_for_KPDVE(a_kpdve))
    e = pt_utils.single_bit_loc(pt_musicutils.circle_ext_note_for_KPDVE(a_kpdve))
    kpde = np.array([k, p, d, d,d,d,d,d,d,d,d,d,d,d,d,d, e]) # separate the hidden state measurements for visual clarity

    return kpde


# HEATMAP WITH DVE PILES
def KPDVE_to_heatmap_dve_complexity(a_kpdve):
    '''
    returns a vector of length 9 with [K,P, DVE ordered chord notes... up to 7] 

    Parameters
    ----------
    a_kpdve : ndarray(5)
        a kpdve location .

    Returns
    -------
    ndarray(9).
    
    >>> KPDVE_as_array_of_notes([0,0,0,4,3])
    array([1, 1, 0, 4, 1, 5])
    '''
    
    k = pt_utils.single_bit_loc(pt_musicutils.circle_conv_lyd_center_for_KPDVE(a_kpdve))
    p = pt_utils.single_bit_loc(pt_musicutils.circle_conv_tonic_for_KPDVE(a_kpdve))
    kp = np.array([k, p, -1]) # separate the hidden state measurements for visual clarity
    dve = pt_keypattern.get_ordered_chord_notes(a_kpdve)
    kpdve = np.concatenate((kp, dve))
    kpdve = (kpdve + 11) % 12 # is this right??
    kpdve[2] = -1
    return np.pad(kpdve, (0, 10-kpdve.shape[0]), mode='constant', constant_values=(0, -1))

def kpdve_list_colormap(kpdve_list):
    '''
    Generate a colormap list for a kpdve list

    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        DESCRIPTION.

    Returns
    -------
    np.array(kpdve_list_length)

    '''

    # create colormap for graphing
    kpdve_norm = np.zeros(kpdve_list.shape[0])
    for i, a_kpdve in enumerate(kpdve_list):
        kpdve_norm[i] = kpdve_colormap_value_mixed(a_kpdve)

    return kpdve_norm


def kpdve_colormap_value(a_kpdve):
    '''
    Returns a float value from 0-1 for a kpdve vector

    Parameters
    ----------
    a_kpdve : np.array(5)
        a_kpdve vector

    Returns
    -------
    float:
        a value for the KPDVE index as a percentage of the complete 16-bit space.... KKKKPPPDDDVVVEEE

    '''

    return pt_utils.KPDVE_to_binary_encoding(a_kpdve) / 0b1011110110110110

# =============================================================================
# color by param k, p, d
# =============================================================================


def kpd_list_colormap(kpdve_list, param=0):
    '''
    Generate a colormap list for a k or p or d, by param...

    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        DESCRIPTION.

    Returns
    -------
    np.array(kpdve_list_length)

    '''

    # create colormap for graphing
    kpdve_norm = np.zeros(kpdve_list.shape[0])
    for i, a_kpdve in enumerate(kpdve_list):
        kpdve_norm[i] = kpd_colormap_value_by_param(a_kpdve, param)

    return kpdve_norm


def kpd_list_function_colormap(kpdve_list):
    '''
    Generate a colormap list for a k or p or d, by param...

    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        DESCRIPTION.

    Returns
    -------
    np.array(kpdve_list_length)

    '''

    # create colormap for graphing
    kpdve_norm = np.zeros(kpdve_list.shape[0])
    for i, a_kpdve in enumerate(kpdve_list):
        kpdve_norm[i] = kpd_colormap_d_function(a_kpdve)

    return kpdve_norm

def kpd_list_pattern_entropy_colormap(kpdve_list):
    '''
    Generate a colormap list for a k or p or d, by param...

    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        DESCRIPTION.

    Returns
    -------
    np.array(kpdve_list_length)

    '''

    # create colormap for graphing
    kpdve_norm = np.zeros(kpdve_list.shape[0])
    for i, a_kpdve in enumerate(kpdve_list):
        kpdve_norm[i] = kpd_colormap_p_distance(a_kpdve)

    return kpdve_norm

def kpd_colormap_value_by_param(a_kpdve, param=0):
    '''
    Returns a float value from 0-1 for a kpdve vector for a colormap

    Parameters
    ----------
    a_kpdve : np.array(5)
        a_kpdve vector
    param : k, p, d

    Returns
    -------
    float: 
        root-based colormap value
     
    >>> kpd_colormap_value_by_param(np.array([0,0,0,4,3]), param=0)
    0.0
        
    >>> kpd_colormap_value_by_param(np.array([0,0,0,4,3]), param=2)
    0.9166666666666666
    
    >>> kpd_colormap_value_by_param(np.array([1,0,0,4,3]), param=0)
    0.08333333333333333
    '''
    
    pitchval = 0
    
    if param == 0:
        pitchval = pt_utils.single_bit_loc(pt_musicutils.circle_conv_lyd_center_for_KPDVE(a_kpdve))
    elif param == 1:
        pitchval = pt_utils.single_bit_loc(pt_musicutils.circle_conv_tonic_for_KPDVE(a_kpdve))
    elif param == 2:
        pitchval = pt_utils.single_bit_loc(pt_musicutils.circle_root_note_for_KPDVE(a_kpdve))
    elif param == 3:
        pitchval = pt_utils.single_bit_loc(pt_musicutils.circle_ext_note_for_KPDVE(a_kpdve))
    
    return (pitchval + 11) % 12 / 12.0  # because it is just NICER to have C Major in red.


def kpd_colormap_d_function(a_kpdve):
    '''
    Returns a float value from 0-1 for a kpdve vector, 

    Parameters
    ----------
    a_kpdve : np.array(5)
        a_kpdve vector

    Returns
    -------
    float: 
        root - conventional tonic value = function value (0-6) / 6

    '''
    
    return pt_musicutils.circle_conv_function_for_KPDVE(a_kpdve) / 6.0


def kpd_colormap_p_distance(a_kpdve):
    '''
    Returns a float value from 0-1 for a kpdve vector, 

    Parameters
    ----------
    a_kpdve : np.array(5)
        a_kpdve vector

    Returns
    -------
    float: 
        root - conventional tonic value = function value (0-6) / 6

    '''
    
    val = a_kpdve[1];
    if val > 3:
        val = abs(val - 7)
    return val / 3.0

# =============================================================================
# mix colors kpd
# =============================================================================

def kpd_colormap_value_mixed(a_kpdve):
    '''
    Returns a float value from 0-1 for a kpdve vector

    Parameters
    ----------
    a_kpdve : np.array(5)
        a_kpdve vector

    Returns
    -------
    float: 
        root-based coloring system... not really ready for prime=time

    '''
    
    colors = np.array([kpd_colormap_value_by_param(a_kpdve, i)for i in range(4)])
    balance_array = np.array([0.1, 0.2, 0.35, 0.35])
    
    return np.sum(colors * balance_array)

def kpdve_colormap_value_mixed(a_kpdve):
    '''
    Returns a float value from 0-1 for a kpdve vector

    Parameters
    ----------
    a_kpdve : np.array(5)
        a_kpdve vector

    Returns
    -------
    float: 
        root-based coloring system... not really ready for prime=time

    '''
    
    colors = np.array([kpd_colormap_value_by_param(a_kpdve, i)for i in range(4)])
    balance_array = np.array([0.05, 0.35, 0.5, 0.1])
    
    return np.sum(colors * balance_array)

# =============================================================================
# common subplots
# =============================================================================

def subplot_waveform(y, sr, ax, label=None):
    ax.set_title(label)
    librosa.display.waveplot(y=y, sr=sr, x_axis=None)
    

def subplot_spectrum(y, sr, ax, label=None):
    ax.set_title(label)
    C = np.abs(librosa.cqt(y=y, sr=sr, bins_per_octave=12, n_bins=7*12))
    librosa.display.specshow(librosa.amplitude_to_db(C, 
                                                     ref=np.max), 
                                                     y_axis=None, 
                                                     bins_per_octave=12)


def subplot_chroma(chroma, ax, label=None):
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    librosa.display.specshow(chroma)


def subplot_binary_analysis(bin_analysis):
    '''
    should plot binary analyses in a manner equivalent to *chroma*

    Parameters
    ----------
    bin_analysis : np.array(n)
        integer list of analyzed notegroups in a piece or segment

    Returns
    -------
    draws subplot

    '''
    pass


def subplot_analyzed_waveform(y, sr, kpdve_analysis, ax, label=None):
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
 
# =============================================================================
#     kpdve_norm = kpdve_list_colormap(kpdve_analysis)
#     colors = [cm.hsv(x) for x in kpdve_norm]
# 
#     for i, cl in enumerate(colors):
#         ax.axvline(i, color=cl)
# =============================================================================

    librosa.display.waveplot(y=y, sr=sr, cmap='hsv', x_axis='none')


# =============================================================================
# time plots
# =============================================================================

def subplot_kpdve(kpdve_analysis, ax, label=None, show_d=False):
    '''
    make a subplot of a kpdve analysis of a file (can be of origin
    notation or audio)

    Parameters
    ----------
    kpdve_analysis : TYPE
        DESCRIPTION.
    ax : TYPE
        DESCRIPTION.
    label : TYPE, optional
        DESCRIPTION. The default is 'kpdve'.

    Returns
    -------
    None.
        plots data
    '''

    ax.margins(0.0)
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    kpdve_norm = kpdve_list_colormap(kpdve_analysis)
    colors = [cm.hsv(x) for x in kpdve_norm]
    alph_norm = [(0.8*(1-a) + 0.2) for a in kpdve_analysis[:, 2] / 6.0]
    #  alph_norm = [(0.8*(1-a) + 0.2) for a in kpd_list_function_colormap(kpdve_analysis)]

    for i, cl in enumerate(colors):
        ax.axvline(i, color=cl, alpha=alph_norm[i])

#   # THIS IS A RATHER NICE EFFECT, BUT PERHAPS ANOTHER WAY OF GRAPHING
        # D MAKES MORE ANALYTICAL SENSE.
    if (show_d):
        d_norm = (kpdve_analysis[:, 2] / 100.0)
        for i, alpha in enumerate(d_norm):
            ax.axvline(i, color='white', alpha=alpha)


def subplot_kpd_param(kpdve_analysis, ax, param=0, label=None):
    ax.margins(0.0)
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    kpdve_norm = kpd_list_colormap(kpdve_analysis, param)
    ht = np.shape(kpdve_norm)[0] // 40
    
    # kpdve_norm = np.expand_dims(kpdve_norm, axis=0)
    kpdve_norm = np.tile(kpdve_norm, (ht, 1))
    ax.imshow(kpdve_norm, cmap=cm.hsv)
    # colors = [cm.hsv(x) for x in kpdve_norm]

    # for i, cl in enumerate(colors):
    #     ax.axvline(i, color=cl)


def subplot_d_functions(kpdve_analysis, ax, label=None):
    ax.margins(0.0)
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    kpdve_norm = kpd_list_function_colormap(kpdve_analysis)
    colors = [cm.copper(x) for x in kpdve_norm]

    for i, cl in enumerate(colors):
        ax.axvline(i, color=cl)
        
def subplot_p_disturbance(kpdve_analysis, ax, label=None):
    ax.margins(0.0)
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    kpdve_norm = kpd_list_pattern_entropy_colormap(kpdve_analysis)
    colors = [cm.copper(x) for x in kpdve_norm]

    for i, cl in enumerate(colors):
        ax.axvline(i, color=cl)


def subplot_kpdve_change(kpdve_analysis, ax, label=None):
    '''
    make a subplot of a kpdve analysis of a file (can be of origin
    notation or audio)

    Parameters
    ----------
    kpdve_analysis : TYPE
        DESCRIPTION.
    ax : TYPE
        DESCRIPTION.
    label : TYPE, optional
        DESCRIPTION. The default is 'kpdve'.

    Returns
    -------
    None.
        plots data
    '''

    kpdve_change = pt_kpdve_list_optimize.kpdve_distance_list(kpdve_analysis)

    ax.margins(0.0)
    ax.set_title(label)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    kpdve_norm = np.zeros(kpdve_analysis.shape[0])
    for i, a_kpdve in enumerate(kpdve_change):
        kpdve_norm[i] = pt_utils.KPDVE_to_binary_encoding(a_kpdve) / 0b0110110110110110 + 0.5
    
    colors = [cm.coolwarm(x) for x in kpdve_norm]

    for i, cl in enumerate(colors):
        ax.axvline(i, color=cl)



def ccmf_waveform_kpdve_graph(y, sr, kpdve_analysis, filename, showtitle=False):
    # PYPLOT
    fig = plt.figure(frameon=False)
    
    plt.style.use('dark_background')

    if(showtitle):
        plt.title(filename)

    g_spec = gridspec.GridSpec(nrows=100, ncols=1, figure=fig)
    g_spec.update(wspace=0, hspace=0)


    ax_wave = fig.add_subplot(g_spec[:17, :])
    subplot_waveform(y, sr, ax_wave)
    
    # ext_note (ve)
    ax_kpdve_ve = fig.add_subplot(g_spec[17:21, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_ve, 3)
    
    # root (d)
    ax_kpdve_d = fig.add_subplot(g_spec[21:25, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_d, 2)
    
    # mode (p)
    ax_kpdve_p = fig.add_subplot(g_spec[25:29, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_p, 1)

    # k
    ax_kpdve_k = fig.add_subplot(g_spec[29:33, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_k, 0)

    
    # kpdve spectrum -- in the end this is a nicer listener experience... more forgiving.
    # ax_kpdve_chr = fig.add_subplot(g_spec[19:30, :])
    # ax_kpdve_chr.axis('off')
    # subplot_kpdve(kpdve_analysis, ax_kpdve_chr)
     

    
    plt.subplots_adjust(0,0,1,1,0,0)
    for ax in fig.axes:
        ax.axis('off')
        ax.margins(0,0)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        
    plt.savefig(filename[:-4] + ".png", dpi=300, bbox_inches='tight', pad_inches=0, facecolor='black', transparent=False);

    # arr = plt.imread(filename[:-4] + ".png")
    # plt.imsave(filename[:-4], arr)
    
    plt.show()


def conventional_kpdve_saved_graph(kpdve_analysis, filename, showtitle=False):
    # PYPLOT
    fig = plt.figure(frameon=False)
    
    plt.style.use('dark_background')

    if(showtitle):
        plt.title(filename)

    g_spec = gridspec.GridSpec(nrows=4, ncols=1, figure=fig)
    g_spec.update(wspace=0, hspace=0)

    
    # ext_note (ve)
    ax_kpdve_ve = fig.add_subplot(g_spec[0, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_ve, 3)
    
    # root (d)
    ax_kpdve_d = fig.add_subplot(g_spec[1, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_d, 2)
    
    # mode (p)
    ax_kpdve_p = fig.add_subplot(g_spec[2, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_p, 1)

    # k
    ax_kpdve_k = fig.add_subplot(g_spec[3, :])
    subplot_kpd_param(kpdve_analysis, ax_kpdve_k, 0)

    
    # kpdve spectrum -- in the end this is a nicer listener experience... more forgiving.
    # ax_kpdve_chr = fig.add_subplot(g_spec[19:30, :])
    # ax_kpdve_chr.axis('off')
    # subplot_kpdve(kpdve_analysis, ax_kpdve_chr)
     

    
    plt.subplots_adjust(0,0,1,1,0,0)
    for ax in fig.axes:
        ax.axis('off')
        ax.margins(0,0)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        
    plt.savefig(filename + ".png", dpi=300, bbox_inches='tight', pad_inches=0, facecolor='black', transparent=False);

    # arr = plt.imread(filename[:-4] + ".png")
    # plt.imsave(filename[:-4], arr)
    
    plt.show()

# =============================================================================
# 3D subplots
# =============================================================================
        
def subplot_kpdve_space(kpdve_list, ax, ttl="KPDVE plot"):
    '''
    Make a 3D plot of a kpdve path. K P and D are dimensions. V and e are 
    locations within kpdcube

    Parameters
    ----------
    kpdve_list : np.array(n, 5)
        a list of kpdve analyses
    axis:
        axis in a matplotlib plot

    Returns
    -------
    None.


    '''

    setup_3d_axes(ax, ttl)
    plot_kpdve_list(ax, kpdve_list)
 
    # cbar.set_label("sequence")


def setup_3d_axes(ax, ttl):
    '''
    tilte and label and configure 3-d axes for a KPDVE subplot

    Parameters
    ----------
    ax : matplotlib axis
        a 3D subplot: K for x axis, P for y axis, D for z axis.
    ttl : string
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    ax.set_title(ttl)

    ax.set_xlabel('Key')
    ax.set_ylabel('Pattern')
    ax.set_zlabel('Degree')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.set_zlim(0, 6)


def plot_kpdve_list(ax, kpdve_list):
    c = np.zeros(kpdve_list.shape[0], dtype=float)

    for i, a_kpdve in enumerate(kpdve_list):
        c[i] = kpdve_colormap_value(a_kpdve) * 12.0  # colors * vertical axis

    x_vals = kpdve_list[:, 0] + (np.random.rand(kpdve_list.shape[0]) * 0.3, )
    y_vals = kpdve_list[:, 1] + (np.random.rand(kpdve_list.shape[0]) * 0.3, )
    z_vals = kpdve_list[:, 2] + (np.random.rand(kpdve_list.shape[0]) * 0.3, )

    # 0-4 -- for color, shape
    # important to get dynamism in the plotting     
    p = ax.scatter(x_vals,
                   y_vals,
                   z_vals,
                   s=3, c=c, cmap='hsv', alpha=1.0, vmin=0, vmax=12)


if __name__ == "__main__":
    import doctest
    doctest.testmod()