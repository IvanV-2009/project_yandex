import os

import pygame
import json
import pygame.font

from player import *
from Enemies import *
from Guns import *

pygame.init()

WIDTH, HEIGHT = 500, 320
SETTINGS_WIDTH, SETTINGS_HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

assets = {'Block': load_images('blocks/platforms/'),
          'decor': load_images('blocks/decorations/')}

LEVEL_NUM = 0

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Шрифт
pygame.font.init()
FONT = pygame.font.Font(None, 30)  # Используем шрифт по умолчанию

# Глобальные переменные настроек (можно хранить в файле)
fullscreen = False
resolution = (800, 600)
difficulty = "Normal"
show_fps = False


# Функция для отображения текста с кнопкой
def draw_button(screen, text, x, y, width, height, color, text_color, action=None):
    """Рисует кнопку и возвращает True, если на неё нажали."""
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]  # 0 - левая кнопка мыши

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(screen, color, (x, y, width, height))  # Подсветка при наведении
        if click == 1:
            if action is not None:
                action()  # Выполнить действие, если кнопка нажата
            pygame.time.delay(200)  # Пауза, чтобы избежать множественных нажатий
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), 2)  # Просто рамка

    text_surface = FONT.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return False


# Функции для изменения настроек
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(resolution)


def change_resolution(width, height):
    global resolution
    resolution = (width, height)
    if fullscreen:
        pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(resolution)


def set_800x600():
    change_resolution(800, 600)


def set_1280x720():
    change_resolution(1280, 720)


def set_1920x1080():
    change_resolution(1920, 1080)


def change_difficulty():
    global difficulty
    if difficulty == "Normal":
        difficulty = "Hard"
    else:
        difficulty = "Normal"


def toggle_fps():
    global show_fps
    show_fps = not show_fps


# Функция для отображения окна настроек
def settings_window(screen):
    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
                return False  # Выход из основной программы

        screen.fill(GRAY)  # Заполняем окно настроек серым цветом

        # Рисуем кнопки
        fullscreen_button = draw_button(screen, f"Fullscreen: {'On' if fullscreen else 'Off'}",
                                        50, 50, 300, 40, WHITE, BLACK, toggle_fullscreen)

        res_800x600_button = draw_button(screen, "800x600", 50, 100, 140, 40, WHITE, BLACK, set_800x600)
        res_1280x720_button = draw_button(screen, "1280x720", 210, 100, 140, 40, WHITE, BLACK, set_1280x720)
        res_1920x1080_button = draw_button(screen, "1920x1080", 50, 150, 140, 40, WHITE, BLACK, set_1920x1080)

        difficulty_button = draw_button(screen, f"Difficulty: {difficulty}", 210, 150, 140, 40, WHITE, BLACK,
                                        change_difficulty)

        fps_button = draw_button(screen, f"Show FPS: {'On' if show_fps else 'Off'}", 50, 200, 300, 40, WHITE, BLACK,
                                 toggle_fps)

        back_button = draw_button(screen, "Back", 50, 250, 100, 40, WHITE, BLACK)

        # Проверка нажатия кнопки "Back"
        if back_button:
            settings_running = False
            return True  # Возвращаемся в основную программу

        pygame.display.flip()
    return False


# Основная функция игры

