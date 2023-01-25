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
width, height = 840, 510
size = [width, height]
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
bullet_right_group = pygame.sprite.Group()
bullet_left_group = pygame.sprite.Group()
bullet_down_group = pygame.sprite.Group()
bullet_up_group = pygame.sprite.Group()
knife_group = pygame.sprite.Group()

door_group = pygame.sprite.Group()


tile_image = {'wall': load_image('wall.png'),
              'empty': load_image('floor.png')}
player_image1 = load_image('hero.png')
player_image2 = load_image('hero4.png')
player_image3 = load_image('hero2.png')
player_image4 = load_image('hero3.png')

gun_image_up = load_image('gun_up.png')
gun_image_down = load_image('gun_down.png')
gun_image_left = load_image('gun_left.png')
gun_image_right = load_image('gun_right.png')
bullet_image = load_image('bullet.png')
knife_image = load_image('knife.png')

monster1 = load_image("mons1.png")
monster2 = load_image("mons2.png")

door = load_image('door (1).png')

WHERE = 'down'
tile_width = tile_height = 50
pygame.mixer.music.load('sound/war.mp3')
sound1 = pygame.mixer.Sound('sound/boom.mp3')

up_bullet = None
down_bullet = None
right_bullet = None
left_bullet = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
rival_group = pygame.sprite.Group()


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
    def __init__(self, group, all_sprites):
        super().__init__(group, all_sprites)
        self.rect = None

    def get_event(self, event):
        pass


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group, all_sprites)
        self.image = player_image1
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.image)

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

    def get_coords(self):
        return self.pos


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group, all_sprites)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Monster(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(rival_group, all_sprites)
        self.image = monster1
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        self.screen_rect = screen.get_rect()
        self.f = 0.0025

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

    def m_left(self):
        self.image = monster2

    def m_right(self):
        self.image = monster1

    def go(self):
        x, y = self.pos
        if self.rect.left == 55:
            mon.m_right()
            self.f = -1 * self.f

        if self.rect.right == 400:
            mon.m_left()
            self.f = -1 * self.f
        mon.move(x + self.f, y)


#Камера
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def apply(self, target):
        return target.rect.move(self.state.topleft)


class Door(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = door
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)
        self.screen_rect = screen.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


class Bullet_right(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_right_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

    def turn_right(self):
        self.image = bullet_image

    def get_coords(self):
        return self.pos


class Bullet_left(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_left_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

    def turn_left(self):
        self.image = bullet_image

    def get_coords(self):
        return self.pos


class Bullet_up(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_up_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

    def turn_up(self):
        self.image = bullet_image

    def get_coords(self):
        return self.pos


class Bullet_down(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_down_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

    def turn_down(self):
        self.image = bullet_image

    def get_coords(self):
        return self.pos


def camera_func(camera, target_rect):
    l = -target_rect.x + size[0] // 2
    t = -target_rect.y + size[1] // 2

    w, h = camera.width, camera.height

    l = min(0, l)
    l = max(-(camera.width - size[0]), l)

    t = max(-(camera.height - size[1]), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)


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


def generate_level(level):
    new_player, x, y, new_door = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                mon = Monster(x, y)
                level[y][x] = '.'
                rival_group.add(mon)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == '*':
                Tile('empty', x, y)
                new_door = Door(x, y)
                level[y][x] = '.'

    return new_player, x, y, rival_group, new_door


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


total_level_width = 50 * 50
total_level_height = 50 * 50

camera = Camera(camera_func, total_level_width, total_level_height)





if __name__ == '__main__':
    pygame.display.set_caption('DDD')

    sprite_group.add(bullet_left_group)
    sprite_group.add(bullet_right_group)
    sprite_group.add(bullet_up_group)
    sprite_group.add(bullet_down_group)

    hero = None
    ranning = True
    start_screen()

    #level_1(Sprite)

   # level_2(Sprite)

    level_map = load_level('map.txt')
    n = 10

    hero, max_x, max_y, rival_group, door = generate_level(level_map)

    pygame.mixer.music.play()

    pygame.mouse.set_visible(False)

    #door.add(door_group)
    sprite_group.add(hero)
# sprite_group.add(mon)
    sprite_group.add(rival_group)
    sprite_group.add(door)

    while ranning:
        for mon in rival_group:
            mon.go()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ranning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(hero, 'up')
                    WHERE = 'up'
                if event.key == pygame.K_s:
                    move(hero, 'down')
                    WHERE = 'down'
                if event.key == pygame.K_d:
                    move(hero, 'right')
                    WHERE = 'right'
                if event.key == pygame.K_a:
                    move(hero, 'left')
                    WHERE = 'left'
                if event.key == pygame.K_SPACE:
                    sound1.play()
                    if WHERE == 'up':
                        up_bullet = Bullet_up(hero.get_coords()[0], hero.get_coords()[1])
                        sprite_group.add(up_bullet)
                        bullet_up_group.add(up_bullet)
                        bullet_up_group.draw(screen)
                    elif WHERE == 'down':
                        down_bullet = Bullet_down(hero.get_coords()[0], hero.get_coords()[1])
                        sprite_group.add(down_bullet)
                        bullet_down_group.add(down_bullet)
                        bullet_down_group.draw(screen)
                    elif WHERE == 'left':
                        left_bullet = Bullet_left(hero.get_coords()[0], hero.get_coords()[1])
                        sprite_group.add(left_bullet)
                        bullet_left_group.add(left_bullet)
                        bullet_left_group.draw(screen)
                    elif WHERE == 'right':
                        right_bullet = Bullet_right(hero.get_coords()[0], hero.get_coords()[1])
                        sprite_group.add(right_bullet)
                        bullet_right_group.add(right_bullet)
                        bullet_right_group.draw(screen)

        if n == 10:
            if pygame.sprite.collide_mask(hero, door):
                sprite_group.empty()
                rival_group.empty()

                level_map = load_level('map2.txt')
                hero, max_x, max_y, rival_group, door = generate_level(level_map)
                sprite_group.add(hero)
                # sprite_group.add(mon)
                sprite_group.add(rival_group)

                n = 0
          #  sprite_group.add(door)

        screen.fill(pygame.Color('black'))
        camera.update(hero)
        for sprite in sprite_group:
            screen.blit(sprite.image, camera.apply(sprite))

        if up_bullet is not None:
            move(up_bullet, 'up')
            if level_map[up_bullet.get_coords()[1] - 1][up_bullet.get_coords()[0]] == '#':
                up_bullet.kill()
        if down_bullet is not None:
            move(down_bullet, 'down')
            if level_map[down_bullet.get_coords()[1] + 1][down_bullet.get_coords()[0]] == '#':
                down_bullet.kill()
        if left_bullet is not None:
            move(left_bullet, 'left')
            if level_map[left_bullet.get_coords()[1]][left_bullet.get_coords()[0] - 1] == '#':
                left_bullet.kill()
        if right_bullet is not None:
            move(right_bullet, 'right')
            if level_map[right_bullet.get_coords()[1]][right_bullet.get_coords()[0] + 1] == '#':
                right_bullet.kill()
        for monster in rival_group:
            if up_bullet is not None and pygame.sprite.collide_rect(monster, up_bullet):
                monster.kill()
                up_bullet.kill()
            if down_bullet is not None and pygame.sprite.collide_rect(monster, down_bullet):
                monster.kill()
                down_bullet.kill()
            if left_bullet is not None and pygame.sprite.collide_rect(monster, left_bullet):
                monster.kill()
                left_bullet.kill()
            if right_bullet is not None and pygame.sprite.collide_rect(monster, right_bullet):
                monster.kill()
                right_bullet.kill()
            if pygame.sprite.collide_rect(monster, hero):
                terminate()
        #sprite_group.draw(screen)
        #hero_group.draw(screen)
      #  rival_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
