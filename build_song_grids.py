__author__ = 'cmgiler'

from music21 import converter, instrument, note, chord, midi
import numpy as np
import os
import pickle
from KojakLibrary import ProcessMusic as KJPM

file_dir = 'midi_files/'
files = os.listdir(file_dir)
for i, fn in enumerate(files):
    if fn.lower().endswith('.mid'):
        print('On "' + fn + '"')
        print('Working on it...')
        KJPM.music_jsonify(fn)
