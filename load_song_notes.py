from music21 import *
import pickle
import os
from KojakLibrary import ProcessMusic as KJPM

try:
    with open('song_notes.pkl', 'rb') as pkl:
        song_notes = pickle.load(pkl)
except:
    song_notes = {}

try:
    dir_contents = os.listdir('midi_files/')
    for i, file in enumerate(dir_contents):
        print('%d/%d' % (i+1, len(dir_contents)))
        if file.lower().endswith('.mid') and file not in song_notes.keys():
            print('Loading File: %s' % file)
            midi_data = KJPM.load_midi('midi_files/' + file)
            parts = [p for p in midi_data.parts]
            notes_list = {}
            unnamed_counter = 1
            for part in parts:
                part_name = part.partName
                if not part_name:
                    part_name = 'Unnamed ' + str(unnamed_counter)
                    unnamed_counter += 1
                notes_list[part_name] = [element for element in part.recurse()]
            song_notes[file] = notes_list
        else:
            print('File already in dictionary: %s' % file)
    with open('song_notes.pkl', 'wb') as pkl:
        pickle.dump(song_notes, pkl)
except:
    print('Writing to Pickle')
    with open('song_notes.pkl', 'wb') as pkl:
        pickle.dump(song_notes, pkl)
