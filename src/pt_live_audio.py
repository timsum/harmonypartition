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

from time import process_time

import pt_analyzeaudio
import pt_naming_conventions
import pt_keypattern
import pt_utils
import harmony_state

import pt_live_graph

# FFT - Chroma params:
N_FFT = 1024
HOP_LENGTH = 256

def analyze_audio_in(buffer_size=2048, sr=22050):
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

    # Harmony State
    current_state = harmony_state.harmony_state()
    graph_window = pt_live_graph.live_harmony_graph(current_state)

    while True:
        try:
            data = stream.read(buffer_size, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=float)
    
            # S = np.abs(librosa.stft(samples, n_fft=N_FFT))**2
            # C = librosa.feature.chroma_stft(S=S, sr=sr, hop_length=HOP_LENGTH)

            C = librosa.feature.chroma_cqt(y=samples, sr=sr)

            C = np.minimum(C, librosa.decompose.nn_filter(C, aggregate=np.mean, metric='cosine'))
            C_mean = np.mean(C, axis=1)

            # can I 'juice' the signal with tonality (resonance) here?

            if (current_state.change_from_chroma(C_mean, threshold=0.5, max_notes=5, v_opt=0)):
                show_terminal_output(current_state)
                graph_window.update_window_for_state()

            stream.write(data)
            
        except  KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("process killed")
            quit()

def show_terminal_output(current_state):
    ng_fifths = pt_utils.c_chrom_to_f_circle(current_state.current_binary)
    ng_kp = pt_keypattern.get_binary_KP(current_state.current_kpdve[0], current_state.current_kpdve[1])
    print("Ob" + bin(ng_fifths)[2:].zfill(12) + "    " +   current_state.current_root_string() + " as " + current_state.current_function_string())
    print("Ob" + bin(ng_kp)[2:].zfill(12) + " of " + current_state.current_conv_tonic_string() + " " + current_state.current_conv_pattern_string())



if __name__ == '__main__':
    analyze_audio_in()
