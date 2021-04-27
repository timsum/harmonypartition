import tkinter
from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import seaborn as sb

import numpy as np
from harmony_state import harmony_state

import pt_utils
import pt_keypattern
import pt_naming_conventions
import pt_standardgraph

hue = 0.27
sat = 1.0
light = 0.8

''' 
graphs a heatmap of : 
'''

class live_harmony_graph():

    def __init__(self, ref_state):
        self.current_state = ref_state

        self.window = tkinter.Tk()
        self.window.wm_title("Representations of Harmonic Process")

        self.fig, self.ax = plt.subplots(4, figsize=(12,3))

        self.chr_img = self.ax[0].imshow(np.expand_dims(self.current_state.chroma_values, axis=0), vmin=0.0, vmax=1.0)
        self.ng_img = self.ax[1].imshow(self.heatmap_axis(pt_utils.c_chrom_to_f_circle(self.current_state.current_binary)))
        self.kp_img = self.ax[2].imshow(self.heatmap_axis(pt_keypattern.get_binary_KP(self.current_state.current_kpdve[0], self.current_state.current_kpdve[1])))

        plt.show(block=False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)  # A tk.DrawingArea.
        self.canvas.draw()

        self.window.update()


    def update_window_for_state(self):
        self.chr_img.set_data(np.expand_dims(pt_utils.numpy_chrom_to_circle(self.current_state.chroma_values), axis=0))
        self.ng_img.set_data(self.heatmap_axis(pt_utils.c_chrom_to_f_circle(self.current_state.current_binary)))
        self.kp_img.set_data(self.heatmap_axis(pt_keypattern.get_binary_KP(self.current_state.current_kpdve[0], self.current_state.current_kpdve[1])))
        self.fig.canvas.flush_events()


    def heatmap_axis(self, notegroup):
        np_notes = pt_utils.binary_notegroup_to_numpy_array(notegroup)
        #mask = np.expand_dims(1- np_notes, axis=0)
        #colored = pt_standardgraph.numpy_array_by_circleindex(np_notes)
        expanded = np.expand_dims(np_notes, axis=0)
        
        return expanded
    


        # return sb.heatmap(expanded,
        #        ax=self.ax[axis_num],
        #        xticklabels=pt_naming_conventions.circle_fifth_notes(), 
        #        linewidths=1,
        #        cmap=sb.husl_palette(12, h=hue, l=light, s=sat),
        #        cbar=False, 
        #        mask=mask,
        #        vmin=0,
        #        vmax=1)


 

