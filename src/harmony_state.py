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



# this should be a subclass of a more efficient version -- starting with only
# the very basics

# class pt_min_chord_context_pair():
#     def __init__(self, bin_ng=0, bin_kpdve=0),:
#         self.current_binary = bin_ng
#         self.current_binary_kpdve = bin_kpdve

# class pt_chord_with_context(pt_min_chord_context_pair):
#     def __init__(self):
#         super().init()


class harmony_state():
    '''
    The core class for improvised performing in the kpdve|binary scheme
    '''


    def __init__(self, start_kpdve=np.array([0, 0, 0, 4, 2])):
        self.start_kpdve = start_kpdve
        self.current_kpdve = start_kpdve
        self.current_binary = partita.chord_for_KPDVE_input(self.current_kpdve)
        self.current_kpdve_list = partita.analyze_binary_note_input(self.current_binary)
        self.current_chord_notes = pt_utils.bit_locs(self.current_binary)
    
        self.prev_kpdve = self.current_kpdve
        self.prev_binary = self.current_binary
    
        self.current_kpdve_scale = np.array([0, 0, 0, 2, 6])
        self.current_binary_scale = partita.chord_for_KPDVE_input(self.current_kpdve_scale)
    
        self.scale_notes = pt_utils.bit_locs(self.current_binary_scale)
        self.next_oct = self.scale_notes + 12
    
        self.current_scale_notes = np.append(self.scale_notes, self.next_oct)
        self.current_scale_note_choice = 0
    
        self.rand_walk_steps = np.array([-1, 0, 1])


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

        #   this can be moved to a sublclass, as can everything below...
        # self.build_context()
        
        return True


    def change_notegroup(self, notegroup):
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
        self.current_kpdve_list = partita.analyze_binary_note_input(notegroup)

        #   this can be moved to a sublclass, as can everything below...
        # self.build_context()
        
        return True

# everything below can be in a subclass of the above == or better, its own class or file.
# it shouldn't change as often as the fundamental integer values
        # these extensions suited for purposes of
        # 1: game navigation
        # 2: midi playing.
    
        # they probably belong in a 'harmony world' file // project // structure...
    def build_context(self):
        self.current_chord_notes = pt_utils.bit_locs(self.current_binary)
        self.current_kpdve_scale = self.current_kpdve.copy()
        self.current_kpdve_scale[3] = 1
        self.current_kpdve_scale[4] = 6
        self.current_binary_scale = partita.chord_for_KPDVE_input(self.current_kpdve_scale)

        self.scale_notes = pt_utils.bit_locs(self.current_binary_scale)
        next_oct = self.scale_notes + 12
        self.current_scale_notes = np.append(self.scale_notes, next_oct)

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


    # access to useful note vals in a range...
    # STANDARD MANIPULATIONS FOR NAVIGATING THE STATE AS A PLAYER...
        
    def param_increment(self, param_num, increment=1):
        '''
        returns a unit kpdve to add or subtract to a given

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
        
    def random_note_in_key(self):
        return 60 + random.choice(self.current_scale_notes)

    def random_walk_in_key(self):
        to_add = random.choice(self.rand_walk_steps)
        self.current_scale_note_choice = self.current_scale_note_choice + to_add

        if self.current_scale_note_choice >= 14:
            self.current_scale_note_choice -= 2
        elif self.current_scale_note_choice < 0:
            self.current_scale_note_choice += 2

        return (60 + self.current_scale_notes[self.current_scale_note_choice])

    def random_note_in_chord(self):
        return (60 + random.choice(self.current_chord_notes))

    def current_kpdve_notes(self):
        notegroup = partita.chord_for_KPDVE_input(self.current_kpdve)
        npnotes = np.array(pt_utils.bit_locs(notegroup))
        return npnotes + 48

    def root_note(self):
        root = pt_utils.bit_locs(pt_musicutils.chrom_root_note_for_KPDVE(self.current_kpdve))[0]
        return 36 + root

    # access to convenient KPDVE 
    def random_friendly_kpdve(self):
        a_kpdve = pt_utils.kpdve_random()
        a_kpdve[3] = 4
        a_kpdve[4] = 2

        self.change_kpdve(a_kpdve)

    def random_list_kpdve(self):
        self.change_kpdve(random.choice(partita.analyze_binary_note_input()))

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