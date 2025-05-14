from src.core.games import Game
from src.spawners.spawners import RandomSpawner, SubsSpawner

game = Game()
game.spawner = RandomSpawner(game)
# game.spawner.spawners = [SubsSpawner]
game.run()
