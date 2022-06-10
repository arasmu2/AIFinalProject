import time
from game import Game
from player import Computer, Rando, Player



def trials(kind, file_name):
  trial = 0  #initialize trial number
  N = 50  #number of games played
  score = [] #keep track of how many guesses it took
  while (trial < N):
    if kind == "COMPUTER":
      player = Computer()
    if kind == "RANDO":
      player = Rando()
    if kind == "HUMAN":
      player = Player()
    game = Game()
    score.append(game.play(player))
    trial = trial + 1
  file = open(file_name, "w")
  file.write(str(score))
  file.close()




if __name__ == '__main__':

  play = True
  print("Welcome to the wordle (not actually wordle) playing bot.\n")
  while play:
    print("\nChoose a player.\n")
    print("Options: \n")
    print("   1:   Human")
    print("   2:   Rando, an agent that uses a stocastic heuristic")
    print("   3:   Computer, an agent that uses letter probability")
    print("   4:   Generate trials data")
    print("   5:   Quit")

    option = int(input("\nEnter option: "))
    game = Game()
    match option:
      case 1:
        player = Player()
        game.play(player) 
      case 2:
        player = Rando()
        game.play(player)
      case 3:
        player = Computer()
        game.play(player)
      case 4:
        player1 = "COMPUTER"
        trials(player1, "computer_trials.txt")
        player2 = "RANDO"
        trials(player2, "rando_trials.txt")

      case 5:
        print("Thank you for playing.")
        play = False
        time.sleep(3)
      case default:
        print("\nInvalid selection.  Try again.\n")
