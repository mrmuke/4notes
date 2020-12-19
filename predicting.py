from music21 import converter, instrument, note, chord
midi = converter.parse("data/mozart.mid")
notes = []

notes_to_parse = None

try: # file has instrument parts
    s2 = instrument.partitionByInstrument(midi)
    notes_to_parse = s2.parts[0].recurse() 
except: # file has notes in a flat structure
    notes_to_parse = midi.flat.notes
print(notes_to_parse)
for element in notes_to_parse:
    if isinstance(element, note.Note):
        notes.append(str(element.pitch))
    elif isinstance(element, chord.Chord):
        notes.append('.'.join(str(n) for n in element.normalOrder))
    print(element)
print(notes)

sequence_length = 100
pitchnames = sorted(set(item for item in notes))
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
network_input = []
network_output = []
for i in range(0, len(notes) - sequence_length, 1):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])
n_patterns = len(network_input)
# reshape the input into a format compatible with LSTM layers
network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
# normalize input
network_input = network_input / float(n_vocab)
network_output = np_utils.to_categorical(network_output)