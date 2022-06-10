
from game import Game
from player import Computer, Rando, Player


def trials(player, file_name):
  game = Game()
  trial = 0  #initialize trial number
  N = 50  #number of games played
  score = [] #keep track of how many guesses it took
  while (trial < N):
    score.append(game.play(player))
    trial = trial + 1
  file = open(file_name, "w")
  file.write(score)
  file.close()

