import random
import pandas as pd
import numpy as np

from game import Game
from game import WRONG_LETTER, CORRECT_LETTER, CORRECT_SPOT
from player import Computer, Rando

class State():
  def __init__(self, previous=None):
    self.previous = previous # pointer to previous state
    self.guess = ''          # guess leading to this state
    self.rejected = []       # letters guessed but are not in solution
    self.wrong_spot = []     # correct letters in wrong spots
    self.correct = []        # correct letters in the right spot, (index, char)
    self.unguessed_words = []

  def next(self, results, guess):
    '''
    Creates the next state after this one given the updated information
      result (int[]): results from a guess
      guess (string): word guessedd
      Return: State
    '''
    if results == [-1, -1, -1, -1, -1]:
      return self

    next = State(self)
    next.unguessed_words = self.unguessed_words.copy()
    next.guess = guess
    for x in range(5):
      if results[x] == CORRECT_SPOT:
        next.correct.append((x, guess[x]))
        next.remove_words_without_at(guess[x], x)
      elif results[x] == CORRECT_LETTER:
        next.wrong_spot.append(guess[x])
        next.remove_words_without(guess[x])
      elif results[x] == WRONG_LETTER:
        next.rejected.append(guess[x])
        next.remove_words_with(guess[x])

    return next

  def remove_words_with(self, c):
    '''
    Filters guess list with words that contain c
      c (char): character that must not be included
    '''
    for word in self.unguessed_words:
      if c in word:
        self.unguessed_words.remove(word)

  def remove_words_without(self, c):
    '''
    Filters guess list with words that don't contain c
      c (char): required character
    '''
    for word in self.unguessed_words:
      if c not in word:
        self.unguessed_words.remove(word)

  def remove_words_without_at(self, c, index):
    '''
    Filters guess list without c at index
      c (char): required character
      index (int): index of requred character
    '''
    for word in self.unguessed_words:
      if word[index] is not c:
        self.unguessed_words.remove(word)

# These methods are probably not necessary, but they may be helpful for outputting information
  def all_guesses(self):
    '''
    Returns a list of all guessed words so far.
      Returns: string[]
    '''
    guesses = []
    guesses.append(self.guess)
    p = self.previous
    while p is not None:
      guesses.append(p.guess)
      p = p.previous
    return guesses

  def all_rejected(self):
    '''
    Returns a list of all rejected characters so far
      Returns: char[]
    '''
    r = []
    r.extend(self.rejected)
    p = self.previous
    while p is not None:
      r.extend(p.rejected)
      p = p.previous
    return r

  def all_wrong_spot(self):
    '''
    Returns a list of all the right characters in the wrong spots so far
      Returns: char[]
    '''
    r = []
    r.extend(self.wrong_spot)
    p = self.previous
    while p is not None:
      r.extend(p.wrong_spot)
      p = p.previous
    return r

  def all_correct(self):
    '''
    Returns a list of all the right characters in the right spots so far
      Returns: char[]
    '''
    r = []
    r.extend(self.correct)
    p = self.previous
    while p is not None:
      r.extend(p.correct)
      p = p.previous
    return r
  
  def heuristics(self, game, results):
    num = len(self.unguessed_words)
    word_stack = pd.DataFrame({'words': pd.Series(self.unguessed_words), 'h': pd.Series((np.zeros(num)), dtype=float)})

    for n in range(0, num):
      h = 10
      compare_to = list(game.active_word)
      guess = list(self.unguessed_words[n])
      for i in range(0, 5):
        if (results[i] == 2):
          if (guess[i] == compare_to[i]):
            h = h - 2
        elif (results[i] == 1):
          for j in range(0, 5):
            if (guess[j] == compare_to[i]):
              h = h - 1
        else:
          l_value = game.lprob.loc[self.unguessed_words[n][i]]  # find probabability
          h = h - l_value

      word_stack.iloc[n, 1] = h
    column = word_stack["h"]
    min_h = column.idxmin()
    print('best guess', word_stack.iloc[min_h, 0], 'heuristic=', word_stack.iloc[min_h, 1])
    return(word_stack.iloc[min_h, 0])
  
  def print_all(self):
    print('Guesses:', self.all_guesses())
    print('Rejected:', sorted(set(self.all_rejected())))
    print('Wrong Spots:', sorted(set(self.all_wrong_spot())))
    print('Correct:', sorted(set(self.all_correct())))

  def __repr__(self):
    return f"State(Previous: {self.previous is not None}, Guess: '{self.guess}', Rejected: {self.rejected}, Wrong Spots: {self.wrong_spot}, Correct: {self.correct}, Unguessed Words left: {len(self.unguessed_words)})"


# Function for performing a simple test
def simple_test():
  state = State() 
  game = Game()
  state.unguessed_words = game.wlist # Should probably write a function for this, just wanted to do it this way for testing
  game.start_game()
  guesses = ['audio']

  for g in guesses:
    results = game.guess_word(state.heuristics(game, results))
    if game.guesses != 0:
      state = state.next(results, g)
    print(f'Guessed word: {g}, Result: {results}, Remaining guesses: {game.guesses}')
    print(state, '\n')
    
    #input next word based on heuristics
    high_pct = state.heuristics(game, results)
    guesses = guesses.append(high_pct)
    print('heuristic guess', high_pct)
    if(high_pct == game.active_word):
      print('You are correct!!')
      game.guesses = 0
  print('Remaining words:', state.unguessed_words)
  print('Remaining words contains answer:', game.active_word in state.unguessed_words)
  print('\n')
  state.print_all()
  game.reveal_word()


# Function for a human player to play the game
def human_play():
  state = State()
  game = Game()
  state.unguessed_words = game.wlist
  game.start_game()
  guesses = 0
  while guesses < 6:
    guess = input("Enter guess: ")
    results = game.guess_word(guess)
    state = state.next(results, guess)
    print(f'Guessed word: {guess}, Result: {results}')
  print('Remaining words:', state.unguessed_words)
  print('Remaining words contains answer:', game.active_word in state.unguessed_words)
  print('\n')
  state.print_all()
  game.reveal_word()
   
  

if __name__ == '__main__':

  game = Game() 
  player = Computer()
  game.play(player)

