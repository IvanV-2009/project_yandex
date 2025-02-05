import pygame
import sys
import os

pygame.init()
def load_image(name, colorkey=None):
    image = pygame.image.load('data/' + name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_images(path):
    images = []
    for img_name in sorted(os.listdir('data/' + path)):
        images.append(load_image(path + '/' + img_name))
    return images


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
                screen = pygame.Surface((4 + rect2.width + 1, rect2.height + 2), pygame.SRCALPHA, 32)
                screen.blit(im, (2, 0),
                            ((rect2.x - 1, rect2.y - 1), (4 + rect2.width + 1, rect2.height + 2)))

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
              'player/death': Animations(pygame.image.load('data/entities/player/Cyborg_death.png'), 6, 1, 0, 0, 11),
              'player/attack': Animations(pygame.image.load('data/entities/player/Cyborg_attack3.png'), 8, 1, 0, 0, 5),
              'player/attack_run': Animations(pygame.image.load('data/entities/player/Cyborg_run_attack.png'), 8, 1, 0,
                                              0, 6),
              'robot/idle': Animations(pygame.image.load('data/entities/enemies/robot/robot_idle.png'), 4, 1, 0, 0, 6),
              'robot/run': Animations(pygame.image.load('data/entities/enemies/robot/robot_run.png'), 6, 1, 0, 0, 6),
              'robot/hurt': Animations(pygame.image.load('data/entities/enemies/robot/robot_hurt.png'), 2, 1, 0, 0, 9),
              'player/hurt': Animations(pygame.image.load('data/entities/player/Cyborg_hurt.png'), 2, 1, 0, 0, 9),
              'robot/death': Animations(pygame.image.load('data/entities/enemies/robot/robot_death.png'), 6, 1, 0, 0,
                                        10),
              'robot/shoting': Animations(pygame.image.load('data/entities/enemies/robot/robot_death.png'), 6, 1, 0, 0,
                                          5)}

