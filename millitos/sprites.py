import pygame
from ajustes import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((celda, celda))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            number_image = pygame.image.load(self.text)
            self.image.blit(number_image, (0, 0))
        else:
            self.image.fill(WHITE)

    def update(self):
        self.rect.x = self.x * celda
        self.rect.y = self.y * celda

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    
    def right(self):
        return self.rect.x + celda < juego_size * celda

    def left(self):
        return self.rect.x - celda >= 0

    def up(self):
        return self.rect.y - celda >= 0

    def down(self):
        return self.rect.y + celda < juego_size * celda
