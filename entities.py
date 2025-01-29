import pygame
from utilits import *
from blocks import *

GRAVITY = 0.75


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, entity_type):
        super().__init__(entities_sprites, all_sprites)
        self.start_x = x
        self.start_y = y
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.velocity = [0, 0]
        self.previous_direction = 1
        self.direction = 1
        self.previous_act = 'idle'
        self.act = self.previous_act
        self.animation = animations[entity_type + '/' + self.act].copy()
        self.jump_state = False
        self.image = self.animation.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.gravitation = GRAVITY
        self.entity_type = entity_type
        self.health = 300
        self.invincible_frames = 0
        self.dead = False
        self.previous_rect = self.rect.copy()
        self.c = 0

    def update(self, blocks, movement=(0, 0)):

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        motion = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        self.rect.x += motion[0]
        for block in blocks:
            if pygame.sprite.collide_rect(self, block):
                if motion[0] > 0:
                    self.collisions['right'] = True
                    self.rect.right = block.rect.left
                if motion[0] < 0:
                    self.collisions['left'] = True
                    self.rect.left = block.rect.right

        self.rect.y += motion[1]
        for block in blocks:
            if pygame.sprite.collide_rect(self, block):
                block.act(self)
                if motion[1] >= 0:
                    self.collisions['down'] = True
                    self.rect.bottom = block.rect.top
                if motion[1] < 0:
                    self.collisions['up'] = True
                    self.rect.top = block.rect.bottom

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        self.velocity[1] = min(self.gravitation + self.velocity[1], 9)

        if motion[0] > 0:
            self.direction = 1
        if motion[0] < 0:
            self.direction = -1

        if motion[1] < 0:
            self.jump_state = True
        if self.collisions['down']:
            self.jump_state = False

        if self.dead:
            self.act = 'death'
        elif self.invincible_frames:
            self.act = 'hurt'
        elif self.jump_state:
            self.act = 'jump'
        elif motion[0]:
            if self.act == 'attack':
                self.act += '_run'
            else:
                self.act = 'run'
        else:
            self.act = 'idle'

        if self.previous_act != self.act:
            self.previous_act = self.act
            self.animation = animations[self.entity_type + '/' + self.act].copy()
            self.image = self.animation.image
            self.rect = self.image.get_rect(center=self.rect.center).move(0, (
                        self.image.get_rect().height - self.rect.height) // 2 * [1, -1][
                                                                              self.rect.height < self.image.get_rect().height])

        self.image = pygame.transform.flip(self.animation.image, self.direction == -1, False)

        if self.invincible_frames:
            self.invincible_frames -= 1

        if self.dead and self.check_end_of_animation():
            self.kill()

        self.animation.update()
        self.check_status()

    def die(self):
        self.act = 'death'
        self.dead = True
        self.velocity = [0, 0]

    def attack(self):
        self.act = 'attack'

    def hit(self, damage):
        self.health -= damage
        self.act = 'hurt'
        self.invincible_frames = 20

    def check_status(self):
        if self.health <= 0:
            self.die()

    def check_end_of_animation(self):
        if self.animation.image == self.animation.frames[-1]:
            return True
        return False


entities_sprites = pygame.sprite.Group()
