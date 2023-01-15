import pygame
#import pygame as pq
import sys
import os


FPS = 60

class StartWin:
    def __init__(self, screen):
        self.screen = screen
        self.fon = pygame.image.load("image/fon1.png")
        self.rect = self.fon.get_rect()
        self.screen_rect = screen.get_rect()

    def start_screen(self):
        clock = pygame.time.Clock()
        intro_text = ["             Deep Dark Dangen", "",
                      "             Нажмите на кнопку мыши,",
                      "         чтобы играть"]
        self.screen.blit(self.fon, self.rect)
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return #начинаем игру
            pygame.display.flip()
            clock.tick(FPS)
