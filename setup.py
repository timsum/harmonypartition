# -*- coding: utf-8 -*-
"""

Seutp for partita package

"""

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='harmonypartition',
      version='0.0.1',
      author="Timothy Summers",
      author_email="timsummers.dev@gmail.com",
      description='Analyze harmonic content of binary data',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/timsum/harmonypartition",
      package_dir={'':'src'},
      #packages=setuptools.find_packages(),
      classifiers = ["Development Status :: 3 - Alpha",
                     "Framework :: Matplotlib",
                     "Intended Audience :: Education",
                     "Intended Audience :: Science/Research",
                     "Intended Audience :: End Users/Desktop",
                     "License :: OSI Approved :: MIT License",
                     "Programming Language :: Python :: 3.6",
                     "Topic :: Games/Entertainment",
                     "Topic :: Multimedia",
                     "Topic :: Multimedia :: Sound/Audio :: Analysis",
                     "Topic :: Multimedia :: Sound/Audio :: MIDI",
                     "Topic :: Scientific/Engineering :: Visualization"],
      py_modules=["harmony_state", "partita", "pt_datafiles", "pt_keypattern", "pt_kpdve_list_optimize", "pt_musicutils", "pt_naming_conventions", "pt_utils", "pt_standardgraph", "pt_wavewrite", "pt_harmonyfilters", "pt_analyzeaudio", "pt_analyzeMIDI", "pt_MIDI_live"],
)
