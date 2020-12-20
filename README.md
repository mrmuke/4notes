## Running It
Run python server.py to start flask
## Inspiration
**I always thought musicians and artists would be the last to have their jobs replaced by machines** I saw this youtube video online of a little girl, who was told of 4 notes, and she had to compose a piece out of it. I was astonished by the masterpiece she composed on the spot and her talent, and as a pianist and coder, I became quite interested in the power of machines to create and wanted to see the extent to which I could reach in creating concert-level pieces in music. Composing music is hard, and I want to help fellow musicians find inspiration. **If machines can never truly understand music, then why don't we work with them to create out of nothing like we do?**

## What it does
I know machines have created before using massive datasets, but I wanted to add a touch of human interaction as we as humans can truly understand and interpret music in unique and emotional ways, something that machines are not yet capable of. These models, in a way, have learned rules and patterns in classical music that we humans can't even identify after reviewing such a large dataset by seeing how notes interact and the jumps that are often made. So, I did some digging and found out about the genetic algorithm. An algorithm that is similar to the process of evolution, the genetic algorithm goes by the rule of "survival of the fittest". Firstly, it generates a few pieces using the already trained model (by predicting sequences from a random input sequence) and displays them to the user. The user then listens to them, and rates each of them out of 10. Then, the best two pieces reproduce to produce two more offspring through the process of single-point crossover, where they each get genes from both of their parents. Then, some keys of the child pieces are mutated into different ones to provide uniqueness. These are then downloaded to the user if the user is satisfied, or the user can choose to continue the process by again rating each of them out of 10 and putting them through the genetic algorithm. **Ultimately, the best sound will survive!**

## How I built it
First I trained a Keras (Tensorflow) model with notes I parsed from midi files that resembled the works of classical composers such as Beethoven, Bach, Chopin, and Tchaikovsky using LSTM (long short term memory) and multiple layers to ensure that the model fit. Then, I trained the model using 100 epochs and obtained the weights, then using the weights to predict the next notes for a randomly generated sequence of notes and could now produce pieces that sounded good already that kind of resembled the style of the classical period of music. Then, I created a web server using Flask to create the UI that implemented the genetic algorithm by asking users to rate each of the pieces generated to select those and produce offspring from them. 

## Challenges I ran into
There weren't a lot of resources on the implementation of the genetic algorithm and how it related to music so I had to read about it and create one entirely myself. I'm relatively new to machine learning and figuring out the best fit for the model and not overfitting or underfitting was also a hard process. The training process also took a very long time, so I wasn't able to test because I didn't realize the time it takes to train a model, even with batch normalization.

## Accomplishments that I'm proud of
In the past, there were already music composition tools made, but I was able to create something new, a tool that used physical humans to determine the quality of music so that the outcome was entirely formed by the user in the end. I hadn't used any of these tools before and learned how algorithms that I've learned could be applied to my individual projects. I'm also proud of figuring out how to implement the genetic algorithm into my program. I've never really used any of the tools that used in this project before so I'm proud of pushing the limits and exploring unknown or unclear concepts and tools.

## What I learned
I learned how to use a multi-layer LSTM neural network to produce outputs from a set of inputs and how to train it with data. I learned the genetic algorithm and this experience taught me how there are many algorithms embedded into nature through the sciences that can be applied to coding in interesting ways. Finally, I learned how to manipulate an algorithm that is abstract and can be used in many different cases and think through how it would apply to my specific problem. 

## What's next for 4notes
I want 4notes to be able to generate music for specific genres, not just classical music, so I will train models for different genres such as modern, pop, etc., and be able to produce music for diverse categories. Additionally, I want to be able to display sheet music (which should be easy as the output is in midi file format). I also then want to be able to accomplish exactly what the girl did in the video, have the user play a sequence of notes, and compose an entire musical piece entirely based on those notes using advanced musical rules and different structures(ABA, ABC, etc.). Finally, I want to deploy it for the public to use once all of these features are done. I want to turn this into an actual app in which anyone can create and listen to their products, mixing and matching until they are satisfied with the music.** I believe that everyone is compelled and inspired to create.**
