import pygame
import json
from utilits import load_images, load_image
from blocks import BLOCK_WIDTH, BLOCK_HEIGHT

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

assets = {'Block': load_images('blocks/platforms/'),
          'decor': load_images('blocks/decorations/'),
          'player': [load_image('entities/player/player.png')],
          'robot': [load_image('entities/enemies/robot/robot.png')],
          'spike': [load_image('blocks/special_blocks/spike.png')],
          'heal_potion': [load_image('blocks/special_blocks/healing_potion.png')],
          'door': [load_image('blocks/special_blocks/door.png')],
          'key': [load_image('blocks/special_blocks/key.png')],
          'disappearing_block': [load_image('blocks/platforms/Tile_29.png')],
          'gates': [load_image('blocks/special_blocks/gates.png')],
          'coin': [load_image('blocks/special_blocks/coin.png')]}

with open('map1.json', 'r') as f:
    map = json.load(f)

running = True
motion = [0, 0]
key_pressed_ticks = 0
clock = pygame.time.Clock()
var = 0
typ = 0
drawing, deleting = False, False
types = list(assets.keys())
while running:
    screen.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    curr_type = types[typ]
    x, y = (pygame.mouse.get_pos()[0] + motion[0]) // BLOCK_WIDTH, (
            pygame.mouse.get_pos()[1] + motion[1]) // BLOCK_HEIGHT
    im = assets[curr_type][var].copy()
    im.set_alpha(100)
    x += (BLOCK_WIDTH - im.get_rect().width) / BLOCK_WIDTH
    y += (BLOCK_HEIGHT - im.get_rect().height) / BLOCK_HEIGHT
    screen.blit(im, (x * BLOCK_WIDTH - motion[0],
                     y * BLOCK_HEIGHT - motion[1]))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEMOTION:
            if drawing:
                map[f'{x};{y}'] = {"type": curr_type, "variant": var, "pos": [x, y]}
            if deleting:
                if f'{x};{y}' in map:
                    map.pop(f'{x};{y}')

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_t:
                with open('map1.json', 'w') as f:
                    json.dump(map, f)
            if e.key == pygame.K_q:
                typ += 1
                typ %= len(types)
                var = 0
            if e.key == pygame.K_e:
                typ -= 1
                typ %= len(types)
                var = 0

        if e.type == pygame.MOUSEWHEEL:
            if e.y > 0:
                var += 1
            else:
                var -= 1
            var %= len(assets[curr_type])

        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                drawing = True
                map[f'{x};{y}'] = {"type": curr_type, "variant": var, "pos": [x, y]}
            if e.button == 3:
                deleting = True
                if f'{x};{y}' in map:
                    map.pop(f'{x};{y}')

        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                drawing = False
            if e.button == 3:
                deleting = False

    if keys[pygame.K_DOWN]:
        motion[1] += 15
    if keys[pygame.K_UP]:
        motion[1] -= 15
    if keys[pygame.K_RIGHT]:
        motion[0] += 15
    if keys[pygame.K_LEFT]:
        motion[0] -= 15
    for i in map:
        tile = map[i]
        screen.blit(assets[tile['type']][tile['variant']],
                    (tile['pos'][0] * BLOCK_WIDTH - motion[0],
                     tile['pos'][1] * BLOCK_HEIGHT - motion[1]))
    if key_pressed_ticks:
        key_pressed_ticks += 1
    clock.tick(60)
    pygame.display.flip()

with open('map1.json', 'w') as f:
    json.dump(map, f)
