import random as rnd
import pandas as pd
import numpy as np

# Evaluating Scores
WRONG_LETTER   = 0 # Letter not in word
CORRECT_LETTER = 1 # Correct letter, wrong spot
CORRECT_SPOT   = 2 # Correct letter in correct spot

class Wordle:
  def __init__(self) -> None:
    self.guesses = 6
    self.active_word = ''
    self.wlist = []
    self.load_word_list()
    self.lprob = pd.read_csv('letter_prob.csv', header=0, index_col='Letter')

  
  # Load the list of words  
  def load_word_list(self):
    with open('word_list.txt') as f:
      for l in f:
        self.wlist.append(l.rstrip())
  
  # Start a new game by choosing a random word and resetting the guess counter
  def start_game(self):
    l = len(self.wlist)
    w = rnd.randint(0, l)
    self.active_word = self.wlist[w]
    self.guesses = 6
    return True
  
  # Take in a guess and return an Evaluating score and remaining moves
  def guess_word(self, guess):
    # If the player is out of turns
    if self.guesses == 0:
      print(f'Game over, no guesses left')
      return [-1, -1, -1, -1, -1], 0
  
    # If the guessed word is not 5 letters long
    if len(guess) != 5:
      print(f'Word is not 5 letters')
      return [-1, -1, -1, -1, -1], self.guesses
    
    # If the word has been guessed correctly
    if guess == self.active_word:
      return [CORRECT_SPOT for _ in range(5)], self.guesses-1
    
    else:
      ret = [WRONG_LETTER for _ in range(5)]
      
      # Look for correct letters that are in the wrong place
      for i in range(5):
        if guess[i] in self.active_word:
          ret[i] = CORRECT_LETTER
      
      # Look for correct letters that are in the right place
      for i in range(5):
        if self.active_word[i] == guess[i]:
          ret[i] = CORRECT_SPOT
      
      # Decrement the guess counter
      self.guesses = self.guesses - 1
      return ret, self.guesses
    
  # Reveal the active word and set guess counter to zero
  def reveal_word(self):
    print(f'The word was: {self.active_word}')
    self.guesses = 0
      
class State():
  def __init__(self, previous=None):
    self.previous = previous # pointer to previous state
    self.guess = ''          # guess leading to this state
    self.rejected = []       # letters guessed but are not in word
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
      print(x)
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
  
  def heuristics(self):

    num = len(s.unguessed_words)
    word_stack = pd.DataFrame({'words': pd.Series(s.unguessed_words), 'h': pd.Series((np.zeros(num)), dtype=float)})

    for n in range(0, num):
      h = 10
      compare_to = list(w.active_word)
      guess = list(s.unguessed_words[n])
      for i in range(0, 5):
        if (results[i] == 2):
          if (guess[i] == compare_to[i]):
            h = h - 2
        elif (results[i] == 1):
          for j in range(0, 5):
            if (guess[j] == compare_to[i]):
              h = h - 1
        else:
          l_value = w.lprob.loc[s.unguessed_words[n][i]]  # find probabability
          h = h - l_value

      word_stack.iloc[n, 1] = h
    column = word_stack["h"]
    min_h = column.idxmin()
    print('best guess', word_stack.iloc[min_h, 0], word_stack.iloc[min_h, 1])
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
  s = State() 
  w = Wordle()
  s.unguessed_words = w.wlist # Should probably write a function for this, just wanted to do it this way for testing
  w.start_game()
  guesses = ['audio', 'thing', 'dulce', 'frost', 'queen', 'trunk', 'clamp']

  guesses_left = 5
  for g in guesses:
    results, guesses_left = w.guess_word(g)
    s = s.next(results, g)
    print(f'Guessed word: {g}, Result: {results}, Remaining guesses: {guesses_left}')
    print(s, '\n')
    
    #input next word based on heuristics
    high_pct = s.heuristics()
    guesses[6-guesses_left]=high_pct
    print('heuristic guess', high_pct)
    if(high_pct == w.active_word):
      print('You are correct!!')  
  print('Remaining words:', s.unguessed_words)
  print('Remaining words contains answer:', w.active_word in s.unguessed_words)
  print('\n')
  s.print_all()
  w.reveal_word()


# Function for a human player to play the game
def human_play():
  state = State()
  wordle = Wordle()
  state.unguessed_words = wordle.wlist
  wordle.start_game()
  guesses = 0
  while guesses < 6:
    guess = input("Enter guess: ")
    results = wordle.guess_word(guess)
    state = state.next(results, guess)
    print(f'Guessed word: {guess}, Result: {results}')
  print('Remaining words:', state.unguessed_words)
  print('Remaining words contains answer:', wordle.active_word in state.unguessed_words)
  print('\n')
  state.print_all()

  wordle.reveal_word()
   
  

if __name__ == '__main__':
  human_play()
  
