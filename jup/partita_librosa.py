
# create a graphic analyis.  See what happens when it is analyzed

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.facecolor' : 'black',
                     'figure.facecolor' : 'black',
                     'savefig.facecolor' : 'black'
                     })

from matplotlib import cm
from matplotlib import gridspec as gridspec

import librosa
import librosa.display

import partita
import pt_utils
import pt_graphics
import harmony_state
import pt_datafiles

import os

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
            notegroup |= partita.pt_utils.LEFT_BIT >> count
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
    
# 1B GET ANALYZABLE FORM TO KPDVE-BIN
def kpdve_analyze_audiofile(filename, hop_length=1024, key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.7, filter_chroma=True):
    '''
    

    Parameters
    ----------
    filename : an audio file 
        file must be of Librosa accepted type.
    hop_length : int, optional
        fourier transform hop. The default is 1024.
    key_orientation : ndarray(5), a valid KPDVE location, optional
        for starting the analysis, a location indicating key. The default is np.array([0,0,0,4,2]).
    chroma_threshold : float, optional
        minimum value for strength of a pitch in the pitch-class set analysis. The default is 0.7.
    filter_chroma : bool, optional
        do k-neighbor filtering in librosa. The default is True.

    Returns
    -------
    tuple: bin_analysis, kpdve_analysis (ndarray(n, 1), ndarray(n, 5))
    '''
    
    y, sr, chroma_a = chroma_analyze_audiofile(filename, 
                                               hop_length=hop_length, 
                                               filter_chroma=filter_chroma)

# ======== ANALYSIS (returns tuple==========
    bin_analysis, kpdve_analysis = analyze_chroma_list(chroma_a, 
                                                       threshold=chroma_threshold, 
                                                       key_orientation=key_orientation)
    
    return bin_analysis, kpdve_analysis

# =============================    
# STEP 1 -> AUDIO TO KPDVE-BIN FILE
def analyze_audiofile_to_datafile(filename, hop_length=1024, key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.7, filter_chroma=True):
    '''
    
    Parameters
    ----------
    filename : an audio file 
        file must be of Librosa accepted type.
    hop_length : int, optional
        fourier transform hop. The default is 1024.
    key_orientation : ndarray(5), a valid KPDVE location, optional
        for starting the analysis, a location indicating key. The default is np.array([0,0,0,4,2]).
    chroma_threshold : float, optional
        minimum value for strength of a pitch in the pitch-class set analysis. The default is 0.7.
    filter_chroma : bool, optional
        do k-neighbor filtering in librosa. The default is True.

    Returns
    -------
    relevant data: binary array, kpdve array, y, sr, chroma
        . writes binary and kpdve data to .npy file next to the audio file.
    '''
    
    trunc_filename = filename[:-4]
    bin_a, kpdve_a = kpdve_analyze_audiofile(filename,
                                             hop_length=hop_length,
                                             key_orientation=key_orientation,
                                             chroma_threshold=chroma_threshold, 
                                             filter_chroma=filter_chroma)
    
    pt_datafiles.save_bin_kpd_file(trunc_filename, bin_a, kpdve_a)
    


# =============================    
# STEP 2 -> KPDVE-BIN FILE TO GRAPH
def graph_kdpve_analysis_file(filename):
    bin_a, kpdve_a = pt_datafiles.read_bin_kpd_file(filename)
    pt_graphics.conventional_kpdve_saved_graph(kpdve_a, filename, showtitle=True)

# =============================
# =============================
# OLD METHODS, SYSTEMATIZED ABOVE... SOON-TO-BE-DEPRECATED.
# =============================
# =============================
    
