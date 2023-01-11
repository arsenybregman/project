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


class Level1:
    def __init__(self, screen, tile_type, pos_x, pos_y):
        self.screen = screen
        tile_width = tile_height = 50
      #  self.floor = pygame.image.load("image/floor.png")
      #  self.wall = pygame.image.load("image/wall.png")
        tile_images = {
            'wall': pygame.image.load("image/wall.png"),
            'floor': pygame.image.load("image/floor.png")
        }
      #  self.rect = self..get_rect()
      #  self.screen_rect = screen.get_rect()
       # self.map =
        super().__init__(tile_images)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def load_level(self, filename):
        self.filename = "maps/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(self.filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self, level):
        x, y = None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Level1('floor', x, y)
                elif level[y][x] == '#':
                    Level1('wall', x, y)
                #elif level[y][x] == '@':
                  #  Level1('empty', x, y)
                 #   new_player = Player(x, y)
        return x, y