import random as rnd


# Evaluating Scores
WRONG_LETTER   = 0 # Letter not in word
CORRECT_LETTER = 1 # Correct letter, wrong spot
CORRECT_SPOT   = 2 # Correct letter in correct spot


class Game:
  def __init__(self) -> None:
    self.guesses = 6
    self.active_word = ''
    self.wlist = []
    self.load_word_list()
    self.guessed_words = []
    self.results = []

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
    while self.guesses != 0:
      results = self.guess_word(input("Enter guess: "))
      print(f'Result: {results}, Remaining guesses: {self.guesses}')
    self.reveal_word()   
    return True

  # Start a new game by choosing a random word and resetting the guess counter
  def play(self, player):
    if player.kind == "HUMAN":
      return self.start_game()
    l = len(self.wlist)
    w = rnd.randint(0, l)
    self.active_word = self.wlist[w]
    self.guesses = 6
    result = [-1, -1, -1, -1, -1]
    while self.guesses != 0:
      guess = player.get_guess(result, self)
      result = self.guess_word(guess)
      print(f'Result: {result}, Remaining guesses: {self.guesses}')
      player.trim_list(result, guess)
    self.reveal_word()   
    return True

  # Take in a guess and return a score and remaining moves
  def guess_word(self, guess):
    message = ''
    # If the player is out of turns
    if self.guesses == 0:
      message = 'Game over, no guesses left'
      return [-1, -1, -1, -1, -1]
    
    if guess not in self.wlist:
      message = "Word is not in list."
      return [-1,-1,-1,-1,-1]

    # If the guessed word is not 5 letters long
    if len(guess) != 5:
      message = 'Word is not 5 letters'
      return [-1, -1, -1, -1, -1]

    
    self.guessed_words.append(guess)

    # If the word has been guessed correctly
    if guess == self.active_word:
      message = '\x1b[6;30;42m' + 'Correct!' + '\x1b[0m'
      result = [2,2,2,2,2]
      self.guesses = 0

    else:
      result = [0,0,0,0,0]

      # Look for correct letters that are in the wrong place
      for i in range(5):
        if guess[i] in self.active_word:
          result[i] = 1

      # Look for correct letters that are in the right place
      for i in range(5):
        if self.active_word[i] == guess[i]:
          result[i] = 2

      # Decrement the guess counter
      self.guesses = self.guesses - 1
    self.results.append(result)
    self.print_board()
    print(message)
    return result

  # Reveal the active word and set guess counter to zero
  def reveal_word(self):
    print(f'The word was: {self.active_word}')
    self.guesses = 0

  # Print the board
  def print_board(self):
    index = 0
    print("-----------")
    for word in self.guessed_words:
      format = []
      result = self.results[index]
      for i in range(0,5):        
        if result[i] == CORRECT_SPOT:
          format.append('\x1b[6;30;42m'+word[i]+'\x1b[0m')
        elif result[i] == CORRECT_LETTER:
          check = word[i]
          num_actual = self.active_word.count(check)
          num = 0
          for j in range(0,5):
            if self.active_word[j] == check and result[j] == CORRECT_SPOT:
              num = num + 1
          if num == num_actual:
            format.append(word[i])
          else:
            format.append('\x1b[0;30;43m'+word[i]+'\x1b[0m')    
        else: format.append(word[i])
      print(f"|{format[0]}|{format[1]}|{format[2]}|{format[3]}|{format[4]}|")
      print("-----------")
      index = index + 1


