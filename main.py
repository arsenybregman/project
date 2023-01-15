import pygame
#import pygame as pq
import os
import sys
#from ObjectsDDD import Player, Gun, Camera
from log import load_image
#from Map1 import Level1
from Map1 import load_level, generate_level
from Start_sc import StartWin

sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

level_map = load_level('map.txt')
hero, max_x, max_y = generate_level(level_map)

size = width, height = 840, 510
screen = pygame.display.set_mode(size)


def start_screen():
    clock = pygame.time.Clock()
    intro_text = ["             Deep Dark Dangen", "",
                    "             Нажмите на кнопку мыши,",
                    "         чтобы играть"]
    fon = pygame.transform.scale(load_image("fon1.png"), size)
    screen.blit((fon), (0, 0))
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


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def run():

#if __name__ == '__main__':
    pygame.display.set_caption("DDD")
    bg_color = (0, 0, 0)
    player = None
    ranning = True

    startwin = StartWin(screen)
    startwin.start_screen()

    level_map = load_level('map.txt')
    hero, max_x, max_y = generate_level(level_map)

    while ranning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ranning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(hero, 'up')
                if event.key == pygame.K_DOWN:
                    move(hero, 'down')
                if event.key == pygame.K_RIGHT:
                    move(hero, 'right')
                if event.key == pygame.K_LEFT:
                    move(hero, 'left')

        screen.fill(bg_color)
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    #pygame.quit()
 #   hero = Player()
 #   gun = Gun(screen)
   # startwin = StartWin(screen)
   # level1 = Level1(screen)
   # camera = Camera()
   # startwin.start_screen()

  #  player = None



  #  while True:
     #   camera.update(hero)
        # обновляем положение всех спрайтов
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
         #       sys.exit()
         #   elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_KP_ENTER:
#
           #     if event.key == pygame.K_d: #вправо
            #        hero.mright = True
              #      hero.turn_right()
             #   elif event.key == pygame.K_a: #влево
              #      hero.mleft = True
               #     hero.turn_left()
              #  elif event.key == pygame.K_w: #вперед
               #     hero.mup = True
              #      hero.turn_up()
             #   elif event.key == pygame.K_s: #вниз
              #      hero.mdown = True
              #      hero.turn_down()
         #   elif event.type == pygame.KEYUP:
           #     if event.key == pygame.K_d: #вправо
           #         hero.mright = False
           #     elif event.key == pygame.K_a: #влево
            #        hero.mleft = False
           #     elif event.key == pygame.K_w: #вперед
             #       hero.mup = False
            #    elif event.key == pygame.K_s: #вниз
            #        hero.mdown = False

     #   screen.fill(bg_color)
      #  sprite_group.draw(screen)
     #   hero_group.draw(screen)
        # gun.output()
       # hero.update_hero()
       # hero.output(screen)
      #  pygame.display.flip()


run()
