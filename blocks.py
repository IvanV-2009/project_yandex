import pygame
from utilits import *

blocks = {'grass': 'data/blocks/1.png', 'spike': 'data/blocks/spike.png', 'empty': 'data/blocks/empty.png'}

BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32

pygame.init()


class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, decor_image):
        super().__init__(all_sprites)
        self.image = decor_image
        self.rect = self.image.get_rect().move(BLOCK_WIDTH * x, BLOCK_HEIGHT * y)
        self.mask = pygame.mask.from_surface(self.image)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_image):
        super().__init__(sprite_blocks, all_sprites)
        self.image = block_image
        self.rect = self.image.get_rect().move(BLOCK_WIDTH * x, BLOCK_HEIGHT * y)
        self.mask = pygame.mask.from_surface(self.image)

    def act(self, entity):
        pass


class Spike(Block):
    def __init__(self, x, y):
        super().__init__(x, y, load_image('blocks/special_blocks/spike.png'))

    def act(self, entity):
        if entity.__class__.__name__ == 'Player':
            entity.hit(40)


class Chest(Block):
    pass


class Key(Block):
    def __init__(self, x, y):
        super().__init__(x, y, load_image('blocks/special_blocks/key.png'))

    def act(self, entity):
        if entity.__class__.__name__ == 'Player':
            entity.get_key = True
            sounds['collect'].play()
            self.kill()


class Disappearing_Block(Block):
    def __init__(self, x, y):
        super().__init__(x, y, load_image('blocks/platforms/Tile_29.png'))
        self.timer = 0

    def disappear(self):
        if self.timer > 500:
            self.kill()
        else:
            self.timer += 5

    def act(self, entity):
        self.disappear()


class Trampoline(Block):
    pass


class Moving_Block(Block):
    def __init__(self, x, y, speed, distance):
        super().__init__(x, y, pygame.image.load('data/blocks/1.png'))
        self.speed = speed
        self.distance = distance
        self.r = 0

    def update(self):
        if abs(self.r) >= self.distance:
            self.speed = -self.speed
        self.rect = self.rect.move(self.speed, 0)
        self.r += self.speed

    def act(self, entity):
        entity.rect.x += self.speed


class HealPotion(Block):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load('data/blocks/special_blocks/healing_potion.png'))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect().move(x * BLOCK_WIDTH, y * BLOCK_HEIGHT)

    def act(self, entity):
        if entity.__class__.__name__ == 'Player':
            entity.health += 50
            self.kill()
            sounds['collect'].play()


class Coin(Block):
    def __init__(self, x, y):
        super().__init__(x, y, load_image('blocks/special_blocks/coin.png'))

    def act(self, entity):
        if entity.__class__.__name__ == 'Player':
            global SCORE
            SCORE += 100
            self.kill()


sprite_blocks = pygame.sprite.Group()
spikes_sprites = pygame.sprite.Group()
