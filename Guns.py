import pygame

from utilits import *

BULLET_SPEED = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_type, bullet_damage):
        super().__init__(bullets_group)
        self.image = load_image('bullets/' + bullet_type)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.damage = bullet_damage
        self.direction = direction

    def update(self, entites):
        if self.direction == 'UP':
            self.rect.y -= BULLET_SPEED
        elif self.direction == 'DOWN':
            self.rect.y += BULLET_SPEED
        elif self.direction == 'LEFT':
            self.rect.x -= BULLET_SPEED
        elif self.direction == 'RIGHT':
            self.rect.x += BULLET_SPEED

        for entity in entites:
            if pygame.sprite.collide_rect(self, entity):
                entity.hit(self.damage)
                self.kill()
                break


class Pistol:
    def __init__(self, bullet_type, bullet_damage):
        self.bullet_type = bullet_type
        self.bullet_damage = bullet_damage

    def shoot(self, x, y, direction):
        return Bullet(x, y, direction, self.bullet_type, self.bullet_damage)


bullets_group = pygame.sprite.Group()
