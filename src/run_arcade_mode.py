from core.games import Game
from core.spawners.spawners import RandomSpawner

game = Game()
game.spawner = RandomSpawner(game)
# game.spawner.spawners = [SubsSpawner]
game.run()
