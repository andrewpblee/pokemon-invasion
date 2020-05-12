class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.bullet_ammo = 6
        self.fleet_drop_speed = 5
        self.lives_limit = 3
        # how fast the does the game speeds up
        self.speedup_scale = 1.05
        self.level_speedup_scale = 1.01
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.hero_speed_factor = 5
        self.bullet_speed_factor = 8
        self.pokemon_speed_factor = 1
        self.fleet_direction = 1
        self.pokemon_points = 50

    def increase_speed(self):
        self.hero_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.pokemon_speed_factor *= self.speedup_scale
        self.pokemon_points = int(self.pokemon_points * self.score_scale)

    def increase_level_speed(self):
        self.pokemon_speed_factor *= self.level_speedup_scale