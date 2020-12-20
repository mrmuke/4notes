## Inspiration
I saw this youtube video online of a little girl, who was told of 4 notes, and she had to compose a piece out of it. I was astonished by the masterpiece she composed on the spot and her talent, and as a pianist and coder, I became quite interested in the power of machines to create and wanted to see the extent to which I could reach in creating concert-level pieces in music. 

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
#show sheet music at eend
#create.... out of nothing
#models define patterns and rules in music that the machine can learn and identify

## What it does
I know machines have created before using massive datasets, but I wanted to add a touch of human interaction as we as humans can truly understand and interpret music in unique and emotional ways, something that machines are not yet capable of. So, I did some digging and found out about the genetic algorithm. An algorithm that is similar to the process of evolution, the genetic algorithm goes by the rule of "survival of the fittest". Firstly, it generates a few pieces using the already trained model (by predicting sequences from a random input sequence) and displays them to the user. The user then listens to them, and rates each of them out of 10. Then, the best two pieces reproduce to produce two more offspring through the process of single-point crossover, where they each get genes from both of their parents. Then, some keys of the child pieces are mutated into different ones to provide uniqueness. These are then downloaded to the user if the user is satisfied, or the user can choose to continue the process by again rating each of them out of 10 and putting them through the genetic algorithm.

## How I built it
First I trained a Keras (Tensorflow) model with notes I parsed from midi files that resembled the works of classical composers such as Beethoven, Bach, Chopin, and Tchaikovsky using LSTM (long short term memory) and multiple layers to ensure that the model fit. Then, I trained the model using 100 epochs and obtained the weights, then using the weights to predict the next notes for a randomly generated sequence of notes and could now produce pieces that sounded good already that kind of resembled the style of the classical period of music. Then, I created a webserver using flask to create the ui that implemented the genetic algorithm by asking users to rate each of the pieces generated to select those and produce offspring from them. 

## Challenges I ran into
There weren't a lot of resources on implementation of the genetic algorithm and how it related to music so I had to read about it and create one entirely myself. I'm relatively new to machine learning and figuring out the best fit for the model and not overfitting or underfitting was hard. I

## Accomplishments that I'm proud of
In the past, there were already music composition tools, but I was able to create something new, a tool that used physical humans to determine the quality of music so that the outcome was entirely formed by the user in the end. I hadn't used any of these tools before and learned how algorithms that I've learned could be applied to my individual projects. I'm also proud of figuring out how to implement the genetic algorithm into my program.

## What I learned
I learned how to use a multi-layer LSTM neural network to produce outputs from a set of inputs and how to train it with data. I learned that 

## What's next for 4notes
I want 4notes to be able to generate music for specific genres, not just classical music, so I will train models for different genres such as modern, pop, etc., and be able to produce music for diverse categories. Additionally, I want to be able to display sheet music (which should be easy as the output is in midi file format). 
add different genres
show sheet music
play 4 notes (already can identify them)
deploy for the public to use
