import pygame
#import pygame as pq
import os
import sys
from ObjectsDDD import Player


PLATFORM_WIDTH = 40
PLATFORM_HEIGHT = 40
PLATFORM_COLOR = (9, 15, 33)


class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()

        entities = pygame.sprite.Group()  # Все объекты
        platforms = []  # то, во что мы будем врезаться или опираться
        hero = Player(screen)
        entities.add(hero)

        self.level = [
            "-------------------------",
            "-                       -",
            "-                       -",
            "-                       -",
            "-            --         -",
            "-                       -",
            "--                      -",
            "-                       -",
            "-                   --- -",
            "-                       -",
            "-                       -",
            "-      ---              -",
            "-                       -",
            "-   -----------        -",
            "-                       -",
            "-                -      -",
            "-                   --  -",
            "-                       -",
            "-                       -",
            "-------------------------"]

    def go(self):
        x = y = 0  # координаты
        for row in self.level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    # создаем блок, заливаем его цветом и рисеум его
                    pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(PLATFORM_COLOR)
                    self.screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


