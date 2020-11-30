#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 23:04:49 2020

@author: johntimothysummers
"""

import music21
import numpy as np

import pt_utils
import pt_graphics
import harmony_state

# BARE=BONES integration with music 21

# =============================
def analyze_parsed_notation_file(parsedfile, key_orientation=np.array([0,0,0,4,2])):
    '''
    Analyze an xml file, and send back a tuple of bin_analysis, kpdve_analysis

    Parameters
    ----------
    filename : str
        the name of a file in the Music21 corpus.

    Returns
    -------
    bin_analysis, kpdve_analysis.
        (n, 1) array and (n, 5) array
    '''

    s = parsedfile.chordify()

    pitch_classes = []
    for a_chord in s.recurse().getElementsByClass('Chord'):
        # senthentically reduce to sixteenths (if necessary)
        sixteenths = int(a_chord.quarterLength // 0.25)
        for _ in range(sixteenths):
            pitch_classes.append([])
            for pc in a_chord.pitches:
                pitch_classes[-1].append(pc.midi % 12)

    bin_analysis = np.zeros(len(pitch_classes), dtype=int)
    for i, pc_array in enumerate(pitch_classes):
        bin_analysis[i] = pt_utils.binary_note_for_chord(pc_array)

    reader_state = harmony_state.harmony_state(start_kpdve=key_orientation)
    
    kpdve_chroma = []
    for ng in bin_analysis:
        reader_state.change_notegroup(ng)
        kpdve_chroma.append(reader_state.current_kpdve)

    return bin_analysis, np.array(kpdve_chroma)

def analyze_notation_file(filename, key_orientation=np.array([0,0,0,4,2])):
    parsedfile = music21.converter.parse(filename)
    bin_a, kpdve_a = analyze_parsed_notation_file(parsedfile, key_orientation)

    return bin_a, kpdve_a



    