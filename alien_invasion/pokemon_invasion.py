import pygame
from settings import Settings
from hero import Hero
from game_stats import GameStats
from scoreboard import Scoreboard
from pygame.sprite import Group
from button import Button
import game_functions as gf

def run_game():

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Pokemon Invasion')

    play_button = Button(ai_settings, screen, "Play")
    hero = Hero(ai_settings, screen)
    bullets = Group()
    gotchas = Group()
    pokemons = Group()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    gf.create_fleet(ai_settings, screen, hero ,pokemons)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, hero, pokemons, bullets, gotchas)

        if stats.game_active:
            hero.update()
            gf.update_bullets(ai_settings, screen,  stats, sb, hero, pokemons, bullets, gotchas)
            gf.update_pokemons(ai_settings, screen, stats, sb, hero, pokemons, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, hero, pokemons,  bullets, play_button, gotchas)

run_game()