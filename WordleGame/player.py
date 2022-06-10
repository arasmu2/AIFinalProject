import random 

from game import WRONG_LETTER, CORRECT_LETTER, CORRECT_SPOT

class Player(object):
  def __init__(self) -> None:
    self.kind = "HUMAN"
    self.letter_lists = ["abcdefghijklmnopqrstuvwxyz",]*5
    self.wrong_place = ''
    self.word_list = []
    self.load_word_list()


  def load_word_list(self):
    with open('word_list.txt') as f:
      for l in f:
        self.word_list.append(l.rstrip())


  def trim_list(self, result, guess):
    if result == [-1, -1, -1, -1, -1]:
      return
    for x in range(5):
      if result[x] == CORRECT_SPOT:
        self.remove_words_without_at(guess[x], x)
      elif result[x] == CORRECT_LETTER:
        self.remove_words_without(guess[x])
      elif result[x] == WRONG_LETTER:
        self.remove_words_with(guess[x])
 
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


  
  def remove_words_with(self, letter):
    '''
    Filters guess list with words that contain letter that must not be included
    '''
    for word in self.word_list:
      if letter in word:
        self.word_list.remove(word)



  def remove_words_without(self, letter):
    '''
    Filters guess list with words that don't contain letter required character
    '''
    for word in self.word_list:
      if letter not in word:
        self.word_list.remove(word)


  def remove_words_without_at(self, letter, index):
    '''
    Filters guess list without letter at index
    '''
    for word in self.word_list:
      if word[index] is not letter:
        self.word_list.remove(word)



class Computer(Player):
  def __init__(self) -> None:
    self.kind = "COMPUTER"
    self.letter_lists = ["abcdefghijklmnopqrstuvwxyz",]*5
    self.wrong_place = ''
    self.word_list = []
    self.load_word_list()
    self.lprob = {}
    self.load_letter_prob()

  def load_letter_prob(self):
    with open('letter_prob.txt') as f:
      for l in f:
        letter = l[0]
        l = l[1::]
        l = l[1::]
        self.lprob[letter] = float(l)


#    self.lprob = pd.read_csv('letter_prob.csv', header=0, index_col='Letter')

  def get_guess(self, result, game):
    if result == [-1, -1, -1, -1, -1]:
      return random.choice(self.word_list)
    return self.heuristics(result, game)

  
  def heuristics(self, result, check):
    #num = len(self.word_list)
    word_stack = {}
    for word in self.word_list:
      word_stack[word] = 0.0
    #word_stack = pd.DataFrame({'words': pd.Series(self.word_list), 'h': pd.Series((np.zeros(num)), dtype=float)})

    for guess in self.word_list:
    #for n in range(0, num):
      h = 10
      compare_to = check
      #guess = self.word_list[n]
      for i in range(0, 5):
        if (result[i] == 2):
          if (guess[i] == compare_to[i]):
            h = h - 2
        elif (result[i] == 1):
          for j in range(0, 5):
            if (guess[j] == compare_to[i]):
              h = h - 1
        else:
          l_value = self.lprob[guess[i]]
          #l_value =  self.lprob.loc[self.word_list[n][i]]  # find probabability set to zero for h1
          h = h - l_value

      word_stack[guess] = h
    column = []
    for word in self.word_list:
      column.append(word_stack[word])
    #column = word_stack["h"]
    min_h = min(column)
    min_guesses = [key for key in word_stack if word_stack[key] == min_h]
    return random.choice(min_guesses)
    #min_h = column.idxmin()
    #valid_min = word_stack[word_stack.h == column[min_h]]
    #print('best guess', word_stack.iloc[min_h, 0], word_stack.iloc[min_h, 1])
    #return (word_stack.iloc[min_h, 0])
    #return (word_stack.iloc[rnd.randint(0,num-1), 0])


class Rando(Player):
  def __init__(self) -> None:
    self.kind = "RANDOM"
    self.letter_lists = ["abcdefghijklmnopqrstuvwxyz",]*5
    self.wrong_place = ''
    self.word_list = []
    self.load_word_list()


  def get_guess(self, result, check):
    guess = ''
    while guess not in self.word_list:
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


  
  def print_all(self):
    print('Guesses:', self.all_guesses())
    print('Rejected:', sorted(set(self.all_rejected())))
    print('Wrong Spots:', sorted(set(self.all_wrong_spot())))
    print('Correct:', sorted(set(self.all_correct())))

  def __repr__(self):
    return f"State(Previous: {self.previous is not None}, Guess: '{self.guess}', Rejected: {self.rejected}, Wrong Spots: {self.wrong_spot}, Correct: {self.correct}, Unguessed Words left: {len(self.unguessed_words)})"
