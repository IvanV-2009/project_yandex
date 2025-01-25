import pygame

from entities import entities_sprites

BULLET_SPEED = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(bullets_group)
        self.image = pygame.image.load('data/bullets/10.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.damage = 10
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
    def shoot(self, x, y, direction):
        return Bullet(x, y, direction)


bullets_group = pygame.sprite.Group()
