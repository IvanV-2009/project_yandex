import pygame


class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, entity_type):
        super().__init__(entities_sprites)
        self.image = pygame.image.load(entity_type)
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

        self.yvel = 0
        self.onGround = False
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.velocity = [0, 0]

    def update(self, blocks, movement=(0, 0)):
        motion = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        self.rect.x += motion[0]
        for block in blocks:
            if pygame.sprite.collide_rect(self, block):
                if motion[0] > 0:
                    self.collisions['right'] = True
                    self.rect.right = block.rect.left
                if motion[0] < 0:
                    self.collisions['left'] = True
                    self.rect.left = block.rect.right

        self.rect.y += motion[1]
        for block in blocks:
            if pygame.sprite.collide_rect(self, block):
                if motion[1] > 0:
                    self.collisions['down'] = True
                    self.rect.bottom = block.rect.top
                if motion[1] < 0:
                    self.collisions['up'] = True
                    self.rect.top = block.rect.bottom

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0


entities_sprites = pygame.sprite.Group()
