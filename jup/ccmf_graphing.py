#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:47:41 2020

@author: timsummers
"""

import numpy as np
import librosa
import partita_librosa
import jupyter_daily_analysis
import pt_datafiles
import pt_graphics
import matplotlib.pyplot as plt
from matplotlib import gridspec as gridspec
import seaborn as sb
import os


def graph_ccmf_mp3_file(filename, key_orientation=np.array([0,0,0,4,3]), chroma_threshold=0.5, filter_chroma=True):
    y, sr, X, bin_a, kpdve_a, chroma_a, file_full_path = load_file_analyses_to_page(filename, key_orientation, chroma_threshold=chroma_threshold, filter_chroma=filter_chroma)
    graph_waveform_kpdve_combo(y, sr, file_full_path)
    return file_full_path


def load_file_analyses_to_page(filename, startkey, chroma_threshold=0.5, filter_chroma=True):
    
    # load file, analysis, and spectrogram data
    file_full_path = filename
    
    y, sr, chroma_a = partita_librosa.chroma_analyze_audiofile(file_full_path, 
                                                               hop_length=2048, 
                                                               filter_chroma=filter_chroma)

    X = librosa.stft(y)

    bin_a, kpdve_a = partita_librosa.analyze_chroma_list(chroma_a, 
                                                         threshold=chroma_threshold,
                                                         key_orientation=startkey)
    
    # save file versions so analysis doesn't go on forever... but this needs help from the pathlib
    trunc_filename = file_full_path[:-4]
    pt_datafiles.save_bin_kpd_file(trunc_filename, bin_a, kpdve_a)
        
    return y, sr, X, bin_a, kpdve_a, chroma_a, file_full_path



def graph_waveform_kpdve_combo(y, sr, path_filename):
    # PYPLOT
    # FIGSIZE IS HERE ADJUSTED TO BEST SHOW ON JUPYTER. NO FIGSIZE IS BEST FOR WEB
    fig = plt.figure(frameon=False, figsize=(12, 2))
#    fig = plt.figure(frameon=False)

    plt.style.use('dark_background')

    g_spec = gridspec.GridSpec(nrows=50, ncols=1, figure=fig)
    g_spec.update(wspace=0, hspace=0)


    ax_wave = fig.add_subplot(g_spec[:25, :])
    librosa.display.waveplot(y=y, sr=sr, x_axis=None)
    
    bin_a, kpdve_a = pt_datafiles.read_bin_kpd_file(path_filename[:-4])

    
    plt.subplots_adjust(0,0,1,1,0,0)
    for ax in fig.axes:
        ax.axis('off')
        ax.margins(0,0)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        
    ax_kpdve_ve = fig.add_subplot(g_spec[25:, :])
    graphable = pt_graphics.kpdve_list_to_heatmap_graphable(kpdve_a).T
    graphable = np.flip(graphable, axis=0)
    sb.heatmap(graphable,
               ax=ax_kpdve_ve,
               xticklabels=False,
               yticklabels=False, 
                      cmap='hsv', 
                      cbar=False, 
                      vmin=0)
        
    plt.savefig(path_filename[:-4] + ".png", dpi=300, bbox_inches='tight', pad_inches=0, facecolor='black', transparent=False);
    
    plt.show()

def analyze_and_graph_audio_folder(path, key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.5, filter_chroma=True, showtitle=False):
    '''
    Loop through the contents of a foder and generate analyses of its contents

    Parameters
    ----------
    path : string
        The path to a folder of audio files.

    Returns
    -------
    None.

    '''


    for paths, _, files in  os.walk(path):
        for a_file in files:
            if a_file[-5:] == "Store" or a_file[-4:] == ".png" or a_file[-4:] == ".npy":
                continue
            graph_ccmf_mp3_file(paths + a_file, key_orientation=key_orientation, chroma_threshold=chroma_threshold, filter_chroma=filter_chroma)


startkey = np.array([3,0,1,4,2])
audiopath = "/Users/timsummers/AnalysisLibraryAudio/"
cur_folder = audiopath + "beethoven/beethoven_12no1_FrauLev/"
analyze_and_graph_audio_folder(cur_folder, key_orientation=startkey, chroma_threshold=0.6, filter_chroma=True)

if __name__ == "__main__":
    import doctest
    doctest.testmod()