import pygame

from entities import *
from player import *
from Guns import Bullet
from utilits import *


class Enemy(PhysicsEntity):
    def __init__(self, x, y, enemy_type, point1, point2, player):
        super().__init__(x, y, enemy_type)
        enemises_sprites.add(self)
        self.point1 = point1
        self.point2 = point2
        self.player = player
        self.damage = 50
        self.velocity = [3, 0]
        self.r = 0
        self.health = 500
        self.range_of_seeing_zone = 240

    def update(self, blocks, screen, movement=(0, 0)):
        super().update(blocks, screen, movement)

        if self.act != 'shoting' and not self.velocity[0]:
            self.velocity[0] = 3 * self.direction

        if self.collisions['right'] or self.collisions['left'] or self.r >= self.point1 or self.r <= -self.point2:
            self.velocity[0] = -self.velocity[0]

        self.image = pygame.transform.flip(self.animation.image, self.direction == -1, False)

        self.r += self.velocity[0]

        if pygame.sprite.collide_rect(self, self.player) and not self.player.invincible_frames and not self.dead:
            self.player.hit(self.damage)

        if self.dead:
            sounds['entity_death'].play()

    def zone_of_seeing(self, screen):
        if self.player.dead:
            return False

        if self.direction == -1:
            if self.hit_boxses_visable:
                pygame.draw.rect(screen, 'green', (
                    (self.rect.x - self.range_of_seeing_zone, self.rect.y),
                    (self.range_of_seeing_zone, self.rect.height)),
                                 width=1)
            if (self.rect.x - self.range_of_seeing_zone < self.player.rect.x + self.player.rect.width < self.rect.x
                    and self.rect.y <= self.player.rect.y + self.player.rect.height and self.player.rect.y <= self.rect.y + self.rect.height):
                return True
        if self.direction == 1:
            if self.hit_boxses_visable:
                pygame.draw.rect(screen, 'green', ((self.rect.x + self.rect.width, self.rect.y),
                                                   (self.range_of_seeing_zone, self.rect.height)), width=1)
            if (
                    self.rect.x + self.rect.width + self.range_of_seeing_zone > self.player.rect.x > self.rect.x + self.rect.width
                    and self.rect.y <= self.player.rect.y + self.player.rect.height and self.player.rect.y <= self.rect.y + self.rect.height):
                return True
        return False



class Robot(Enemy):
    def __init__(self, x, y, player, point1=50, point2=50):
        super().__init__(x, y, 'robot', point1, point2, player)

    def blast(self):
        sounds['laser_shot'].play()
        Bullet(self.rect.x, self.rect.y + self.rect.height // 2 - 10, ['LEFT', "RIGHT"][self.direction == 1],
               'laser.png',
               40, self)

    def update(self, blocks, screen, movement=(0, 0)):
        super().update(blocks, screen, movement)

        if self.act == 'shoting' and self.check_end_of_animation():
            self.blast()

        if self.zone_of_seeing(screen):
            self.attack()

    def attack(self):
        self.act = 'shoting'
        self.velocity[0] = 0


enemises_sprites = pygame.sprite.Group()
