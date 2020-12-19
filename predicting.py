from music21 import converter, instrument, note, chord
import numpy
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation

midi = converter.parse("data/mozart.mid")
notes = []

notes_to_parse = None

try:
    s2 = instrument.partitionByInstrument(midi)
    notes_to_parse = s2.parts[0].recurse() 
except:
    notes_to_parse = midi.flat.notes
print(notes_to_parse)
for element in notes_to_parse:
    if isinstance(element, note.Note):
        notes.append(str(element.pitch))
    elif isinstance(element, chord.Chord):
        notes.append('.'.join(str(n) for n in element.normalOrder))
print(notes)
#how many input notes to determine output (use dice and other method?)
sequence_length = 100
pitchnames = sorted(set(item for item in notes))
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
network_input = []
network_output = []
for i in range(0, len(notes) - sequence_length,1):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])
#for LSTM (can take sequence input and return sequence output)
network_input = numpy.reshape(network_input, (len(network_input), sequence_length, 1))
#normalize data
network_input = network_input / float(len(set(notes)))
network_output = np_utils.to_categorical(network_output)

#create network
model = Sequential()
model.add(LSTM(
    256,
    input_shape=(network_input.shape[1], network_input.shape[2]),
    return_sequences=True
))
#number in parameter as number of nodes 
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
#LSTM can take sequence input and return sequence output
model.add(LSTM(256))
model.add(Dense(256))
#prevent overfitting
model.add(Dropout(0.3))
model.add(Dense(n_vocab))
#determine the output of a node
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')