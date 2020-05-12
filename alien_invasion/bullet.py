import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, ai_settings, screen, hero):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/pokeball.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = hero.rect.centerx - 15
        self.rect.top = hero.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)