import pygame

from entities import *
from player import *


class Enemy(PhysicsEntity):
    def __init__(self, x, y, enemy_type, point1, point2, player):
        super().__init__(x, y, enemy_type)
        enemises_sprites.add(self)
        self.point1 = point1
        self.point2 = point2
        self.player = player
        self.damage = 50
        self.velocity = [3, 0]

    def update(self, blocks, movement=(0, 0)):
        super().update(blocks, movement)

        if self.rect.x + self.rect.width >= self.point1 + self.start_x or self.rect.x <= self.start_x - self.point2 or \
                self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = - self.velocity[0]

        if pygame.sprite.collide_rect(self, self.player) and not self.player.invincible_frames:
            print(1)
            self.player.hit(self.damage)


enemises_sprites = pygame.sprite.Group()
