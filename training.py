from music21 import converter, instrument, note, chord
import numpy
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.callbacks import ModelCheckpoint
from keras.layers import BatchNormalization as BatchNorm
import os


#training the model
def train_model(model, network_input,network_output):
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"    
    #save weights so we don't have to wrorry about losing them
    checkpoint = ModelCheckpoint(
        filepath, monitor='loss', 
        verbose=0,        
        save_best_only=True,        
        mode='min' 
    )     
    callbacks_list = [checkpoint]      
    model.fit(network_input, network_output, epochs=200, batch_size=128, callbacks=callbacks_list)
 #get all notes from midi files - mozart bach beethoven chopin tchaikovsky

notes = []
for filename in os.listdir("data"):
    midi = converter.parse("data/"+filename) 
    print(filename)
    notes_to_parse = None
    #parsing notes from midi files
    try:
        s2 = instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts[0].recurse() 
    except:
        notes_to_parse = midi.flat.notes
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))


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

#create network and structure of it
#play around iwth number of each see if make better predictions
#number in parameter as number of nodes the layer should have 

model = Sequential()
model.add(LSTM(
    512,
    input_shape=(network_input.shape[1], network_input.shape[2]),
    recurrent_dropout=0.3,
    return_sequences=True
))
#LSTM can take sequence input and return sequence output

model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
model.add(LSTM(512))
model.add(BatchNorm())
#prevent overfitting (fraction of input nodes that should be dropped out)

model.add(Dropout(0.3))
model.add(Dense(256))
model.add(Activation('relu'))
#speed up
model.add(BatchNorm())
model.add(Dropout(0.3))
#Dense determines where the corresponding output node is to input node

model.add(Dense(len(set(notes))))
#determine the output of a node

model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
train_model(model,network_input,network_output)