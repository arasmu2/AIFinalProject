
from game import Game
from player import Computer, Rando, Player

if __name__ == '__main__':

  score = []
  for i in range(0, 50):
    game = Game()
    player = Computer()
    score.append(game.play(player))

  with open('result.txt', 'w+') as f:
    f.write(str(score))
    f.close()
