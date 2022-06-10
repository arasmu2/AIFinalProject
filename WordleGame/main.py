import time
from game import Game
from player import Computer, Rando, Player

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
        print("Trials to come...")
      case 5:
        print("Thank you for playing.")
        play = False
        time.sleep(10)
      case default:
        print("\nInvalid selection.  Try again.\n")
