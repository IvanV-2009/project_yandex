import pygame

from utilits import *

BULLET_SPEED = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_type, bullet_damage, shooter):
        super().__init__(bullets_group, all_sprites)
        self.image = load_image('bullets/' + bullet_type)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.damage = bullet_damage
        self.direction = direction
        self.shooter = shooter
        self.life_time = 400

    def update(self, entites, blocks):
        if self.direction == 'UP':
            self.rect.y -= BULLET_SPEED
        elif self.direction == 'DOWN':
            self.rect.y += BULLET_SPEED
        elif self.direction == 'LEFT':
            self.rect.x -= BULLET_SPEED
        elif self.direction == 'RIGHT':
            self.rect.x += BULLET_SPEED

        for entity in entites:
            if type(self.shooter) != type(entity) and pygame.sprite.collide_rect(self, entity):
                entity.hit(self.damage)
                self.kill()
                break

        for block in blocks:
            if pygame.sprite.collide_rect(self, block) and block.__class__.__name__ == 'Block':
                self.kill()
                break

        self.life_time -= 1

        if self.life_time <= 0:
            self.kill()


class Pistol:
    def __init__(self, bullet_type, bullet_damage, player):
        self.bullet_type = bullet_type
        self.bullet_damage = bullet_damage
        self.player = player

    def shoot(self):
        Bullet(self.player.rect.x + self.player.rect.width * self.player.direction,
               self.player.rect.y + self.player.rect.height // 2,
               ['RIGHT', 'LEFT'][self.player.direction == -1], self.bullet_type, self.bullet_damage, self.player)
        sounds['bulletshot'].play()


bullets_group = pygame.sprite.Group()
