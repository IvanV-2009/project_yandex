import pygame
import json

from blocks import *
from player import *
from Enemies import *
from Guns import *

WIDTH, HEIGHT = 500, 320

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

assets = {'Block': load_images('blocks/platforms/'),
          'decor': load_images('blocks/decorations/')}


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


def generate_level(file_name):
    with open('data/levels/' + file_name) as f:
        level = json.load(f)
    player = None
    for i in level:
        tile = level[i]
        if tile['type'] == 'Block':
            Block(tile['pos'][0], tile['pos'][1], assets[tile['type']][tile['variant']])
        if tile['type'] == 'decor':
            Decoration(tile['pos'][0], tile['pos'][1], assets[tile['type']][tile['variant']])
        if tile['type'] == 'player':
            player = Player(tile['pos'][0] * BLOCK_WIDTH, tile['pos'][1] * BLOCK_HEIGHT)
    # if tile['type'] == 'robot':
    #   Robot(tile['pos'][0] * BLOCK_WIDTH, tile['pos'][1] * BLOCK_HEIGHT)
    return player


player = generate_level('map_test.json')
healthbar = HealBar(10, 10, 80, 20, player)
camera = Camera()
gun = Pistol('10.png', 80)
bullets = []


def main():
    running = True
    clock = pygame.time.Clock()
    fps = 60
    movement = [0, 0]
    while running:
        screen.fill((255, 255, 255))
        background_images = load_images('backgrounds')
        for im in background_images:
            screen.blit(im, (0, 0))
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
                    gun.shoot(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2,
                              ["RIGHT", 'LEFT'][player.direction == -1])
                if e.key == pygame.K_2:
                    for enemy in enemises_sprites:
                        if type(enemy) == Robot:
                            enemy.blast()

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
        entities_sprites.draw(screen)
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
