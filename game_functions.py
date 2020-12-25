import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet
from settings import Settings
from pygame.math import Vector2
import math

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    # 响应键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                fire_bullet(ai_settings,screen,ship,bullets)
            elif event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_ships()

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环绘制背景图
    screen.blit(ai_settings.img, ai_settings.img.get_rect())
    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)
    # 绘制子弹
    for bullet in bullets:
        bullet.draw()
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新子弹位置，删除已消失的子弹"""
    for bullet in bullets:
        bullet.alter_speed()
    bullets.update()
    # 当子弹离开屏幕时删除子弹
    # 检测子弹是否有跟踪目标
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        else:
            for alien in aliens:
                # 假如外星人在子弹跟踪范围内，则记录跟踪目标
                distance = math.hypot(alien.rect.x-bullet.rect.x,alien.rect.y-bullet.rect.y)
                if distance <= ai_settings.bullet_track_range and not bullet.track_target:
                    bullet.track_target.add(alien)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(aliens,bullets,True,True)
    if collisions:
        stats.score += ai_settings.alien_points * len(collisions.keys())
        sb.prep_score()
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    # 计算每行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    # 计算屏幕可容纳多少行外星人
    number_rows = get_number_rows(ai_settings,ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人"""
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - (3*alien_height)-ship_height
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达屏幕边缘时采取响应措施"""
    for alien in aliens:
        if alien.check_edges():
            # 改变外星人的移动方向
            ai_settings.fleet_direction *= -1
            #change_fleet_direction(ai_settings,aliens)
            break

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 1:
        # 将ships_left减一
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break

####
def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
