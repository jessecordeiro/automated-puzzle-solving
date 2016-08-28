# automated puzzle solving

# overview
Puzzle solving is a typically human activity that, in recent decades, is being explored in the context of
computers. There are two benefits to this: first, we can off-load some puzzle-solving tasks to computers, and
second, we may understand human puzzle-solving better by studying how to implement it on a computer.

This project investigates a class of puzzles that have the following features in common:

* full information: all information about the puzzle conguration at any given point is visible to the solver; there are no hidden or random aspects

* well-defined extensions: a denition of legal extensions from a given puzzle conguration to new congurations is given

* well-defined solution: a denition of what it means for the puzzled to be in a solved state is given

These features are common to a very large class of puzzles: crosswords, sudoku, peg solitaire, verbal
arithmetic, and so on. This project generalizes the required features into an abstract superclass Puzzle,
and solving functions are written in terms of this abstract class.
Particular concrete puzzles are be modelled as subclasses of Puzzle, and solved using
the solving functions. Although there may be faster puzzle-specific solvers for a particular puzzle by knowing
specific features of that puzzle, the general solvers are designed to work for all puzzles of this sort.
