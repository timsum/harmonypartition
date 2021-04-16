import numpy as np
import harmony_state
import pt_utils
import pt_musicutils
import pt_naming_conventions

import matplotlib.pyplot as plt
import seaborn as sb

# ==============================================================================
# THE CURRENT STANDARD GRAPH
# This uses K, P, and D as long-term memory underneath a colored 'fifths-chroma' which shows the pitch entropy in a notation OR audio file.
# input is bin_a, kpdve_a
# ==============================================================================

hue = 0.27
sat = 1.0
light = 0.8

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
    


# ==============================================================================
# THE CURRENT STANDARD NOTEGROUP GRAPH
# This uses K, P, and D as long-term memory underneath a colored 'fifths-chroma' which shows the pitch entropy in a notation OR audio file.
# input is bin_a, kpdve_a
# ==============================================================================

    
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
    
    # if it's NOT chromatic (default) everything has to be reconfigured to be analyzed...
    # y_ticknames = []          *GUH*
    
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

def numpy_array_by_circleindex(np_array):
    return np.array([(arr_val * i)/12.0 for i, arr_val in enumerate(np_array)])

def numpy_matrix_by_circleindex(np_matrix):
    return np.array([numpy_array_by_circleindex(an_array) for an_array in np_matrix])


# straight KPDVE input

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