def main_menu(screen):
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.fill((0, 0, 255))  # Заполняем экран чёрным цветом

        # Заголовок меню
        title_text = FONT.render("My Awesome Game", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Кнопки меню
        start_button = draw_button(screen, "Start", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, BLACK)
        options_button = draw_button(screen, "Options", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, BLACK)
        quit_button = draw_button(screen, "Quit", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, GRAY, BLACK)

        # Обработка нажатий на кнопки
        if start_button:
            print("Start button clicked!")  # Замените на запуск игры
            menu_running = False  # Выход из меню
            return True  # Вернем True для запуска игры
        if options_button:
            print("Options button clicked!")  # Замените на открытие окна настроек
            settings_window(screen)
        if quit_button:
            exit(0)

        pygame.display.flip()

    return False


def death_screen(screen, score):
    """Отображает экран после смерти."""
    death_running = True
    while death_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.fill(BLACK)  # Заполняем экран чёрным цветом

        # Заголовок экрана смерти
        death_text = FONT.render("You Died!", True, RED)
        death_rect = death_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))
        screen.blit(death_text, death_rect)

        # Отображение счета
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 70 - 50))
        screen.blit(score_text, score_rect)

        # Кнопки экрана смерти
        restart_button = draw_button(screen, "Restart", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, BLACK)
        menu_button = draw_button(screen, "Main Menu", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, BLACK)
        quit_button = draw_button(screen, "Quit", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, GRAY, BLACK)

        # Обработка нажатий на кнопки
        if restart_button:
            global LEVEL_NUM, player, healthbar, gun, movement
            for sprite in all_sprites:
                sprite.kill()
            movement = [0, 0]
            player, healthbar, gun = generate_level(os.listdir('data/levels')[LEVEL_NUM])
            return True  # Возвращаем True для перезапуска игры
        if menu_button:
            main_menu(screen)
            return None  # Возвращаем None для возврата в главное меню
        if quit_button:
            exit(0)

        pygame.display.flip()

    return False


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


class Changer_levels(Block):
    def __init__(self, x, y, im):
        super().__init__(x, y, im)

    def act(self, pl):
        if type(pl) == Player:
            global LEVEL_NUM, player, healthbar, gun, movement
            for sprite in all_sprites:
                sprite.kill()
            LEVEL_NUM += 1
            level_name = os.listdir('data/levels')[LEVEL_NUM]
            movement = [0, 0]
            player, healthbar, gun = generate_level(level_name)


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
        if tile['type'] == 'robot':
            Robot(tile['pos'][0] * BLOCK_WIDTH, tile['pos'][1] * BLOCK_HEIGHT, player, 300, 300)
    healthbar = HealBar(10, 10, 80, 20, player)
    gun = Pistol('10.png', 80, player)
    return player, healthbar, gun


player, healthbar, gun = generate_level('map_test.json')
camera = Camera()
lever_changer = Changer_levels(2, 2, pygame.image.load('data/blocks/1.png'))

HealPotion(6, 7)
bullets = []


def main():
    running = True
    clock = pygame.time.Clock()
    fps = 60
    movement = [0, 0]
    main_menu(screen)
    while running:
        screen.fill((255, 255, 255))
        background_images = load_images('backgrounds')
        for im in background_images:
            screen.blit(im, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    movement[0] -= 5
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    movement[0] += 5
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    player.jump()
                if e.key == pygame.K_LSHIFT:
                    player.running(True)
                if e.key == pygame.K_1:
                    for entity in entities_sprites:
                        entity.show_hit_box()
                if e.key == pygame.K_2:
                    for enemy in enemises_sprites:
                        if type(enemy) == Robot:
                            enemy.blast()
                if e.key == pygame.K_ESCAPE:
                    settings_window(screen)
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    movement[0] += 5
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    movement[0] -= 5
                if e.key == pygame.K_LSHIFT:
                    player.running(False)

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    player.attack()
                    gun.shoot()
        clock.tick(fps)
        if not player.dead:
            camera.update(player)
            for i in all_sprites:
                camera.apply(i)
        if player.dead:
            death_screen(screen, 100)
        all_sprites.draw(screen)
        entities_sprites.draw(screen)
        player.update(sprite_blocks, screen, movement)
        enemises_sprites.update(sprite_blocks, screen, (0, 0))
        healthbar.draw(screen)
        healthbar.update_health()
        bullets_group.draw(screen)
        bullets_group.update(entities_sprites, sprite_blocks)
        sprite_blocks.update()
        pygame.display.flip()
    pygame.quit()


main()
