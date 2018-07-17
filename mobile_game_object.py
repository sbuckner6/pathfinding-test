import pygame
from game_object import GameObject

class MobileGameObject(GameObject):

    def __init__(self, game, x, y, width, height, color):
        GameObject.__init__(self, game, x, y, width, height, color)
        self.dx = 0
        self.dy = 0
        self.visited = []

    def update(self):
        if self.rect.left + self.dx > 0 and self.rect.right + self.dx < self.game.width:
            self.rect.left += self.dx
        if self.rect.top + self.dy > 0 and self.rect.bottom + self.dy < self.game.height:
            self.rect.top += self.dy
        self.handle_collision()

    def handle_collision(self):
        x_rect = pygame.Rect(self.rect.left,
                             self.rect.top - self.dy,
                             self.rect.width,
                             self.rect.height)

        y_rect = pygame.Rect(self.rect.left - self.dx,
                             self.rect.top,
                             self.rect.width,
                             self.rect.height)

        collided = False

        for other_object in self.game.game_objects:
            if other_object.id == self.id:
                continue

            if self.rect.colliderect(other_object.rect):
                if self.dx > 0 and x_rect.colliderect(other_object.rect):
                    self.rect.right = other_object.rect.left
                elif self.dx < 0 and x_rect.colliderect(other_object.rect):
                    self.rect.left = other_object.rect.right
                if self.dy > 0 and y_rect.colliderect(other_object.rect):
                    self.rect.bottom = other_object.rect.top
                elif self.dy < 0 and y_rect.colliderect(
                        other_object.rect):
                    self.rect.top = other_object.rect.bottom
                collided = True

        return collided