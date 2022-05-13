import random as rnd

class Wordle:
  def __init__(self) -> None:
    self.guesses = 6
    self.active_word = ''
    self.wlist = []
    self.load_word_list()
  
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
  
  # Take in a guess and return a score and remaining moves
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
      return [2,2,2,2,2], self.guesses-1
    
    else:
      ret = [0,0,0,0,0]
      
      # Look for correct letters that are in the wrong place
      for i in range(5):
        if guess[i] in self.active_word:
          ret[i] = 1
      
      # Look for correct letters that are in the right place
      for i in range(5):
        if self.active_word[i] == guess[i]:
          ret[i] = 2
      
      # Decrement the guess counter
      self.guesses = self.guesses - 1
      return ret, self.guesses
    
  # Reveal the active word and set guess counter to zero
  def reveal_word(self):
    print(f'The word was: {self.active_word}')
    self.guesses = 0
      
      
       
w = Wordle() 
w.start_game()
results, guesses_left = w.guess_word('prose')
print(f'Guessed word: prose, Result: {results}, Remaining guesses: {guesses_left}')

results, guesses_left = w.guess_word('thing')
print(f'Guessed word: thing, Result: {results}, Remaining guesses: {guesses_left}')

results, guesses_left = w.guess_word('dulce')
print(f'Guessed word: dulce, Result: {results}, Remaining guesses: {guesses_left}')

results, guesses_left = w.guess_word('frost')
print(f'Guessed word: frost, Result: {results}, Remaining guesses: {guesses_left}')

results, guesses_left = w.guess_word('queen')
print(f'Guessed word: queen, Result: {results}, Remaining guesses: {guesses_left}')

results, guesses_left = w.guess_word('trunk')
print(f'Guessed word: trunk, Result: {results}, Remaining guesses: {guesses_left}')

results, guesses_left = w.guess_word('clamp')
print(f'Guessed word: clamp, Result: {results}, Remaining guesses: {guesses_left}')
w.reveal_word()