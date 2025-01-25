import pygame

from blocks import *
from entities import *
from Screens import *

GRAVITY = 0.75

CELL_SIZE = 30

cooldown_tracker = 0


class Player(PhysicsEntity):
    def __init__(self, x, y):
        super().__init__(x, y, 'player')
        self.xvel = 0
        self.jump_strenght = 15
        self.gravitation = GRAVITY
        self.slide = False
        self.jumps = 0
        self.run = False
        self.invincible_frames = 0

    def jump(self):
        if self.collisions['down']:
            self.velocity[1] = -self.jump_strenght

    def update(self, blocks, movement):
        super().update(blocks, movement)

        if self.run:
            if self.direction == 1:
                self.velocity[0] = min(2, self.velocity[0] + 0.1)
            else:
                self.velocity[0] = max(-2, self.velocity[0] - 0.1)
        else:
            if self.direction == 1:
                self.velocity[0] = max(0, self.velocity[0] - 0.1)
            else:
                self.velocity[0] = min(0, self.velocity[0] + 0.1)

        if self.invincible_frames:
            self.invincible_frames -= 1

        self.check_status()

    def running(self, k):
        self.run = k

    def check_status(self):
        if self.health <= 0:
            self.die()

    def hit(self, damage):
        super().hit(damage)
        self.invincible_frames = 20
