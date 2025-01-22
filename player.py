import pygame

from blocks import *
from entities import *

GRAVITY = 0.35

entities = {'player': 'data/entities/player.png'}
CELL_SIZE = 30

MOVE_SPEED = 8

cooldown_tracker = 0


class Player(PhysicsEntity):
    def __init__(self, x, y):
        super().__init__(x, y, entities['player'])
        self.xvel = 0
        self.jump_strenght = 10
        self.gravitation = GRAVITY
        self.slide = False
        self.speed_x = MOVE_SPEED
        self.onGround = False

    def collide_x(self, blocks):
        col = 0
        for block in blocks:
            if pygame.sprite.collide_rect(self, block):
                if self.xvel > 0:
                    self.rect.right = block.rect.left

                if self.xvel < 0:
                    self.rect.left = block.rect.right

                if not self.onGround:
                    self.slide = True
                col += 1

        if not col:
            self.slide = False

    def collide_y(self, blocks):
        for block in blocks:
            if pygame.sprite.collide_rect(self, block):
                if type(block) == Spike:
                    self.kill()
                    break

                if type(block) == Disappearing_Block:
                    block.disappear()

                if type(block) == Moving_Block:
                    self.xvel += block.speed_x

                if self.yvel > 0:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.slide = False
                    self.yvel = 0

                if self.yvel < 0:
                    self.rect.top = block.rect.bottom
                    self.gravitation = GRAVITY
                    self.yvel = 0

    def update(self, left, right, up, blocks):
        if left:
            self.xvel = -MOVE_SPEED

        if right:
            self.xvel = MOVE_SPEED

        if not (left or right):
            self.xvel = 0
        if up:
            if self.onGround:
                self.yvel = -self.jump_strenght
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide_y(blocks)

        self.rect.x += self.xvel
        self.collide_x(blocks)

    def die(self):
        self.kill()

    def dash(self, blocks):
        self.speed_x = 20
        for i in range(8):
            self.update(False, True, False, blocks)
        self.speed_x = MOVE_SPEED
