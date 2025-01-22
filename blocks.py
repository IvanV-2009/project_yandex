import pygame

blocks = {'grass': 'data/blocks/1.png',
          'spike': 'data/blocks/spike.png',
          'empty': 'data/blocks/empty.png'}

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 30


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super().__init__(sprite_blocks)
        self.image = pygame.image.load(blocks[block_type])
        self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect().move(BLOCK_WIDTH * x, BLOCK_HEIGHT * y)
        self.mask = pygame.mask.from_surface(self.image)


class Spike(Block):
    def __init__(self, x, y):
        super().__init__(x, y, 'spike')


class Changer_levels(Block):
    def __init__(self, x, y):
        super().__init__(x, y, 'empty')


class Chest(Block):
    pass


class Key(Block):
    def __init__(self, x, y):
        super().__init__(x, y, 'key')


class Disappearing_Block(Block):
    def __init__(self, x, y):
        super().__init__(x, y, 'grass')
        self.timer = 0

    def disappear(self):
        if self.timer > 200:
            self.kill()
        else:
            self.timer += 5


class Death_Block(Block):
    def __init__(self, x, y):
        super().__init__(x, y, 'empty')


class Trampoline(Block):
    pass


class Moving_Block(Block):
    def __init__(self, x, y, speed_x, distance_x, speed_y, distance_y):
        super().__init__(x, y, 'grass')
        self.speed_x = speed_x
        self.distance_x = distance_x
        self.speed_y = speed_y
        self.distance_y = distance_y
        self.r = 0
        self.k = 0

    def update(self):
        if abs(self.r) >= self.distance_x:
            self.speed_x = -self.speed_x

        if abs(self.k) >= self.distance_y:
            self.speed_y = -self.speed_y

        self.rect = self.rect.move(self.speed_x, self.speed_y)
        self.r += self.speed_x
        self.k += self.speed_y


sprite_blocks = pygame.sprite.Group()
spikes_sprites = pygame.sprite.Group()
