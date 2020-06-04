import pygame as pg
from .settings import *
import math
import random

def check_for_collide(sprite, group, dir):
    # Check for collide in each direction
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # If collision has occured, update position and set velocity and acceleration = 0
        if hits:
            if sprite.rect.left - sprite.width * (1 - HIT_RECT) / 2 < hits[0].rect.right and sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.width / 2 - sprite.width * (1 - HIT_RECT) / 2
            if sprite.rect.right + sprite.width * (1 - HIT_RECT) / 2 > hits[0].rect.left and sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.width / 2  + sprite.width * (1 - HIT_RECT) / 2
            sprite.vel.x = 0
            sprite.acc.x = 0
        sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # If collision has occured, update position and set velocity and acceleration = 0
        if hits:
            if sprite.rect.top < hits[0].rect.bottom and sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.height

            if sprite.rect.bottom > hits[0].rect.top and sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top
            sprite.vel.y = 0
            sprite.acc.y = 0
        sprite.rect.bottom = sprite.pos.y

def collide_hit_rect(one, two):
    one.hit_rect = pg.Rect(0, 0, one.width * HIT_RECT, one.height)
    one.hit_rect.midbottom = one.pos
    return one.hit_rect.colliderect(two.rect)

def animate_moving(sprite, images, switch):
    img_time = pg.time.get_ticks()
    # If switching between states that have different image update rate
    # E.g. switching between walking, standing and jumping. Then immedietly
    # switch image.
    if switch != sprite.update_rate:
            sprite.update_rate = switch
            sprite.last_update = 0
    # If requested time has elapsed update animating image
    if (img_time - sprite.last_update) > switch:
        sprite.current_frame = (sprite.current_frame + 1) % len(images)
        image = images[sprite.current_frame]
        sprite.last_update = img_time
        sprite.non_flipped_image = image

    # Depending on direction, flip image
    if sprite.direction > 0:
        sprite.image = sprite.non_flipped_image
    else:
        sprite.image = pg.transform.flip(sprite.non_flipped_image, True, False)

    sprite.width, sprite.height = sprite.image.get_size()

def load_images(sprite, spritesheet, stand, move, jump):
    # Load images for all states: walking, standing and jumping
    sprite.move_images = []
    sprite.stand_images = []
    sprite.jump_images = []
    for location in move:
        image = spritesheet.get_image(*location)
        image.set_colorkey(BLACK)
        sprite.move_images.append(image)
    for location in stand:
        image = spritesheet.get_image(*location)
        image.set_colorkey(BLACK)
        sprite.stand_images.append(image)
    for location in jump:
        image = spritesheet.get_image(*location)
        image.set_colorkey(BLACK)
        sprite.jump_images.append(image)



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        load_images(self, self.game.player_spritesheet, PLAYER_STAND_IMAGES, PLAYER_WALK_IMAGES, PLAYER_JUMP_IMAGES)
        # Set initial image and rectangle values based on image
        self.image = self.stand_images[0]
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = 1
        self.all_direction = 0
        self.current_frame = 0
        self.last_update = 0
        self.update_rate = SWITCH_PLAYER_STANDING_IMAGE
        self.jumping = False
        self.jump_again = False
        self.walking = False
        self.non_flipped_image = self.image

    def update(self):
        # Update position
        self.movement()

    def standing_on_platform(self):
        # Check if standing on platform by checking a few pixels below.
        self.rect.y += 3
        self.pos.y += 3
        hits = pg.sprite.spritecollide(self, self.game.platforms, False, collide_hit_rect)
        self.rect.y -= 3
        self.pos.y -= 3
        if hits:
            return True
        return False

    def movement(self):
        # Get input to do Player movement
        self.acc = vec(0, PLAYER_GRAVITY)
        self.standing = True
        self.walking = False

        # Check pressed keys and update direction of player
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_RUN
            self.standing = False
            self.direction = -1
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_RUN
            self.standing = False
            self.direction = 1
        # If holding Space while jumping reduce gravity until a certain point in jump
        if (keys[pg.K_SPACE] or keys[pg.K_UP]) and self.vel.y < PLAYER_JUMP_LIMIT:
            self.acc.y -= PLAYER_JUMP_FORCE

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # Equations of Motion x
        self.vel.x += self.acc.x
        self.pos.x += self.vel.x + 0.5 * self.acc.x

        # Wrap around
        if self.pos.x > WIDTH + self.width / 2:
            self.pos.x = -self.width / 2
        elif self.pos.x < -self.width / 2:
            self.pos.x = WIDTH + self.width / 2

        # Check for collision in x
        self.rect.centerx = self.pos.x
        check_for_collide(self, self.game.platforms, 'x')

        # Equations of Motion y
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y

        # Check for collision in y
        self.rect.bottom = self.pos.y
        check_for_collide(self, self.game.platforms, 'y')

        # Check if standing on platform, then remove gravity
        if self.standing_on_platform():
            self.acc.y = 0
            # If standing on platform and arrow key pressed then player is walking
            if not self.standing:
                self.walking = True

        # Animate moving only when standing on platform
        if self.standing_on_platform():
            self.jumping = False
            self.jump_again = True
            if self.walking:
                animate_moving(self, self.move_images, SWITCH_PLAYER_WALKING_IMAGE)
            else:
                animate_moving(self, self.stand_images, SWITCH_PLAYER_STANDING_IMAGE)

        # If jumping set jumping image
        if self.jumping:
            animate_moving(self, self.jump_images, SWITCH_PLAYER_WALKING_IMAGE)

        self.rect = self.non_flipped_image.get_rect()
        self.rect.midbottom = self.pos

    def jump(self):
        # Jump only if standing on something
        if self.standing_on_platform() or self.jump_again:
            self.game.jump_sound.play()
            if self.jumping:
                self.jump_again = False
            self.jumping = True
            self.vel.y = PLAYER_JUMP_SPEED

