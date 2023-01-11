import pygame
import pygame as pq
import sys
from ObjectsDDD import Player, Tile, ScreenFrame, Sprite
import os

WIDTH = 874  # ширина игрового окна
HEIGHT = 500 # высота игрового окна
FPS = 60 # частота кадров в секунду


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



tile_images = {
    'wall': pq.image.load('wall.png'),
    'empty': pq.image.load('floor.png')
}
player_image = pq.image.load('hero.png')

tile_width = tile_height = 50

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DDD")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
all_sprites.update()
game_folder = os.path.dirname(__file__)

running = True


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(pq.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
   # filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level_map = load_level('map.txt')
hero, max_x, max_y = generate_level(level_map)

def move(hero, movement):
    x, y = hero.pas
    print(level_map[x][y - 1])
    print(level_map[x][y + 1])
    print(level_map[x - 1][y])
    print(level_map[x][y + 1])
    print()
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            player.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == ".":
            player.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            player.move(x - 1, y)
    elif movement == "eight":
        if x < max_x - 1 and level_map[y][x + 1] == ".":
            player.move(x + 1, y)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
    pygame.display.flip()
    clock.tick(FPS)

    pygame.display.flip()

pygame.quit()