def analyze_audio_for_graphing(filename, hop_length=1024, key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.7, filter_chroma=True):
    '''
    Get grahing relevant info from an audio file:
        y, sr, chroma_switched, bin_analysis, kpdve_analysis

    Parameters
    ----------
    filename : gt
        an audio file

    Returns
    -------
     y, sr, chroma_switched, bin_analysis, kpdve_analysis.

    '''
    y, sr, chroma_a = chroma_analyze_audiofile(filename, 
                                               hop_length=1024, 
                                               filter_chroma=filter_chroma)

    bin_analysis, kpdve_analysis = analyze_chroma_list(chroma_a, 
                                                       threshold=chroma_threshold, 
                                                       key_orientation=key_orientation)

    
    chr_binary = chroma_a > chroma_threshold
    # THIS IS A LOVELY VISUALIZATION, BUT NOT SO USEFUL HERE...
    # generate a model with switched pitch parameters, for visual tracking
    chr_switched = np.zeros(chroma_a.shape)
    
    for i in range(12):
        chr_switched[i] = chr_binary[(i * 7) % 12] # +1 gets f to the bottom..
    
    return y, sr, chr_switched, bin_analysis, kpdve_analysis


def analyze_and_graph_audio(filename,key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.5):
    '''
    given the name of an mp3 file, load it and perform a KPDVE analysis

    Parameters
    ----------
    filename : string
        the name of an mp3 file

    Returns
    -------
    None
        plots an analysis:
            1) spectrum analysis
            2) switched chroma
            3) KPDVE linar analysis
            5) kpdve 3-space

    '''
    # load audio
    y, sr, chr_switched, bin_analysis, kpdve_analysis = analyze_audio_for_graphing(filename, key_orientation=key_orientation, chroma_threshold=chroma_threshold)

    # PYPLOT
    fig = plt.figure(constrained_layout=True)
    g_spec = gridspec.GridSpec(nrows=9, ncols=1, figure=fig)
    g_spec.update(wspace=0.01, hspace=0.01)

    # waveform
    ax_wave = fig.add_subplot(g_spec[0,:])
    pt_graphics.subplot_analyzed_waveform(y, sr, kpdve_analysis, ax_wave)

    # frequency
    ax_freq = fig.add_subplot(g_spec[1,:])
    pt_graphics.subplot_spectrum(y, sr, ax_freq)

    # binary values
    ax_switch = fig.add_subplot(g_spec[2,:])
    pt_graphics.subplot_chroma(chr_switched, ax_switch)

    # k

    ax_kpdve_k = fig.add_subplot(g_spec[3, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_k, 0)

    # p

    ax_kpdve_p = fig.add_subplot(g_spec[4, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_p, 1)
    

    # d

    ax_kpdve_d = fig.add_subplot(g_spec[5, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_d, 2)


    # d functions

    ax_kpdve_d_func = fig.add_subplot(g_spec[6, :])
    pt_graphics.subplot_d_functions(kpdve_analysis, ax_kpdve_d_func)

    # kpdve spectrum
    ax_kpdve_chr = fig.add_subplot(g_spec[7:9, :])
    pt_graphics.subplot_kpdve(kpdve_analysis, ax_kpdve_chr)
    

    # plt.xlabel('SAMPLES')
    plt.suptitle(filename, fontsize=15)
    
    # ax_kpdve_chr3d = fig.add_subplot(g_spec[7:, :], projection='3d')
    # pt_graphics.subplot_kpdve_space(kpdve_analysis, ax_kpdve_chr3d)
    
    plt.show()


def analyze_and_graph_audio_for_nav(filename, title=None, key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.5):
    '''
    given the name of an mp3 file, load it and perform a KPDVE analysis
    format to be used as pagesized button for web navigation of audio.

    Parameters
    ----------
    filename : string
        the name of an mp3 file

    Returns
    -------
    None
        plots an analysis:


    '''
    # load audio
    y, sr, chr_switched, bin_analysis, kpdve_analysis = analyze_audio_for_graphing(filename, key_orientation=key_orientation, chroma_threshold=chroma_threshold)

    # PYPLOT
    fig = plt.figure(constrained_layout=True)
    g_spec = gridspec.GridSpec(nrows=6, ncols=1, figure=fig)
    g_spec.update(wspace=0.01, hspace=0.01)

    # waveform
    ax_wave = fig.add_subplot(g_spec[0,:])
    pt_graphics.subplot_analyzed_waveform(y, sr, kpdve_analysis, ax_wave)

    # k
    ax_kpdve_k = fig.add_subplot(g_spec[1, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_k, 0)

    # mode (p)
    ax_kpdve_p = fig.add_subplot(g_spec[2, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_p, 1)

    # root (d)
    ax_kpdve_d = fig.add_subplot(g_spec[3, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_d, 2)

    # ext_note (ve)
    ax_kpdve_ve = fig.add_subplot(g_spec[4, :])
    pt_graphics.subplot_kpd_param(kpdve_analysis, ax_kpdve_ve, 3)

    # kpdve spectrum
    ax_kpdve_chr = fig.add_subplot(g_spec[5, :])
    pt_graphics.subplot_kpdve(kpdve_analysis, ax_kpdve_chr)
    
    plt.suptitle(title, fontsize=15)
    
    plt.show()


def analyze_and_graph_audio_for_ccmf_player(filename, 
                                            title=None, 
                                            key_orientation=np.array([0,0,0,4,2]), 
                                            chroma_threshold=0.5, 
                                            filter_chroma=True,
                                            showtitle=False):
    '''
    given the name of an mp3 file, load it and perform a KPDVE analysis
    format to show waveform and analysis next to each other.

    Parameters
    ----------
    filename : string
        the name of an mp3 file

    Returns
    -------
    None
        plots an analysis:


    '''
    if filename[-5:] == "Store" or filename[-4:] == ".png" or filename[-4:] == ".npy":
        return
    
    # load audio
    y, sr, chr_switched, bin_analysis, kpdve_analysis = analyze_audio_for_graphing(filename, 
                                                                                   key_orientation=key_orientation, 
                                                                                   chroma_threshold=chroma_threshold,
                                                                                   filter_chroma=filter_chroma)
    pt_graphics.ccmf_waveform_kpdve_graph(y, sr, kpdve_analysis, filename, showtitle=False)


def analyze_audio_folder_to_datafiles(path, key_orientation=np.array([0,0,0,4,2]), chroma_threshold=0.5, filter_chroma=True):
    '''
    Loop through the contents of a foder and generate analyses of its contents

    Parameters
    ----------
    path : string
        The path to a folder of audio files.

    Returns
    -------
    None.
        generates .npy files next to audio files
    '''

    for paths, _, files in  os.walk(path):
        for a_file in files:
            if a_file[-5:] == "Store" or a_file[-4:] == ".png" or a_file[-4:] == ".npy":
                continue
            analyze_audiofile_to_datafile(paths + a_file, 
                                          key_orientation=key_orientation, 
                                          chroma_threshold=chroma_threshold,
                                          filter_chroma=filter_chroma)


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
            analyze_and_graph_audio_for_ccmf_player(paths + a_file, 
                                                    title=a_file, 
                                                    key_orientation=key_orientation, 
                                                    chroma_threshold=chroma_threshold, 
                                                    filter_chroma=filter_chroma,
                                                    showtitle=showtitle)


#=============================================================================
# audiopath = "audio/" # default audio path

# currentfile = "D_759_ii_Franz_Schubert_Herbert_von_Karajan_1957.mp3"
# startkey = np.array([4,0,1,4,2])
#=============================================================================

#=============================================================================
# analyze_and_graph_audio_folder(audiopath, 
#                                 key_orientation=np.array([0,0,0,4,2]), 
#                                 chroma_threshold=0.6,
#                                 filter_chroma=False)
# #=============================================================================
# analyze_audio_folder_to_datafiles(audiopath, 
#                                   key_orientation=np.array([0,0,0,4,2]), 
#                                   chroma_threshold=0.5, 
#                                   filter_chroma=True)
#=============================================================================
# analyze_audiofile_to_datafile(audiopath + currentfile,
#                               key_orientation=startkey, 
#                               chroma_threshold=0.5,
#                               filter_chroma=True)
# graph_kdpve_analysis_file(audiopath + currentfile[:-4])
#=============================================================================

