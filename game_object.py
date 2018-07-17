import pygame

class GameObject:

    id = 0

    def __init__(self, game, x, y, width, height, color):
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        if self.game.debug:
            self.old_color = color
        self.id = GameObject.id
        GameObject.id += 1

    def update(self):
        pass

    def x(self):
        return self.rect.left + (self.rect.width >> 1)

    def y(self):
        return self.rect.top + (self.rect.height >> 1)

    def collide(self):
        pass