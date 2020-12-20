import math
import numpy
import pyaudio
import itertools
from scipy import interpolate
from operator import itemgetter
import random
from pydub import AudioSegment
import itertools
import click
from ga import generate_genome, Genome, selection_pair,single_point_crossover, mutation
from typing import List, Dict

class Note:

  NOTES = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

  def __init__(self, note, octave=4):
    self.octave = octave
    if isinstance(note, int):
      self.index = note
      self.note = Note.NOTES[note]
    elif isinstance(note, str):
      self.note = note.strip().lower()
      self.index = Note.NOTES.index(self.note)

  def transpose(self, halfsteps):
    octave_delta, note = divmod(self.index + halfsteps, 12)
    return Note(note, self.octave + octave_delta)

  def frequency(self):
    base_frequency = 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)
    return base_frequency * (2.0 ** self.octave)

  def __float__(self):
    return self.frequency()


def sine(frequency, length, rate):
  length = int(length * rate)
  factor = float(frequency) * (math.pi * 2) / rate
  return numpy.sin(numpy.arange(length) * factor)

def shape(data, points, kind='slinear'):
    items = points.items()
    sorted(items,key=itemgetter(0))
    keys = list(map(itemgetter(0), items))
    vals = list(map(itemgetter(1), items))
    interp = interpolate.interp1d(keys, vals, kind=kind)
    factor = 1.0 / len(data)
    shape = interp(numpy.arange(len(data)) * factor)
    return data * shape 
 
def harmonics1(freq, length): 
  a = sine(freq * 1.00, length, 44100)
  b = sine(freq * 2.00, length, 44100) * 0.5
  c = sine(freq * 4.00, length, 44100) * 0.125
  return (a + b + c) * 0.2

def harmonics2(freq, length):
  a = sine(freq * 1.00, length, 44100)
  b = sine(freq * 2.00, length, 44100) * 0.5
  return (a + b) * 0.2

def pluck1(note,length):
  chunk = harmonics1(note.frequency(), length)
  return shape(chunk, {0.0: 1, 1.0:0.1})

def pluck2(note):
  chunk = harmonics2(note.frequency(), 1)
  return shape(chunk, {0.0: 0.0, 0.5:0.75, 0.8:0.4, 1.0:0.1})

def majorChord(note,length):
  third = note.transpose(4)
  fifth = third.transpose(3)
  return pluck1(note,length) + pluck1(third,length) + pluck1(fifth,length)

def minorChord(note):
  third = note.transpose(3)
  fifth = third.transpose(4)
  return pluck1(note) + pluck1(third) + pluck1(fifth)

def majorScale(note):
  second = note.transpose(2)
  third = second.transpose(2)
  fourth = third.transpose(1)
  fifth = fourth.transpose(2)
  sixth = fifth.transpose(2)
  seventh = sixth.transpose(2)
  eigth = seventh.transpose(1)
  return [note,second,third,fourth,fifth,sixth,seventh,eigth]
def minorScale(note):
  second = note.transpose(2)
  third = second.transpose(1)
  fourth = third.transpose(2)
  fifth = fourth.transpose(2)
  sixth = fifth.transpose(1)
  seventh = sixth.transpose(2)
  eigth = seventh.transpose(1)

  return [note,second,third,fourth,fifth,sixth,seventh,eigth]

def fractal():
  notes=['A', 'C', 'E', 'F', 'G']
  rules={
    "A":['C','F','E'],
    "C":['G','E'],
    "E":['C','G'],
    'F':['A','C'],
    'G':['E','F','C']
  }
 
  iterations=4
  for i in range(iterations):
    new_notes=[rules[x] for x in notes]
    new_notes=list(itertools.chain.from_iterable(new_notes))
    notes=new_notes

  result=[pluck1(Note(x),random.uniform(0.25,0.4)) for x in notes]
  chunk = numpy.concatenate(result) * 0.25

  p = pyaudio.PyAudio()
  stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
  stream.write(chunk.astype(numpy.float32).tobytes())
  stream.close()
  p.terminate()

 #next use specific scales from input
 #maybe add random rythmn patterns 
 #make melodies sound better
def dice():
  melodies = [['G','D','C','E'],['B','A','B'],['E','G','E','D'],['C','E','E','A','A','G','G'],['A','F','D']]
  song=[]
  length=50
  while len(song)<length:
    index = random.randint(0,len(melodies)-1)
    song.append(melodies[index])
  song=list(itertools.chain.from_iterable(song))
  song=[pluck1(Note(x),random.uniform(0.25,0.5)) for x in song]
  chunk = numpy.concatenate(song) * 0.25

  p = pyaudio.PyAudio()
  stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
  stream.write(chunk.astype(numpy.float32).tobytes())
  stream.close()
  p.terminate()

