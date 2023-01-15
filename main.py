import pygame
#import pygame as pq
import os
import sys
from ObjectsDDD import Player, Gun
from Start_sc import StartWin
from Map1 import Level1


def run():

    pygame.init()
    screen = pygame.display.set_mode((840, 510))
    pygame.display.set_caption("DDD")
    bg_color = (0, 0, 0)
    hero = Player(screen)
    gun = Gun(screen)
    startwin = StartWin(screen)
    level1 = Level1(screen)
    startwin.start_screen()

  #  level_map = level1.load_level('map1.txt')
  #  level_x, level_y = level1.generate_level(level_map)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_KP_ENTER:
#
                if event.key == pygame.K_d: #вправо
                    hero.mright = True
                    hero.turn_right()
                elif event.key == pygame.K_a: #влево
                    hero.mleft = True
                    hero.turn_left()
                elif event.key == pygame.K_w: #вперед
                    hero.mup = True
                    hero.turn_up()
                elif event.key == pygame.K_s: #вниз
                    hero.mdown = True
                    hero.turn_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d: #вправо
                    hero.mright = False
                elif event.key == pygame.K_a: #влево
                    hero.mleft = False
                elif event.key == pygame.K_w: #вперед
                    hero.mup = False
                elif event.key == pygame.K_s: #вниз
                    hero.mdown = False



        screen.fill(bg_color)
        level1.go()
        # gun.output()
        hero.update_hero()
        hero.output()
        pygame.display.flip()


run()
