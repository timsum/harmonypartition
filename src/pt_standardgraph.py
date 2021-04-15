import numpy as np
import pt_utils
import pt_musicutils

import matplotlib.pyplot as plt
import seaborn as sb

# ==============================================================================
# THE CURRENT STANDARD GRAPH
# This uses K, P, and D as long-term memory underneath a colored 'fifths-chroma' which shows the pitch entropy in a notation OR audio file.
# input is bin_a, kpdve_a
# ==============================================================================

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