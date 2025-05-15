from core.games import Game
from core.spawners.spawners import *

game = Game()
game.spawner = RandomSpawner(game)
game.spawner.spawners = [DeleteToEnd]
game.run()
