import sys
import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
import time
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
    # 创建配置对象
    ai_settings = Settings()
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # 创建Play按钮
    play_button = Button(ai_settings,screen,"Play")
    # 创建一个用于储存游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 创建一只飞船，一个子弹编组和一个外星人编组
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    # 创建储存游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
            ship.update()
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()
