import pygame
from PIL import Image
#import pygame as pq

FPS = 60


class Player:
    def __init__(self, screen):
        #инициализация игрока
        self.screen = screen
        self.image1 = pygame.image.load("image/hero1.png")
        self.image2 = pygame.image.load("image/hero2.png")
        self.image3 = pygame.image.load("image/hero3.png")
        self.image4 = pygame.image.load("image/hero4.png")
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom

        self.mright = False
        self.mleft = False
        self.mup = False
        self.mdown = False

    def output(self):
        #отрисовка игрока
        self.screen.blit(self.image, self.rect)

    def update_hero(self):
        #обновление позиций игрока
        clock = pygame.time.Clock()
        v = 80
        clock.tick(FPS)
        if self.mright and self.rect.right < self.screen_rect.right:
            self.rect.centerx += v / FPS
        elif self.mleft and self.rect.left > self.screen_rect.left:
            self.rect.centerx -= v / FPS
        elif self.mup and self.rect.top > self.screen_rect.top:
            self.rect.centery -= v / FPS
        elif self.mdown and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += v / FPS

    def turn_left(self):
        self.image = self.image4

    def turn_right(self):
        self.image = self.image2

    def turn_up(self):
        self.image = self.image3

    def turn_down(self):
        self.image = self.image1


class Gun:
    def __init__(self, screen):
        #инициализация пистолета
        self.screen = screen
        self.image = pygame.image.load("image/gun.png")

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def output(self):
        #отрисовка пистолета
        self.screen.blit(self.image, self.rect)

