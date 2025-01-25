import pygame

from blocks import *
from player import *
from Enemies import *
from Guns import *

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
                Moving_Block(x, y, 1, 20)
            elif level[y][x] == 'R':
                Enemy(x * CELL_SIZE, y * CELL_SIZE, 'robot', 500, 500, player)
                pass
    return x, y


player = Player(50, 50)
level_x, level_y = generate_level(load_level('level1.txt'))
healthbar = HealBar(10, 10, 80, 20, player)
camera = Camera()
gun = Pistol()
bullets = []


def main():
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT, 100)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    clock = pygame.time.Clock()
    fps = 60
    movement = [0, 0]
    while running:
        screen.fill((255, 255, 255))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    movement[0] -= 5
                if e.key == pygame.K_RIGHT:
                    movement[0] += 5
                if e.key == pygame.K_UP:
                    player.jump()
                if e.key == pygame.K_LSHIFT:
                    player.running(True)
                if e.key == pygame.K_1:
                    print(1)
                    player.die()
                if e.key == pygame.K_d:
                    gun.shoot(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2, 'RIGHT')

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    movement[0] += 5
                if e.key == pygame.K_RIGHT:
                    movement[0] -= 5
                if e.key == pygame.K_LSHIFT:
                    player.running(False)

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    player.attack()
        clock.tick(fps)
        camera.update(player)
        for i in all_sprites:
            camera.apply(i)
        all_sprites.draw(screen)
        player.update(sprite_blocks, movement)
        enemises_sprites.update(sprite_blocks, (0, 0))
        healthbar.draw(screen)
        healthbar.update_health()
        bullets_group.draw(screen)
        bullets_group.update(entities_sprites)
        sprite_blocks.update()
        pygame.display.flip()
    pygame.quit()


main()
