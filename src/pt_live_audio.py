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

import pt_analyzeaudio
import pt_naming_conventions
import harmony_state

def analyze_audio_in(buffer_size=2048, sr=11025):
    #init pyaudio
    p = pyaudio.PyAudio()

    #open stream
    buffer_size = buffer_size
    pyaudio_format = pyaudio.paFloat32
    stream = p.open(format=pyaudio_format,
                    channels=1,
                    rate=11025,
                    input=True,
                    output=True,
                    frames_per_buffer=buffer_size)
    
    current_state = harmony_state.harmony_state()
    
    while True:
        try:
            data = stream.read(buffer_size, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=float)
    
            # IS THIS NORMALIZED? IS THAT A PROBLEM (IF SO, I THINK IT IS... investigate)
            C = librosa.feature.chroma_stft(y=samples, sr=11025, hop_length=2048)
            # C_f = np.minimum(C, librosa.decompose.nn_filter(C,
            #                                                 aggregate=np.median,
            #                                                 metric='cosine'))
            
            num = pt_analyzeaudio.chroma_to_binary_value(C)
            current_state.change_notegroup(num)
            

# =============================================================================
#             if count == 100:
# #                 pt_graphics_live.update_chroma_combo(C, graph_dict['ims'])
# #                 count = 0
#                 current_state.change_notegroup(bin_analysis) 
#                 pt_graphics_live.annotated_scroll(current_state)
#             count +=  1
# =============================================================================
            # send (C, C_f, current_state[...] ) and (axis, axis, axis...). graph_away!            

            stream.write(data)
            
            
        except  KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("process killed")
            quit()


if __name__ == '__main__':
    analyze_audio_in()
