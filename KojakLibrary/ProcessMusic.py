__author__ = 'cmgiler'

from music21 import converter, instrument, note, chord, midi
import numpy as np
import os
import time
import codecs, json

def load_midi(fn):
    'Load MIDI file using Music21 library'
    my_midi = converter.parse(fn)
    return my_midi

def create_grid(part):
    'Create Numpy array representing note grid for MIDI part'
    all_notes = []
    for element in part.recurse():
        try:
            if element.isChord:
                all_notes += [[p.pitch.midi, 
                               float(element.offset), 
                               float(element.quarterLength), 
                               p.volume.velocity] for p in element]
            elif element.isNote:
                all_notes.append([element.pitch.midi, 
                                  float(element.offset),
                                  float(element.quarterLength),
                                  element.volume.velocity])
        except:
            continue
            
    note_grid = np.zeros([128, int(max([x[1]*12+x[2]*12 for x in all_notes]))])

    for note in all_notes:
        note_grid[note[0], int(note[1]*12):int(note[1]*12+note[2]*12)] = note[3]
        
    return note_grid

def get_track_grids(my_midi):
    'Create dictionary of all track grids in MIDI file'
    parts = [p for p in my_midi.parts]
    track_grids = {}
    unnamed_counter = 1
    for i in range(len(parts)):
        part_name = parts[i].partName
        all_notes = create_grid(parts[i])

        note_grid = np.zeros([128, int(max([x[1]*12+x[2]*12 for x in all_notes]))])

        for note in all_notes:
            note_grid[note[0], int(note[1]*12):int(note[1]*12+note[2]*12)] = note[3]
        
        if not part_name:
            part_name = 'Unnamed ' + str(unnamed_counter)
            unnamed_counter += 1
            
        track_grids[part_name] = note_grid
    max_grid_length = max([len(x[0]) for x in track_grids.values()])
    for k, v in track_grids.items():
        num_rows = np.size(v, axis=1)
        if num_rows < max_grid_length:
            result = np.zeros([v.shape[0], max_grid_length])
            result[:v.shape[0], :v.shape[1]] = v
            v = result
            track_grids[k] = v
    return track_grids

def music_jsonify(midi_file):
    'Convert MIDI file to JSON file, for use in matching algorithm'
    print('Loading ' + midi_file)
    my_midi = load_midi('midi_files/'+midi_file)
    
    print('Creating Track Grids')
    cur_grid = get_track_grids(my_midi)
    cur_grid = {k: v.tolist() for k, v in cur_grid.items()}
    
    file_path = 'json_files/' + midi_file.lower().replace('.mid', '.json') ## your path variable
    
    song_key = my_midi.analyze('key')
    primary_key = song_key.tonic.pitchClass
    primary_mode = song_key.mode
    relative_key = song_key.relative.tonic.pitchClass
    relative_mode = song_key.relative.mode
    
    BPM_Array = [x[-1].getQuarterBPM() for x in my_midi.metronomeMarkBoundaries()]
    data_import = {'title': midi_file,
                    'instruments': cur_grid,
                    'starting_bpm': int(BPM_Array[0]),
                    'ending_bpm': int(BPM_Array[-1]),
                    'primary_key': primary_key,
                    'primary_mode': primary_mode,
                    'relative_key': relative_key,
                    'relative_mode': relative_mode}
    
    print('Dumping to JSON File (' + file_path + ')')
    json.dump(data_import, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    
def music_unjsonify(json_file):
    'Load json music grids'
    print('Loading ' + json_file)
    my_midi = json.load(codecs.open('json_files/' + json_file, 'r', encoding='utf-8'))
    my_midi['instruments'] = {k: np.array(v) for k, v in my_midi['instruments'].items()}
    return my_midi