KEYS = ["C", "C#","D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SCALES = ["major", "minor"] #more coming soon
BITS_PER_NOTE = 4
def int_from_bits(bits: List[int]) -> int:
    return int(sum([bit*pow(2, index) for index, bit in enumerate(bits)]))


def genome_to_melody(genome: Genome, num_bars: int, num_notes: int, num_steps: int,
                     pauses: int, key: str, scale: str, root: int) -> Dict[str, list]:
    notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(num_bars * num_notes)]
    print(notes)
    scl = []
    if(scale == "major"):
      scl=majorScale(Note(key))
    
    else:
      scl=minorScale(Note(key))
    
    note_length = 3 / float(num_notes)
    melody=[]
    beats=[]

    for note in notes:
        integer = int_from_bits(note)
        if not pauses:
            integer = int(integer % pow(2, BITS_PER_NOTE - 1))

        if integer >= pow(2, BITS_PER_NOTE - 1):
            melody += [0]
            beats += [note_length]
        else:
            if len(melody) > 0 and melody[-1] == integer:
                beats[-1] += note_length
            else:
                melody += [integer]
                beats += [note_length]
    melody=[scl[(note+num_steps*2) % len(scl)] for note in melody]
    return {"melody":melody,"beats":beats}


def fitness(genome: Genome,  num_bars: int, num_notes: int, num_steps: int,
            pauses: bool, key: str, scale: str, root: int) -> int:
    notes = genome_to_melody(genome, num_bars, num_notes, num_steps, pauses, key, scale, root)

    song=[pluck1(note,notes["beats"][index]) for (index,note) in enumerate(notes["melody"])]
    chunk = numpy.concatenate(song) * 0.25
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    stream.write(chunk.astype(numpy.float32).tobytes())
    stream.close()
    p.terminate()

    rating = input("Rating (0-5)")
    rating = int(rating)

    return rating
#4 notes and generate baselines,melody,pop, jazz, etc. with different styules with scales and harmonzie with machine learning
#i always thought musicians and artists would be the last to have their jobs replaced  by machines
#add repetition and import into audio editing to create one big song
#generate chords
#add rythmn
#make full song from four notes
#pictures of charts of freuqnecy of music 
#pyaudio record and save
#music intervals
#design appliation
# help aspriing musicians find inspiration as a fellow musician
#didnt want to use an existing library for ai/machine learning, wanted to ode one from stratch
#fix github commit
#music aided by human hearing predict next note and length
#markov chain and genre using ai
#use machine learning to generate song by genre as initial dataset
#saw a youtube video of little girl (but what if we could create out of nothing like famous composers?)
#normal music composers lack human interaction to actually make sure it sounds good
#4 notes and generate based on genre random with machine learning and rate = true happiness
#show sheet music at eend
#use flask
#create.... out of notnhing
@click.command()
@click.option("--num-bars", default=8, prompt='Number of bars:', type=int)
@click.option("--num-notes", default=8, prompt='Notes per bar:', type=int)
@click.option("--num-steps", default=1, prompt='Number of steps:', type=int)
@click.option("--pauses", default=True, prompt='Introduce Pauses?', type=bool)
@click.option("--key", default="C", prompt='Key:', type=click.Choice(KEYS, case_sensitive=False))
@click.option("--scale", default="major", prompt='Scale:', type=click.Choice(SCALES, case_sensitive=False))
@click.option("--root", default=4, prompt='Scale Root:', type=int)
@click.option("--population-size", default=5, prompt='Population size:', type=int)
@click.option("--num-mutations", default=2, prompt='Number of mutations:', type=int)
@click.option("--mutation-probability", default=0.5, prompt='Mutations probability:', type=float)
def genetic_algo(num_bars: int, num_notes: int, num_steps: int, pauses: bool, key: str, scale: str, root: int,
  population_size: int, num_mutations: int, mutation_probability: float):
  population = [generate_genome(num_bars * num_notes * BITS_PER_NOTE) for _ in range(population_size)]
  print(population)
  running = True
  while running:
    random.shuffle(population)
    print(len(population))
    population_fitness = [(genome, fitness(genome, num_bars, num_notes, num_steps, pauses, key, scale, root)) for genome in population]
    sorted_population_fitness = sorted(population_fitness, key=lambda e: e[1], reverse=True)

    population = [e[0] for e in sorted_population_fitness]
    next_generation = population[0:2]
    for j in range(int(len(population) / 2) - 1):
      def find_fitness(genome):
          for e in population_fitness:
              if e[0] == genome:
                  return e[1]
          return 0

      parents = selection_pair(population, find_fitness)
      offspring_a, offspring_b = single_point_crossover(parents[0], parents[1])
      offspring_a = mutation(offspring_a, num=num_mutations, probability=mutation_probability)
      offspring_b = mutation(offspring_b, num=num_mutations, probability=mutation_probability)
      next_generation += [offspring_a, offspring_b]
    notes = genome_to_melody(population[0], num_bars, num_notes, num_steps, pauses, key, scale, root)
    song=[pluck1(note,notes["beats"][index]) for (index,note) in enumerate(notes["melody"])]
    chunk = numpy.concatenate(song) * 0.25
    input("here is the no1 hit …")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    stream.write(chunk.astype(numpy.float32).tobytes())
    stream.close()
    p.terminate()

    notes = genome_to_melody(population[1], num_bars, num_notes, num_steps, pauses, key, scale, root)

    song=[pluck1(note,notes["beats"][index]) for (index,note) in enumerate(notes["melody"])]
    chunk = numpy.concatenate(song) * 0.25
    input("here is the no2 hit …")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    stream.write(chunk.astype(numpy.float32).tobytes())
    stream.close()
    p.terminate()

    running = input("continue? [Y/n]") != "n"
    population = next_generation

