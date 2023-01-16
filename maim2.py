import pygame
import os
import sys

import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('image/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
size = width, height = 840, 510
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_image = {'wall': load_image('wall.png'),
              'empty': load_image('floor.png')}
player_image1 = load_image('hero.png')
player_image2 = load_image('hero4.png')
player_image3 = load_image('hero2.png')
player_image4 = load_image('hero3.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image1
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

    def turn_left(self):
        self.image = player_image2

    def turn_right(self):
        self.image = player_image3

    def turn_up(self):
        self.image = player_image4

    def turn_down(self):
        self.image = player_image1


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["             Deep Dark Dangen", "",
                  "             Нажмите на кнопку мыши,",
                  "         чтобы играть"]
    fon = pygame.transform.scale(load_image('fon1.png'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_level(filename):
    filename = 'maps/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


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
                level[y][x] = '.'
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
            hero.turn_up()
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
            hero.turn_down()
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
            hero.turn_left()
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)
            hero.turn_right()



if __name__ == '__main__':
    pygame.display.set_caption('DDD')
    player = None
    ranning = True
    start_screen()
    level_map = load_level('map.txt')
    hero, max_x, max_y = generate_level(level_map)

    camera = Camera()

    while ranning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ranning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(hero, 'up')
                if event.key == pygame.K_s:
                    move(hero, 'down')
                if event.key == pygame.K_d:
                    move(hero, 'right')
                if event.key == pygame.K_a:
                    move(hero, 'left')

            # изменяем ракурс камеры
            camera.update(hero)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
