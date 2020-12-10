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

class harmony_state():
    '''
    The core class for improvised performing in the kpdve|binary scheme
    '''

    def __init__(self, start_kpdve=np.array([0, 0, 0, 4, 3])):
        # KPDVE VAL & START (START DOES *NOT* CHANGE)
        self.start_kpdve = start_kpdve
        self.current_kpdve = start_kpdve

        # BINARY (chromatic)
        self.current_binary = partita.chord_for_KPDVE_input(self.current_kpdve)

        # KPDVE LIST
        self.current_kpdve_list = partita.analyze_binary_note_input(self.current_binary)

        # PREVIOUS VALUES
        self.prev_kpdve = self.current_kpdve
        self.prev_binary = self.current_binary

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
        self.current_kpdve_list = partita.analyze_binary_note_input(self.current_binary)
        
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
        
        if ((notegroup & self.current_binary) == notegroup): # NO CHANGE IN CHORD IS *NECESSARY*
            self.current_binary = notegroup
            return False

        self.current_kpdve = partita.analyze_binary_input_for_closest_KPDVE(notegroup, self.current_kpdve)
        self.current_binary = notegroup
        self.current_kpdve_list = partita.analyze_binary_note_input(notegroup, v_opt=v_opt)
        
        return True

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
        chord = [pt_keypattern.DVE_linear_eq((self.current_kpdve[2], self.current_kpdve[3], i) for i in range(self.current_kpdve[4] + 1))]
        chord = (chord * kpdve[3]) % 7
        return np.array(chord)
    
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
        '''
        return pt_naming_conventions.kpdve_stream_string(self.current_kpdve, self.current_binary)
    
    # --------------------------------------------------------------
    # STANDARD MANIPULATIONS FOR NAVIGATING THE STATE AS A PLAYER...        
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

