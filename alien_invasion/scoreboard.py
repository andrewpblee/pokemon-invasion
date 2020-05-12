import pygame.font
from pygame.sprite import Group
from pokeball import Pokeball

class Scoreboard():

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = f'{rounded_score:,}'
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # we're classing a level as part of the score
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)


    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = f'{high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 100
        self.level_rect.top = self.score_rect.top

    def prep_lives(self):
        self.lives = Group()
        for lives_number in range(self.stats.lives_left):
            life = Pokeball(self.ai_settings, self.screen)
            life.rect.x = 10 + lives_number * (life.rect.width * 1.2)
            life.rect.y = 25
            self.lives.add(life)