class Mob(pg.sprite.Sprite):
    def __init__(self, game, spritesheet, stand_image_locations, move_image_locations, jump_image_locations, update_rate):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        load_images(self, spritesheet, stand_image_locations, move_image_locations, jump_image_locations)
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.direction = 0
        self.last_update = 0
        self.current_frame = 0
        self.update_rate = update_rate

        def update(self):
            pass

class SlidingMob(Mob):
    def __init__(self, game, platform):
        super().__init__(game, game.enemy1_spritesheet, [], SLIME_MOVE_IMAGES, [], SWITCH_SLIME_MOVING_IMAGE)
        self.image = self.move_images[0]
        self.non_flipped_image = self.image
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.platform = platform
        self.pos = vec(self.platform.rect.centerx, self.platform.rect.top)
        self.rect.midbottom = self.pos
        self.vel = vec(-SLIME_SPEED, 0)
        self.direction = 1
        self.platform_last_pos = self.platform.start_posx

    def update(self):

        animate_moving(self, self.move_images, self.update_rate)
        self.rect = self.non_flipped_image.get_rect()
        # Adjust x position to slime velocity and if platform is moving
        self.pos.x += self.vel.x
        platform_moved = self.platform.rect.x - self.platform_last_pos
        if platform_moved >= 1:
            self.pos.x += platform_moved
            self.platform_last_pos = self.platform.rect.x
        if self.pos.x - self.width / 2 < self.platform.rect.left + 2:
            self.vel.x = SLIME_SPEED
            self.direction = -1
        elif self.pos.x + self.width / 2 > self.platform.rect.right - 2:
            self.vel.x = -SLIME_SPEED
            self.direction = 1
        self.rect.centerx = self.pos.x
        self.rect.bottom = self.platform.rect.top
        if not self.game.platforms.has(self.platform):
            self.kill()

        # Depending on direction, flip image
        if self.direction > 0:
            self.image = self.non_flipped_image
        else:
            self.image = pg.transform.flip(self.non_flipped_image, True, False)

        self.width, self.height = self.image.get_size()


class Platform (pg.sprite.Sprite):
    def __init__(self, game, x, y, slime_spawn_rate):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        location = random.choice(TILES_PLATFORM_IMAGES)
        self.image = self.game.tiles_spritesheet.get_image(*location)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.enemy = False
        self.platform_speed = random.choice(PLATFORM_SPEED)
        self.platform_update = 0
        self.start_posx = x
        rand_direction = random.randrange(101)
        direction = -1
        if rand_direction < NOT_MOVING_PLATFORMS:
            direction = 0
        elif rand_direction < SLOW_MOVING_PLATFORMS + NOT_MOVING_PLATFORMS:
            direction = 1

        self.velx = self.platform_speed * direction
        if random.randrange(100) < slime_spawn_rate and len(self.game.platforms) > 0:
            SlidingMob(self.game, self)
            self.enemy = True

    def update(self):
        now = pg.time.get_ticks()
        if now - self.platform_update > PLATFORM_X_UPDATE:
            self.rect.x += self.velx
            self.platform_update = now
        if self.rect.x >= self.start_posx + PLATFORM_MOVE:
            self.velx = -self.platform_speed
        if self.rect.x <= self.start_posx - PLATFORM_MOVE:
            self.velx = self.platform_speed

class Spritesheet:
    # Utility class for loading and parsing spritessheets
    def __init__(self, filename, scale_x, scale_y):
        self.spritesheet = pg.image.load(filename).convert()
        self.scale_x = scale_x
        self.scale_y = scale_y

    def get_image(self, x, y, width, height):
        # Grab an image out of a larger Spreadsheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // self.scale_x, height // self.scale_y))
        return image

class Pow (pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        location = random.choice(TILES_PLATFORM_IMAGES)
        self.image = self.game.tiles_spritesheet.get_image(*location)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Planet(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLANET_LAYER
        self.groups = game.all_sprites, game.planets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = random.choice(self.game.planet_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-1000, -400)
        self.vel = vec(PLANET_SPEED, 0)
        self.direction = random.choice([1, -1])
        self.update_rate = 0

    def update(self):
        now = pg.time.get_ticks()
        if now - self.update_rate > PLANET_UPDATE_RATE:
            self.update_rate = now
            self.rect.x += self.vel.x * self.direction
        if self.rect.top > HEIGHT:
            self.kill()
