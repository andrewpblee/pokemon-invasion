import pygame
from pygame.sprite import Sprite

class Gotcha(Sprite):

    def __init__(self, screen, pokemon_x, pokemon_y):
        super().__init__()

        self.screen = screen
        self.image = pygame.image.load('images/gotcha.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = pokemon_x + 25
        self.rect.centery = pokemon_y + 25
        self.center = float(self.rect.centerx)


    def draw_gotcha(self):
        self.screen.blit(self.image, self.rect)

