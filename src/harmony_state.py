#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 21:07:29 2020

@author: johntimothysummers
"""

import random
import numpy as np
import partita
import pt_utils
import pt_musicutils
import pt_naming_conventions
import pt_keypattern
import pt_analyzeaudio

#   IMPORTANT: IT MAY BE BEST IN THE END TO DIG ONE LEVEL DEEPER, AND HAVE THE WHOLE THING DEFINED BY THE BITWISE ENCODING
#   THIS WILL ALLOW ONE OF THE EXTRA BITS (CURRENTLY IT USES 28) TO ENCODE THE PENTATONIC/HEPTATONIC BASE.
#   PENTATONIC REMAINS INSUFFICIENTLY EXPLORED

class harmony_state():
    '''
    The core class for improvised performing in the kpdve|binary scheme
    '''

    def __init__(self, start_kpdve=np.array([0, 0, 0, 4, 3])):
        # KPDVE VAL & START (START DOES *NOT* CHANGE)
        self.start_kpdve = start_kpdve # THIS NEVER CHANGES -- IT MAY TURN OUT TO BE USEFUL FOR ORIENTING TOWARD A TONALITY... SEEKING 'HOME'

        # KPDVE (5-param Key, Pattern, Degree, Voicing, Extensions)
        self.current_kpdve = start_kpdve

        # BINARY (chromatic)
        self.current_binary = partita.chord_for_KPDVE_input(self.current_kpdve)

        # PREVIOUS VALUES -- THES REMAIN UNUSED...
        self.prev_kpdve = self.current_kpdve
        self.prev_binary = self.current_binary

        #FLAG INVALID STATE
        self.valid_state = True

        #CHROMA STATUS
        self.chroma_values = np.zeros((12,))

        self.rand_walk_steps = np.array([-1, 0, 1])


#   CORE FUNCTIONS: CHANGE BY KPDVE OR BINARY
    def change_kpdve(self, new_kdpve):
        '''
        change harmonic location and associated global vars

        Parameters
        ----------
        new_kdpve : np.array(5)
            the new harmonic context for the module.

        Returns
        -------
        None.

        '''

        if (np.array_equal(self.current_kpdve, new_kdpve)):
            return False
        
        self.current_kpdve = new_kdpve
        self.current_binary = partita.chord_for_KPDVE_input(self.current_kpdve)
        
        return True


    def change_notegroup(self, notegroup, v_opt=0):
        '''
        Generate the harmonic context from a binary notegroup

        Parameters
        ----------
        notegroup : int
            a chromatic pitch-class set.

        Returns
        -------
        True if changed, False if no change is NECESSARY

        '''

        # BIG QUESTION: SHOULD THIS STAY IN THE SAME CHORD IF THE or OPERATIONS ALLOWS?
        if (notegroup == self.current_binary):
            return False
        
        # if ((notegroup & self.current_binary) == notegroup): # NO CHANGE IN CHORD IS *NECESSARY*
        #     self.current_binary = notegroup
        #     return False

        probe_kpdve = partita.analyze_binary_input_for_closest_KPDVE(notegroup, self.current_kpdve)
        self.valid_state = (np.array_equal(probe_kpdve, pt_utils.MODVALS) == False)

        if self.valid_state:
            self.current_kpdve = np.copy(probe_kpdve)
            self.current_binary = notegroup
            ng_fifths = pt_utils.c_chrom_to_f_circle(self.current_binary)
            ng_kp = pt_keypattern.get_binary_KP(self.current_kpdve[0], self.current_kpdve[1])
            if (ng_fifths & ng_kp != ng_fifths):
                print("mismatch in fifths/kp")
            return True
            
        return False


    def change_from_midi(self, midi_list, v_opt=0):
        '''
        a simple wrapper of 'change_notegroup' which accepts a list of 0-127 numberd MIDI notes and reduces them to a single byte.

        pt_live_MIDI.py handles buffering and collection.
        '''
        notegroup = 0
        for midi_note in midi_list:
            notegroup |= pt_utils.LEFT_BIT >> (midi_note % 12)

        return self.change_notegroup(notegroup, v_opt=v_opt)
        

    def change_from_chroma(self, chroma_array, threshold=0.5, max_notes=None, v_opt=0):
        '''
        takes a 

        Parameters
        ----------
        chroma_array : np.array(1, 12)
            a chromatic pitch-class set, represented as floats 0-1
        threshold : float
            a lower threshold for strength of input
        max_notes : int
            limits chroma to the top N notes. (can be further culled by threshold)

        Returns
        -------
        True if changed, False if no change is NECESSARY
        '''
        # it is very possible that the previous KPDVE state has to alter a nearest-neighbor algorithm so that half-steps
        # around string notes don't 
        # create too much chaos  -- it makes sense that a key should build in a bias for its notes.

        if max_notes != None:
            # pick top N values
            top_n = chroma_array.argsort()[::-1][:max_notes]
            sparse_chroma = np.zeros((12,))
            for an_idx in top_n:
                sparse_chroma[an_idx] = chroma_array[an_idx]
            notegroup = pt_analyzeaudio.chroma_to_binary_value(sparse_chroma, threshold=threshold)
            self.chroma_values = np.copy(sparse_chroma)
        else:
            notegroup = pt_analyzeaudio.chroma_to_binary_value(chroma_array, threshold=threshold)
            self.chroma_values = np.copy(chroma_array)

        return self.change_notegroup(notegroup, v_opt=v_opt)


    # ACCESS EXTRAPOLATIONS.
    def current_chord_notes(self):
        return pt_utils.bit_locs(self.current_binary)
    
    def current_scale_notes(self):
        return pt_musicutils.scale_notes_for_KPDVE(self.current_kpdve)
    
    def ordered_chord_oct(self):
        return pt_musicutils.ordered_chord_notes_for_KPDVE(self.current_kpdve)
    
    def ordered_scale_oct(self):
        return pt_musicutils.ordered_scale_notes_for_KPDVE(self.current_kpdve)
    
    def ordered_chord_asc(self):
        return pt_musicutils.unfold_ascending(self.ordered_chord_oct())
    
    def ordered_scale_asc(self):
        return pt_musicutils.unfold_ascending(self.ordered_scale_oct())
    
    def current_root(self):
        return pt_utils.bit_locs(pt_musicutils.chrom_root_note_for_KPDVE(self.current_kpdve))[0]
    
    def current_conv_tonic(self):
        return pt_utils.bit_locs(pt_musicutils.chrom_conv_tonic_for_KPDVE(self.current_kpdve))[0]

    def current_minimal_rep(self):
        return pt_utils.minimal_bin_kpdve(self.current_binary, self.current_kpdve)

    def current_kpdve_list(self):
        return partita.analyze_binary_note_input(self.current_binary)

    
    # RAW CHORDS/MODES WITH A DISPLACEMENT, TO INTERACT WITH SCALE/KEY-BASED ENVIRONMENTS (e.g. FoxDot)
    # assumes chromatic basis
    def get_chord_disp_tuple(self):
        return pt_musicutils.get_chord_disp_tuple(self.current_kpdve)
    
    def get_mode_disp_tuple(self):
        return pt_musicutils.get_mode_disp_tuple(self.current_kpdve)
    
    def get_tonic_mode_disp_tuple(self):
        return pt_musicutils.get_tonic_mode_disp_tuple(self.current_kpdve)
    
    
    # FOR NAVIGATING WITHIN A SEVEN-TONE SCALE ENVIRONMENT
    # assumes seven=tone basis (kp established in scale)
    def current_chord_as_scale_degrees(self):
        chord = np.array([pt_keypattern.DVE_linear_eq(0, self.current_kpdve[3], i) for i in range(self.current_kpdve[4] + 1)])
        as_degree = (chord * self.current_kpdve[3]) % 7
        return (pt_musicutils.scale_conv_degree_for_KPDVE(self.current_kpdve) + np.array(as_degree)) % 7
    
    
    # string descriptions individual
    def current_hex_string(self):
        return "0x" + hex(self.current_minimal_rep())[2:].zfill(7)

    def current_notegroup_string(self):
        return "Ob" + bin(self.current_binary)[2:].zfill(12)

    def current_conv_tonic_string(self):
        return pt_naming_conventions.conv_tonic_name_for_kpdve(self.current_kpdve)
    
    def current_conv_pattern_string(self):
        return pt_naming_conventions.PATTERN_CONVENTIONAL_NAMES[self.current_kpdve[1]]
    
    def current_conv_mode_complete(self):
        return self.current_conv_tonic_string() + " " + self.current_conv_pattern_string()
    
    def current_root_string(self):
        return pt_naming_conventions.chord_root_name_for_KPDVE(self.current_kpdve)
    
    def current_function_string(self):
        return pt_naming_conventions.chord_function_in_key(self.current_kpdve)
    
    def current_chord_notes_string(self):
        return ' '.join(pt_naming_conventions.chord_note_names_for_KPDVE(self.current_kpdve))
    

    
    # --------------------------------------------------------------
    def string_description(self):
        '''
        returns string showing the current state in a terminal-friendly format.

        Parameters
        ----------
        None

        Returns
        -------
        String

        >>> kpdve_stream_string(np.array([0,0,0,4,2]), 0b110010000000)
        hex string:
        '0022c80 <--> 111111100000 : C Major (tonic) === 110010000000 : F as  IV'

        '''
        kpdve = self.current_kpdve
        core_kpdve = np.array([self.current_kpdve[0], 0, 0, 0, 0])
        notegroup = self.current_binary

        # the basic hex string
        hex_string = "compressed uniqueID: "
        hex_string += self.current_hex_string() + " \n"
        kpdve_string = np.array_str(self.current_kpdve) + " \n"
        bin_string = self.current_notegroup_string()
        # div
        div_string = "\n==-- derived meanings: --==\n"
        # mode
        mode_string = " (conventional) mode: " 
        tonicstring = pt_naming_conventions.conv_tonic_name_for_kpdve(kpdve)
        patternstring = pt_naming_conventions.PATTERN_CONVENTIONAL_NAMES[kpdve[1]] + " \n"
        mode_string += tonicstring + " " + patternstring
        
        # chord
        chord_string = "(conventional) chord: "
        chord_string += pt_naming_conventions.chord_root_name_for_KPDVE(kpdve) + " functioning as "  + pt_naming_conventions.chord_function_in_key(kpdve).ljust(4)  + "\n"
        
        # essential key
        lyd_string = " (non-entropic) base: "
        lyd_tonic_string = pt_naming_conventions.note_name_for_kpdve(core_kpdve)
        lyd_patternstring = pt_naming_conventions.MODE_NAMES[core_kpdve[1]] + " \n"
        lyd_string += lyd_tonic_string + " " + lyd_patternstring
        
        # chromatic patterns:
        chord_notes_name_string = ' '.join(pt_naming_conventions.chord_note_names_for_KPDVE(self.current_kpdve))
        chord_notes_string = "chord notes: " + np.array_str(self.current_chord_notes()) + " : " + chord_notes_name_string + " \n"
        
        scale_notes_name_string = ' '.join(pt_naming_conventions.scale_note_names_for_KPDVE(self.current_kpdve))
        scale_notes_string = "scale notes: " + np.array_str(self.current_scale_notes())  + " : " + scale_notes_name_string + " \n" 

        # in-mode patterns: 
        chord, cdisp = self.get_chord_disp_tuple()
        chord_raw_string = "   chord measured from root: " + np.array_str(chord) + " \n"
        cdisp_raw_string = " root: " + cdisp.astype(str)
        
        mode, mdisp = self.get_mode_disp_tuple()
        mode_raw_string = "    mode measured from chord root: " + np.array_str(mode) + " \n"
        mdisp_raw_string = " root : " + mdisp.astype(str)

        tonic_scale, tonic_scaledisp = self.get_tonic_mode_disp_tuple()
        tonic_scale_raw_string = "    tonic scale: " + np.array_str(tonic_scale)  + " \n"
        tonic_scaledisp_raw_string = " starting from: " + tonic_scaledisp.astype(str)   
        
        degrees_string = np.array_str(self.current_chord_as_scale_degrees())
        
        print(hex_string 
                + f"       kpdve values: {kpdve_string}" 
                + f"chromatic notegroup: {bin_string}" 
                + div_string + mode_string + chord_string + lyd_string  + "\n"
                + "== chromatic (12-note pitch-class) locations: \n" 
                + chord_notes_string + scale_notes_string + "\n"
                + "== modes and chords over roots (modal scales) \n"
                + chord_raw_string + cdisp_raw_string + " (" + chord_notes_name_string +")" + "\n"
                + mode_raw_string + mdisp_raw_string + " (" + scale_notes_name_string +")"  + "\n"
                + "displacement/mode *** for DAW settings: ***\n"
                + tonic_scale_raw_string + tonic_scaledisp_raw_string + "\n\n"
                + "== locations in 7-note system: " 
                + degrees_string
             )
  
    
    # ------------------------------------------------------------------
    # STANDARD MANIPULATIONS FOR NAVIGATING THE STATE THROUGH PARAMETERS
    # ------------------------------------------------------------------
    
    def param_increment(self, param_num, increment=-1):
        '''
        returns a unit kpdve to add or subtract to a given parameter.  Creates navigation possibilities through mapping

        Parameters
        ----------
        param_num : int
            which param to change (KPDVE).
        increment : int, optional
            how many steps to move in a given direction. The default is 1.

        Returns
        -------
        None

        >>> param_increment(2, increment=2)
        array([0, 0, 2, 0, 0])

        >>> param_increment(13)
        array([0, 0, 0, 1, 0])

        >>> param_increment(13)
        array([0, 0, 0, 1, 0])
        '''

        inc_kpdve = np.zeros(5, dtype=int)
        inc_kpdve[param_num % 5] = increment

        self.change_kpdve(pt_utils.kpdve_add(self.current_kpdve, inc_kpdve))

    def random_friendly_kpdve(self):
        a_kpdve = pt_utils.kpdve_random()
        a_kpdve[3] = 4
        a_kpdve[4] = 3

        self.change_kpdve(a_kpdve)

    def random_list_kpdve(self):
        self.change_kpdve(random.choice(partita.analyze_binary_note_input(self.current_binary)))

    def random_kpdve(self):
        self.change_kpdve(pt_utils.kpdve_random())

    def random_friendly_d(self):
        a_kpdve = self.current_kpdve.copy()
        a_kpdve[2] = (a_kpdve[2] + random.choice(self.rand_walk_steps))  % 7
        self.change_kpdve(a_kpdve)

    def random_friendly_p(self):
        a_kpdve = self.current_kpdve.copy()
        a_kpdve[1] = (a_kpdve[1] + random.choice(self.rand_walk_steps))  % pt_utils.MODVALS[1]    
        self.change_kpdve(a_kpdve)

    def resolve(self):
        a_kpdve = self.current_kpdve.copy()
        a_kpdve[2] = pt_utils.CONVENTION_DIST[a_kpdve[1]]
        self.change_kpdve(a_kpdve)

    def current_dominant(self):
        a_kpdve = self.current_kpdve.copy()
        a_kpdve[2] = (pt_utils.CONVENTION_DIST[a_kpdve[1]] + 1) % pt_utils.MODVALS[2]
        self.change_kpdve(a_kpdve)
        
    def current_two(self):
        a_kpdve = self.current_kpdve.copy()
        a_kpdve[2] = (pt_utils.CONVENTION_DIST[a_kpdve[1]] + 2) % pt_utils.MODVALS[2]
        self.change_kpdve(a_kpdve)

if __name__ == "__main__":
    h = harmony_state();
    h.string_description()
    print('=============')
    print('=RANDOMIZED==')
    print('=============')
    h.random_kpdve()
    h.string_description()

