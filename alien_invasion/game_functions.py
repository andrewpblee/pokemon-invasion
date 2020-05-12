import sys
import pygame
from bullet import Bullet
from pokemon import Pokemon
from gotcha import Gotcha
from time import sleep


def check_keydown_events(event, ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas):
    if event.key == pygame.K_RIGHT:
        hero.moving_right = True
    elif event.key == pygame.K_LEFT:
        hero.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, hero, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas)


def fire_bullet(ai_settings, screen, hero, bullets):
    if len(bullets) < ai_settings.bullet_ammo:
        new_bullet = Bullet(ai_settings, screen, hero)
        bullets.add(new_bullet)


def create_gotcha(pokemon_x, pokemon_y, screen, gotchas):
    new_gotcha = Gotcha(screen, pokemon_x, pokemon_y)
    gotchas.add(new_gotcha)



def check_keyup_events(event, hero):
    if event.key == pygame.K_RIGHT:
        hero.moving_right = False
    elif event.key == pygame.K_LEFT:
        hero.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, hero,
                      pokemons, bullets, gotchas):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, hero)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, hero,
                      pokemons, bullets, gotchas, mouse_x, mouse_y)




def start_game(ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas):
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    sb.prep_high_score()
    sb.prep_score()
    sb.prep_level()
    sb.prep_lives()
    pokemons.empty()
    bullets.empty()
    gotchas.empty()
    create_fleet(ai_settings, screen, hero, pokemons)
    hero.center_hero()



def check_play_button(ai_settings, screen, stats, sb, play_button, hero,
                      pokemons, bullets, gotchas, mouse_x, mouse_y):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        start_game(ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas)



def update_screen(ai_settings, screen, stats, sb, hero, pokemons, bullets, play_button, gotchas):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for gotcha in gotchas.sprites():
        gotcha.draw_gotcha()

    hero.blitme()
    pokemons.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings, screen,  stats, sb, hero, pokemons, bullets, gotchas):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_pokemon_collisions(ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas)


def check_bullet_pokemon_collisions(ai_settings, screen, stats, sb, hero, pokemons, bullets, gotchas):

    collisions = pygame.sprite.groupcollide(bullets, pokemons, True, True)

    if collisions:
        for pokemons in collisions.values():
            for pokemon in pokemons:
                create_gotcha(pokemon.rect[0], pokemon.rect[1], screen, gotchas)
            stats.score += ai_settings.pokemon_points * len(pokemons)
            sb.prep_score()
        check_high_scores(stats, sb)
        ai_settings.increase_level_speed()

    if len(pokemons) == 0:
        # if all pokemon are cleared, we go up a level
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, hero, pokemons)



def get_number_rows(ai_settings, hero_height, pokemon_height):

    available_space_y = (ai_settings.screen_height -
                         (3 * pokemon_height) - hero_height)
    number_rows = int(available_space_y / (2.5 * pokemon_height))
    return number_rows


def get_number_pokemon_x(ai_settings, pokemon_width):
    available_space_x = ai_settings.screen_width - 2 * pokemon_width
    number_pokemon_x = int(available_space_x / (2 * pokemon_width))
    return number_pokemon_x


def create_pokemon(ai_settings, screen, pokemons, pokemon_number, row_number):
    pokemon = Pokemon(ai_settings, screen)
    pokemon_width = pokemon.rect.width
    pokemon.x = pokemon_width + 2 * pokemon_width * pokemon_number
    pokemon.rect.x = pokemon.x
    pokemon.rect.y = pokemon.rect.height + 2 * pokemon.rect.height * row_number
    pokemons.add(pokemon)


def create_fleet(ai_settings, screen, hero, pokemons):
    pokemon = Pokemon(ai_settings, screen)
    number_pokemon_x = get_number_pokemon_x(ai_settings, pokemon.rect.width)
    number_rows = get_number_rows(ai_settings, hero.rect.height,
                                  pokemon.rect.height)

    for row_number in range(number_rows):
        for pokemon_number in range(number_pokemon_x):
            create_pokemon(ai_settings, screen, pokemons, pokemon_number, row_number)


def check_fleet_edges(ai_settings, pokemons):
    for pokemon in pokemons.sprites():
        if pokemon.check_edges():
            change_fleet_direction(ai_settings, pokemons)
            break


def change_fleet_direction(ai_settings, pokemons):
    for pokemon in pokemons.sprites():
        pokemon.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def hero_hit(ai_settings, screen, stats, sb, hero, pokemons, bullets):
    if stats.lives_left > 0:
        stats.lives_left -= 1

        pokemons.empty()
        bullets.empty()
        sb.prep_lives()
        create_fleet(ai_settings, screen, hero, pokemons)
        hero.center_hero()
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def update_pokemons(ai_settings, screen, stats, sb, hero, pokemons, bullets):
    check_pokemons_bottom(ai_settings,screen,  stats, sb, hero, pokemons, bullets)
    check_fleet_edges(ai_settings, pokemons)

    if pygame.sprite.spritecollideany(hero, pokemons):
        hero_hit(ai_settings, screen, stats, sb, hero, pokemons, bullets)
    pokemons.update()


def check_pokemons_bottom(ai_settings, screen,stats, sb, hero, pokemons, bullets):
    screen_rect = screen.get_rect()
    for pokemon in pokemons.sprites():
        if pokemon.rect.bottom >= screen_rect.bottom:
            hero_hit(ai_settings, screen,stats, sb, hero, pokemons, bullets)


def check_high_scores(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()