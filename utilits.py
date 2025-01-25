import pygame
import sys
import os


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Animations:
    def __init__(self, sheet, columns, rows, x, y, frame_duration):
        self.frames = []
        self.sheet = sheet
        self.columns = columns
        self.rows = rows
        self.frame_duration = frame_duration
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                im = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                rect2 = im.copy().get_bounding_rect()
                screen = pygame.Surface((4 + rect2.width + 1, rect2.height + 1), pygame.SRCALPHA, 32)
                screen.blit(im, (2, 0),
                            ((rect2.x - 1, rect2.y - 1), (4 + rect2.width + 1, rect2.height + 1)))

                im = screen
                self.frames.append(im)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames) * self.frame_duration)
        self.image = self.frames[self.cur_frame // self.frame_duration]

    def copy(self):
        return Animations(self.sheet.copy(), self.columns, self.rows, self.rect.x, self.rect.y, self.frame_duration)


all_sprites = pygame.sprite.Group()
animations = {'player/idle': Animations(pygame.image.load('data/entities/player/Cyborg_idle.png'), 4, 1, 0, 0, 6),
              'player/run': Animations(pygame.image.load('data/entities/player/Cyborg_run.png'), 6, 1, 0, 0, 5),
              'player/jump': Animations(pygame.image.load('data/entities/player/Cyborg_jump.png'), 4, 1, 0, 0, 12),
              'player/death': Animations(pygame.image.load('data/entities/player/Cyborg_jump.png'), 5, 1, 0, 0, 5),
              'player/attack': Animations(pygame.image.load('data/entities/player/Cyborg_attack3.png'), 8, 1, 0, 0, 5),
              'player/attack_run': Animations(pygame.image.load('data/entities/player/Cyborg_run_attack.png'), 8, 1, 0, 0, 6),
              'robot/idle': Animations(pygame.image.load('data/entities/enemies/robot/robot_idle.png'), 4, 1, 0, 0, 6),
              'robot/run': Animations(pygame.image.load('data/entities/enemies/robot/robot_run.png'), 6, 1, 0, 0, 6)}
