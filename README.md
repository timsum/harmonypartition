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



*harmonypartition* sets up a network of bits, in which a combination of binary filters and a
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

### partita outputs an encoding of harmonic context paired with a set of notes:
** a five-integer array (KPDVE) <==> (binary) a pitch-class set of a chord within a context **

In this system, harmony and melody become reciprocal types of information

The net result is to *combine one type of input with a derived version of the other*

* Within those bounds, there are three forms for this output:
    * 1) a list of integers encoded in the form below, which binds the two types of input in a single encoding.
        * RxxxKKKKPPPDDDVVVEEEC-D-EF-G-A-B
        * this form of output is most complete and compact for transfer, 
            explicitly pairing two different types of information (notes and 
            harmonic context). 
        * it ties together both context and chord in a 32-bit format (4 bits at left for special markings: TBD):
    * 2) an (n x 5) numpy array of KPDVE (chord context) values for a group of notes 
        (where the chord notes are known, but not the harmonic context)
        this provides all possible locations for a given chord, without choosing one as 'best'
            * a partita list has a max length 84 for a single note, but averages about 10-12 for multi-note input
                * The matter of which of these numbers constitutes the optimal solution is trivial in the case of KPDVE input -- always the same
                * List output from note intput requires analysis: the simplest system would simply measure the proximity to the previous result. 
                    This is currently calculated as pythagorean distance in modular space
    * 3) a group of notes represented in 12-bit form (0b101010110101)built from a 
        KPDVE value (where the context is known, but not the notes of the chord)
