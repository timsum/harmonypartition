# harmonypartition
 *harmonypartition* is a system for the analysis and generation of musical harmony
 Developed by [Timothy Summers](http://www.timsummers.org)

In this system, musical modes function as latent spaces into which single notes can be given clearly definable roles and weights. 

This 'dynamic tokenization' is made possible by treating musical harmony as a more or less 'natural' consequence of mixing binary and ternary computing.

---

*harmonypartition* relies almost entirely on logic operations and runs with an efficiency equal 
to the task of parsing live audio. This Python/Numpy implementation also allows for integration with many powerful libraries, especially Librosa, Music21, and TensorFlow/Keras.

The underlying system allows entwines  ideas of melody and harmony:

* a harmony is an audible path to a single note
* a melody note is the consequence of a harmonic path.



*harmonypartition* sets up a network of bits in which a combination of binary filters and a
trivial backpropagation provide a wealth of actionable musical information.

The system is modeled on the practise modal improvisation, and is intended to promote the practise of tonal improvisation both on digital and analog devices. 

The correspondence to many conventions of Western harmonic practise is strong, but there is infinite room for extension and variation. 

---
# I/O

## INPUT

## Partita handles two fundamental types of input.
1) **integer:** groups of notes as a binary pitch-class set (0b100010010001)
2) **integer array:** a harmonic context (KPDVE): np.array([0, 0, 0, 4, 3])
   
*(NB: for transfer, these can be combined into a single 28-bit integer, e.g.: 0x00238c4)*

* **binary pitch class set input (int)**
    * note input can take the following forms:
        *   a 12-note pitch class set reduced to a single 12-bit integer, e.g.: 0b100010010000 as a C Major triad
            * the order of the input is C -> B (matching MIDI standard with lowest note zero as C)
                * Example 1: 0b100010010000 is ANY C major 5 chord, octave-reduced
                * Example 2: 0b101010000001 is ANY C major 9 chord (without 5), octave-reduced
        * a midi note or group of midi notes (0-128)
            * a group of midi notes reduces to binary form for analysis
        * a chroma analysis can be quickly reduced to this form, allowing for audio analysis.
        
* **context type input -- an array of 5 integers** 
    * parameters are as follows:
        *  K   "Key" (0-11) in the circle of fifths 
        *  P   "Pattern" (0-7) as a distortion of a central key (relative 
                minor, harmonic minor, harmonic major)
        *  D   "Degree" (0-7) as the distance of a chord from the Tonic chord
        *  V   "Voicing" (0-7) as the regular interval ('stride') between notes in a group
        *  E   "Extensions" (0-7) as the distance in notes from 
                the root of a chord to the furthest (measured in increments of voicing "V")
    * chord type input can take the following forms:
        * A 16-bit integer encoding 5 digits (KKKKPPPDDDVVVEEE)
        * a python list (or numpy array) of 5 integers

---
## OUTPUT

### *partita.py* calculates a harmonic context paired with a set of notes:
**context: np.array([K,P,D,V,E]) <==> audible notes: (integer)**

In this system, harmony and melody become reciprocal types of information

The net result of the analysis is to *combine each type of input with a derived version of the other*

* Within those bounds, there are three forms for this output:
    * 1) KPDVE/binary :: a list of integers encoded in the form below, which binds the two types of input in a single encoding.
        * 0b----KKKKPPPDDDVVVEEEC-D-EF-G-A-B
        * 4 bits at left for special markings: TBD
    * 2) an (n, 5) numpy array of KPDVE (context) values which serve as possible context for a group of notes 
        * a kpdve_list has a max length n = 84 for a single note, but is usually length 10 or so three- or four-note input
        * kpdve_list output from note intput requires analysis: the simplest system measures the proximity to the previous result. 
        * best fit is currently calculated as pythagorean distance in a modular space (harmony voxel) (pt_kpdve_list_optimize.py)
    * 3) a group of notes represented in 12-bit form (0b101010110101)built from a KPDVE value (where the context is known, but not the notes of the chord)

---
## STATE: The harmony_state Class

### The central mechanism for handling input and output is the harmony_state. 

The harmony state can be changed with groups of notes given as:

1) a 12-bit integer in chromatic-tone order, e.g. 0b100010010001 for a C Major 7 chord
   + these can be derived from Librosa *chroma*, and might possibly be extended to include *any* result of a Fourier transform... 
2) a list of midi notes, e.g. [60, 64, 67, 71] for a C Major 7 chord
   
The harmony state can change its output and context through a five-parameter system:
1) a numpy array of length 5, eg. np.array([0,0,1,4,3]) for a C Major 7 chord
2) direct access to current_tonic(), current_dominant(), etc. 
3) filters may be applied (e.g. 'negativize()) to change the harmonic space according to familiar patterns.

Every harmony_state can be mined for at least the following information (available through string_description() function):

```
compressed uniqueID: 0x00238c4 
       kpdve values: [0 0 0 4 3] 
chromatic notegroup: 0b100011000100
==-- derived meanings: --==
 (conventional) mode: C Major (tonic) 
(conventional) chord: F functioning as IV  
 (non-entropic) base: F Lydian 

== chromatic (12-note pitch-class) locations: 
chord notes: [0 4 5 9] : F A C E 
scale notes: [ 0  2  4  5  7  9 11] : F G A B C D E 

== modes and chords over roots (modal scales) 
   chord measured from root: [ 0  4  7 11] 
 root: 5 (F A C E)
    mode measured from chord root: [ 0  2  4  6  7  9 11] 
 root : 5 (F G A B C D E)
displacement/mode *** for DAW settings: ***
    tonic scale: [ 0  2  4  5  7  9 11] 
 starting from: 0

== locations in 7-note system: [3 5 0 2]
```

# USE

---
## Analyzing Audio Files
- Librosa
- Magenta Onsets and Frames (?)
(instructions coming soon)

---
## Analyzing MIDI Files
- Music21
(instructions coming soon)

---
## Analyzing Live MIDI
- Mido
(instructions coming soon)

---
## Analyzing Live Audio
- Pyaudio
(instructions coming soon)


