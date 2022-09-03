# genetic_Algoritm_sudoku
Sudoku is a puzzle game designed for a single player, much like a crossword puzzle. The puzzle itself is nothing more than a grid of little boxes called “cells” or “squares”. They are stacked nine height and nine width, making 81 squares total. The puzzle comes with some of the squares (usually less than half of them) already filled in, like figure1. One of the rules this game is that you do not repeat any number in any row or column (in 9 . 9 grid). Another rule is numbers should not be repeated in each 3 . 3 square. With these rules you have to fill the sudoku table like figure2.

Your task is to solve sudoku table (any given sudoku table) by Genetic Algorithm. The genetic algorithm attempts to iteratively improve a population of candidate solutions. In general, genetic algorithm performs the following steps:

· Initial Population: Defines the set of possible solutions (you can choose random numbers)

· Fitness Function: Defines the function that evaluate whether an individual is how much fit

· Selection: Using the results obtained from the fitness function selects the fittest individuals

· Crossover: The selected individuals are ‘mated’ and an offspring is produced

· Mutation: Some of the individuals may be mutated with a small probability

After following the steps mentioned above, the newly created generation replaces the individuals with bad fitness value (bad fitness be throw away) and the process repeats. Initial population could be 100. The probability of crossover could be %85 and mutation %15 or even less. These information are suggestion.
