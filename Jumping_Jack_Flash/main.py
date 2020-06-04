# "Jumping Jack Flash" a Platformer by OverDEdge
# Game art by: https://opengameart.org/users/kenney
# Sound by: https://opengameart.org/users/dklon
# 'rpgcasaibgm.ogg' by https://opengameart.org/users/tozan
# 'Background Music 2.gg' by https://opengameart.org/users/bonobogames
# 'little town - orchestral.ogg' by https://opengameart.org/users/bart

import pygame as pg
import random
from .sprites import Player, Mob, Platform, Spritesheet, Planet
from .settings import *
from os import path
from os import environ

class Game:
    def __init__(self):
        # Intialize game window, etc...
        self.running_program = True
        environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X, WINDOW_Y)
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # Load High Score
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # Load spritesheet images
        self.player_spritesheet = Spritesheet(path.join(self.img_dir, PLAYER_SPRITESHEET), *PLAYER_SCALE)
        self.tiles_spritesheet = Spritesheet(path.join(self.img_dir, TILES_SPRITESHEET), *PLATFORMS_SCALE)
        self.enemy1_spritesheet = Spritesheet(path.join(self.img_dir, ENEMY1_SPRITESHEET), *ENEMY1_SCALE)

        # Load Sound
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, JUMP_SOUND))
        self.jump_sound.set_volume(0.1)

        # Planet images
        self.planet_images = []
        for i in range(1, 19):
            image = pg.image.load(path.join(self.img_dir, PLANET_IMAGE_NAME.format(i)))
            self.planet_images.append(pg.transform.scale(image, (PLANET_WIDTH, PLANET_HEIGHT)))


        # Load background
        self.bg_image = pg.image.load(path.join(self.img_dir, 'backgroundSpace.png'))
        self.bg_image = pg.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect = self.bg_rect.move((0, 0))

    def new(self):
        # Setup for a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.planets = pg.sprite.Group()
        self.player = Player(self, PLAYER_START_POS[0], PLAYER_START_POS[1])
        self.spawn_start_platforms()
        # Open Music for Game
        pg.mixer.music.load(path.join(self.snd_dir, BG_GAME_SOUND))
        pg.mixer.music.set_volume(0.2)
        # Start game
        self.run()

    def spawn_start_platforms(self):
        for platform in PLATFORM_LIST:
            self.spawn_platforms(platform)

    def spawn_platforms(self, platform):
        # Platforms are handled differently to check if new platform collides with existing list before adding it to group.
        if self.score < SLIME_MID_SCORE:
            slime_spawn_rate = SLIME_EASY_SPAWN_PCT
        elif self.score < SLIME_HARD_SCORE:
             slime_spawn_rate = SLIME_MID_SPAWN_PCT
        else:
            slime_spawn_rate = SLIME_HARD_SPAWN_PCT
        p = Platform(self, *platform, slime_spawn_rate)
        self.all_sprites.add(p)
        # Check if new platform collides with existing platform or mob
        hits_plat = pg.sprite.spritecollide(p, self.platforms, False)
        hits_mob = pg.sprite.spritecollide(p, self.mobs, False)
        if hits_plat or hits_mob:
            p.kill()
        else:
            p._layer = PLATFORM_LAYER
            self.platforms.add(p)

    def update(self):
        # Game Loop - update
        self.all_sprites.update()

        # If player reaches top 1/4 of the screen
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(PLANET_SPAWN_RATE) < 1:
                Planet(self)
            for planet in self.planets:
                planet.rect.y += max(abs(self.player.vel.y), 1)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for platform in self.platforms:
                platform.rect.y += max(abs(self.player.vel.y), 2)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.score += 10
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)

        enemy_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if enemy_hits:
            self.playing = False

        # Player Dies
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Spawn next platform to keep same amount of platforms
        while len(self.platforms) < len(PLATFORM_LIST) + 2 and self.player.rect.bottom <= HEIGHT:
            posx = random.randrange(0, WIDTH - 200)
            posy = random.randrange(-100, -50)
            self.spawn_platforms((posx, posy))

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

        # Fade out music at end of game
        pg.mixer.music.fadeout(FADEOUT)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.bg_image, self.bg_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 35, WHITE, WIDTH / 2, 30)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def launch_start_screen(self):
        # Open Music for Start Screen
        pg.mixer.music.load(path.join(self.snd_dir, BG_START_SOUND))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = -1)
        # Start screen
        self.screen.blit(self.bg_image, self.bg_rect)
        self.draw_text(TITLE, 120, YELLOW, WIDTH / 2, HEIGHT / 4 + 30)
        self.draw_text(INSTRUCTIONS_ARROWS, 30, WHITE, WIDTH / 2, HEIGHT *3 / 4 - 100)
        self.draw_text(INSTRUCTIONS_SPACE, 30, WHITE, WIDTH / 2, HEIGHT *3 / 4 - 50)
        self.draw_text(PRESS_TO_PLAY, 30, GREEN, WIDTH / 2, HEIGHT - 100)
        self.draw_text(HIGH_SCORE_TEXT + str(self.highscore), 50, RED, WIDTH / 2, 50)
        pg.display.flip()
        self.wait_for_key()

        # Fade out music at end of start screen
        pg.mixer.music.fadeout(FADEOUT)

    def launch_go_screen(self):
        # Open Music for Game Over Screen
        pg.mixer.music.load(path.join(self.snd_dir, BG_END_SOUND))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = -1)
        # Game Over screen
        self.screen.blit(self.bg_image, self.bg_rect)
        if self.score > self.highscore:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = self.score
                f.write(str(self.score))
            self.draw_text(NEW_HIGHSCORE_TEXT + str(self.score), 50, RED, WIDTH / 2, HEIGHT / 2)
        else:
            self.draw_text(SCORE_TEXT + str(self.score), 50, YELLOW, WIDTH / 2, HEIGHT / 2)
            self.draw_text(HIGH_SCORE_TEXT + str(self.highscore), 30, RED, WIDTH / 2, HEIGHT / 2 + 100)

        self.draw_text(GAME_OVER_TEXT, 100, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(PRESS_TO_PLAY_AGAIN, 35, GREEN, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

        # Fade out music at end of game over screen
        pg.mixer.music.fadeout(FADEOUT)

    # Waiting for any key input
    def wait_for_key(self):
        waiting = True
        key_down = False
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.KEYDOWN:
                    key_down = True
                if event.type == pg.KEYUP and key_down:
                    waiting = False

    def quit(self):
        pg.quit()
        exit()

g = Game()

while g.running_program:
    g.launch_start_screen()
    g.new()
    g.launch_go_screen()

pg.quit()
exit()
