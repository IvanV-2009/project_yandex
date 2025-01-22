import pygame

from blocks import *
from player import *

WIDTH, HEIGHT = 500, 500


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Spike(x, y)
            elif level[y][x] == '-':
                Block(x, y, 'grass')
            elif level[y][x] == '0':
                Changer_levels(x, y)
            elif level[y][x] == 'G':
                Disappearing_Block(x, y)
            elif level[y][x] == 'M':
                Moving_Block(x, y, 0, 0, 2, 30)
    return x, y


all_sprites = pygame.sprite.Group()
level_x, level_y = generate_level(load_level('level1.txt'))
player = Player(50, 50)
camera = Camera()
all_sprites.add(entities_sprites)
all_sprites.add(sprite_blocks)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    clock = pygame.time.Clock()
    fps = 60
    movement = (0, 0)
    player_up, player_left, player_right = False, False, False
    while running:
        screen.fill((255, 255, 255))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    player_left = True
                if e.key == pygame.K_RIGHT:
                    player_right = True
                if e.key == pygame.K_UP:
                    player_up = True
                if e.key == pygame.K_LSHIFT:
                    player.dash(sprite_blocks)

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    player_left = False
                if e.key == pygame.K_RIGHT:
                    player_right = False
                if e.key == pygame.K_UP:
                    player_up = False

        clock.tick(fps)
        camera.update(player)
        for i in all_sprites:
            camera.apply(i)
        entities_sprites.draw(screen)
        sprite_blocks.draw(screen)
        sprite_blocks.update()
        player.update(player_left, player_right, player_up, sprite_blocks)
        pygame.display.flip()
    pygame.quit()


main()
