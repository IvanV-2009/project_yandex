import pygame

from blocks import *
from entities import *
from utilits import *

GRAVITY = 0.75

CELL_SIZE = 30

cooldown_tracker = 0


class Player(PhysicsEntity):
    def __init__(self, x, y):
        super().__init__(x, y, 'player')
        self.xvel = 0
        self.jump_strenght = 17
        self.double_jump_strenght = self.jump_strenght * 0.5  # Сила второго прыжка (50% от первого)
        self.jumpscnt = 0  # Количество выполненных прыжков
        self.gravitation = GRAVITY
        self.slide = False
        self.jumps = 0
        self.run = False
        self.invincible_frames = 0
        self.get_key = False

    def jump(self):
        if self.collisions['down']:  # Первый прыжок (на земле)
            self.velocity[1] = -self.jump_strenght
            self.jumpscnt = 1  # Увеличиваем счетчик прыжков
            sounds['jump'].play()  # Воспроизведение звука прыжка
        elif self.jumpscnt == 1:  # Второй прыжок (в воздухе)
            self.velocity[1] = -self.double_jump_strenght
            self.jumpscnt = 2  # Увеличиваем счетчик прыжков
            print(1)
            self.act = 'double_jump'
            self.change_animation()
            sounds['jump'].play()
    def update(self, blocks, screen, movement):
        super().update(blocks, screen, movement)

        motion = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        if motion[0]:
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

        if self.dead:
            sounds['death'].play()

    def running(self, k):
        self.run = k

    def hit(self, damage):
        super().hit(damage)
        if self.invincible_frames:
            sounds['player_hit'].play()


class HealBar:
    def __init__(self, x, y, width, height, player):
        self.rect = pygame.Rect(x, y, width, height)
        self.player = player
        self.max_health = player.health
        self.current_health = player.health

    def update_health(self):
        self.current_health = max(0, min(self.player.health, self.max_health))

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        health_ratio = self.current_health / self.max_health
        fill_width = int(self.rect.width * health_ratio)

        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)
