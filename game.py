import pygame
import random
from game_object import GameObject
from mobile_game_object import MobileGameObject
from enemy import Enemy

class Game:

    def __init__(self, width, height, tile_size, debug):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_width = int(self.width / self.tile_size)
        self.map_height = int(self.height / self.tile_size)
        self.clock = pygame.time.Clock()
        self.debug = debug
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.game_objects = []

        self.player = MobileGameObject(self, 25, 25, 20, 20, (200, 85, 0))
        self.game_objects.append(self.player)


        for i in range(75):
            wall = GameObject(self,
                              random.randint(0, self.map_width - 1) * self.tile_size,
                              random.randint(0, self.map_height - 1) * self.tile_size,
                              self.tile_size, self.tile_size, (0, random.randint(125, 255), 0))
            self.game_objects.append(wall)

        self.enemies = [
            Enemy(self, self.width - 75, self.height - 75, 20, 20, (255, 0, 0)),
            Enemy(self, 24, self.height - 75, 20, 20, (255, 0, 0)),
            Enemy(self, self.width - 75, 25, 20, 20, (255, 0, 0))
        ]
        self.game_objects += self.enemies


    def draw_enemy_lines(self):

        for enemy in self.enemies:

            pygame.draw.line(self.screen,
                             (255, 195, 0),
                             (enemy.x(), enemy.y()),
                             (self.player.x(), self.player.y()))

            if enemy.target is not None:
                pygame.draw.line(self.screen,
                                 (200, 0, 0),
                                 (enemy.x(), enemy.y()),
                                 (enemy.target[0], enemy.target[1]))

            if len(enemy.path) > 0:
                pygame.draw.line(self.screen, (25, 25, 200),
                                 (enemy.target[0],
                                  enemy.target[1]),
                                 (enemy.path[-1][0],
                                  enemy.path[-1][1]))

                for i in range(len(enemy.path) - 1):
                    pygame.draw.line(self.screen, (25, 25, 200),
                                     (enemy.path[i][0], enemy.path[i][1]),
                                     (enemy.path[i+1][0], enemy.path[i+1][1]))

    def execute(self):
        exit = False

        while not exit:
            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.dy = -2
                    if event.key == pygame.K_DOWN:
                        self.player.dy = 2
                    if event.key == pygame.K_LEFT:
                        self.player.dx = -2
                    if event.key == pygame.K_RIGHT:
                        self.player.dx = 2
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP and self.player.dy < 0:
                        self.player.dy = 0
                    if event.key == pygame.K_DOWN and self.player.dy > 0:
                        self.player.dy = 0
                    if event.key == pygame.K_LEFT and self.player.dx < 0:
                        self.player.dx = 0
                    if event.key == pygame.K_RIGHT and self.player.dx > 0:
                        self.player.dx = 0

            #Updates and Rendering
            if self.debug:
                # self.screen.fill((125, 125, 255))
                self.screen.fill((0, 0, 0))
                for i in range(self.map_height):
                    for j in range(self.map_width):
                        val = Enemy.grid[i][j]
                        val = val * 6
                        val = 255 - val
                        if val > 0:
                            pygame.draw.rect(self.screen,
                                             (0, val, val),
                                             (j * self.tile_size,
                                              i * self.tile_size,
                                              self.tile_size,
                                              self.tile_size))
            else:
                self.screen.fill((125, 125, 255))

            for game_object in self.game_objects:
                game_object.update()
                pygame.draw.rect(self.screen, game_object.color, game_object.rect)

            if self.debug:
                self.draw_enemy_lines()

            pygame.display.flip()
            self.clock.tick(60)