#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 22:40:10 2020

@author: johntimothysummers
"""


import pyaudio
import sys
import numpy as np
import librosa
import matplotlib.pyplot as plt

import pt_analyzeaudio
import pt_naming_conventions
import pt_keypattern
import pt_utils
import harmony_state

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


def analyze_audio_in(buffer_size=2048, sr=44100):
    #init pyaudio
    p = pyaudio.PyAudio()

    #open stream
    buffer_size = buffer_size
    pyaudio_format = pyaudio.paFloat32
    stream = p.open(format=pyaudio_format,
                    channels=1,
                    rate=sr,
                    input=True,
                    output=True,
                    frames_per_buffer=buffer_size)
    

    # FFT - Chroma params:
    N_FFT = 4096
    HOP_LENGTH = 2048

    # Harmony State
    current_state = harmony_state.harmony_state()

    # fig = plt.figure(figsize=(12, 1))
    # ax = fig.add_subplot(111)
    # im = ax.imshow(np.random.rand())
    # plt.show(block=False)

    count = 0
    maxcount = 100

    while True:
        try:
            data = stream.read(buffer_size, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=float)
    
            # C = np.minimum(C,librosa.decompose.nn_filter(C,
            #                                               aggregate=np.mean,
            #                                               metric='cosine'))

            S = np.abs(librosa.stft(samples, n_fft=N_FFT))**2
            C = librosa.feature.chroma_stft(S=S, sr=sr, hop_length=HOP_LENGTH)
        
            C_mean = np.mean(C, axis=1)

            bin_num = pt_analyzeaudio.chroma_to_binary_value(C_mean, threshold=0.5)
            if current_state.change_notegroup(bin_num):
                ng_fifths = pt_utils.c_chrom_to_f_circle(current_state.current_binary)
                ng_kp = pt_keypattern.get_binary_KP(current_state.current_kpdve[0], current_state.current_kpdve[1])

                print("Ob" + bin(ng_fifths)[2:].zfill(12) + "    " +   current_state.current_root_string() + " as " + current_state.current_function_string() + "|| Ob" + bin(ng_kp)[2:].zfill(12) + " of " + current_state.current_conv_tonic_string() + " " + current_state.current_conv_pattern_string())


            if (count == maxcount):  
                #im.set_array(np.random.random(12, 1))
                # redraw the figure

                # fig.canvas.draw()
                # plt.cla()
                count = 0
            else:
                count = count + 1


            stream.write(data)
            
            
        except  KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("process killed")
            quit()


if __name__ == '__main__':
    analyze_audio_in()
