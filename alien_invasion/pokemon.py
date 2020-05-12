import pygame
from pygame.sprite import Sprite
import random

pokemon_list = ['images/pikachu.bmp',
                'images/bulbasor.bmp',
                'images/charizard.bmp',
                'images/squirtle.bmp',
                'images/188991.bmp',
                'images/188992.bmp',
                'images/188993.bmp',
                'images/188994.bmp',
                'images/188995.bmp',
                'images/188996.bmp',
                'images/188997.bmp',
                'images/188998.bmp',
                'images/188999.bmp',
                'images/189000.bmp',
                'images/189001.bmp',
                'images/189002.bmp',
                'images/189003.bmp',
                'images/189004.bmp',
                'images/189005.bmp',
                'images/189006.bmp',
                ]


class Pokemon(Sprite):

    def __init__(self, ai_settings, screen):

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load(random.choice(pokemon_list))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.pokemon_speed_factor
                   * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        self.screen.blit(self.image, self.rect)


