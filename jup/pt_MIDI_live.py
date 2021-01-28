from harmony_state  import harmony_state

# this module opens MIDI input can receive MIDI signals from... some port.  Which port?  Let's see.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 10:34:59 2020

@author: johntimothysummers
"""

import mido

from harmony_state import harmony_state
from collections import deque

import time

import numpy as np
import pt_utils


class midi_note_pitchclass_collector():
    pclass_count = np.zeros(12, dtype=int)
    current_notegroup = 0

    def add_note(self, midi_note):
        self.pclass_count[midi_note % 12] += 1
        self.current_notegroup = pt_utils.numpy_array_to_binary_notegroup(self.pclass_count)

    def remove_note(self, midi_note):
        if (self.pclass_count[midi_note % 12] > 0):
            self.pclass_count[midi_note % 12] -= 1
            self.current_notegroup = pt_utils.numpy_array_to_binary_notegroup(self.pclass_count)



def play_current_kpdve(outport, current_state):
    for e in current_state.current_kpdve_notes():
        simple_midi_note(outport, e)


def play_root(outport, current_state):
    simple_midi_note(outport, current_state.root_note(), 1)


def simple_midi_note(outport, note_num, channel=0):
    msg = mido.Message('note_on', note=note_num, channel=channel)
    #msg_off = mido.Message('note_off', note=note_num, channel=channel)
    outport.send(msg)
    #outport.send(msg_off)


def ask_in_out_ports():
    '''
    Get user in/out from list

    Parameters
    ----------
    def ask_in : None
        Prompts user.

    Returns
    -------
    inport, outport tuple

    '''
    ins = mido.get_input_names()
    max_ins = len(ins)-1
    print(ins)
    in_idx = input(f'choose input from list: (0...{max_ins}) ')
    in_idx = int(in_idx) % (max_ins + 1)
    inport = mido.open_input(ins[in_idx])

    outs = mido.get_output_names()
    max_outs = len(outs)-1
    print(outs)
    out_idx = input(f'choose output from list: (0...{max_outs}) ')
    out_idx = int(out_idx) % (max_outs + 1)
    outport = mido.open_output(outs[out_idx])

    return inport, outport


def analyze_midi_piano_input():
    inport, outport = ask_in_out_ports()

    p_classes = midi_note_pitchclass_collector()
    
    current_state = harmony_state()
    # graph_dict = pt_graphics_live.build_fig_axes(current_state)
    # pt_graphics_live.update_data_for_state(graph_dict)

    msglog = deque()
    
    while True:
        msg = inport.receive()
        if (msg.type == "note_on"):
            if msg.velocity > 0:
                p_classes.add_note(msg.note)
            else:
                p_classes.remove_note(msg.note)
                
            current_state.change_notegroup(p_classes.current_notegroup)
            # pt_graphics_live.update_data_for_state(graph_dict)

            msglog.append({"msg": msg, "due": time.time()})
               
        while len(msglog) > 0 and msglog[0]["due"] <= time.time():
            outport.send(msglog.popleft()["msg"])

        print(current_state.current_root_string() + " as " + current_state.current_function_string() + " of " + current_state.current_conv_tonic_string() + " " + current_state.current_conv_pattern_string())
        
        time.sleep(0.001)
        
analyze_midi_piano_input()