import pygame
from pygame.sprite import Sprite

class Pokeball(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()

        self.screen = screen
        self.image = pygame.image.load('images/pokeball.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)