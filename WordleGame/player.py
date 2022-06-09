import random 
import pandas as pd
import numpy as np

from game import WRONG_LETTER, CORRECT_LETTER, CORRECT_SPOT

class Player(object):
  def __init__(self) -> None:
    self.kind = "HUMAN"
    self.letter_lists = ["abcdefghijklmnopqrstuvwxyz",]*5
    self.wrong_place = ''

  def trim_list(self, result, guess):
    for i in range(0,5):
      if result[i] == CORRECT_SPOT:
        self.letter_lists[i] = guess[i]
      if result[i] == CORRECT_LETTER:
        self.letter_lists[i] = self.letter_lists[i].replace(guess[i], '')
        self.wrong_place = self.wrong_place + guess[i]
      if result[i] == WRONG_LETTER:
        for j in range(0,5):
          self.letter_lists[j] = self.letter_lists[j].replace(guess[i],'') 
    #  print(guess[i], result[i], self.letter_lists[i])



class Computer(Player):
  def __init__(self) -> None:
    self.kind = "COMPUTER"
    self.letter_lists = ["abcdefghijklmnopqrstuvwxyz",]*5


class Rando(Player):
  def __init__(self) -> None:
    self.kind = "RANDOM"
    self.letter_lists = ["abcdefghijklmnopqrstuvwxyz",]*5
    self.wrong_place = ''

    
  def get_guess(self, word_list):
    guess = ''
    while guess not in word_list:
      guess = ''
      for i in range(0,5):
        list = self.letter_lists[i]
        index = random.randrange(0,len(list))
        letter = list[index]
        guess = guess + letter
      for j in self.wrong_place:
        if j not in guess:
          guess = ''
    return guess



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
      results (int[]): results from a guess
      guess (string): word guessed
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
