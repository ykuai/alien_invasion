import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.sprite import GroupSingle

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self,ai_settings,screen,ship):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.image = pygame.image.load("images/bullet5.png")
        self.color = ai_settings.bullet_color
        self.track_range = ai_settings.bullet_track_range
        self.speed_factor = ai_settings.bullet_speed_factor
        self.angle = 0
        # 储存位置矢量
        self.v = Vector2(float(self.rect.x),float(self.rect.y))
        # 储存速度矢量
        self.speed_v = Vector2(0,-ai_settings.bullet_speed_factor)
        # 储存跟踪对象
        self.track_target = GroupSingle()

    def alter_speed(self):
        """根据子弹当前位置和跟踪目标位置调整速度"""
        if self.track_target:
            # 跟踪目标位置
            tt_v = Vector2(self.track_target.sprite.rect.center)
            # 子弹当前位置到跟踪位置的向量
            distance = Vector2(tt_v.x - self.v.x,tt_v.y - self.v.y)
            # 假如跟踪目标超出范围则移除目标
            if distance.length() > self.track_range:
                self.track_target.empty()
            # 否则调整速度，跟踪目标
            else:
                self.speed_v = distance.normalize() * self.speed_factor
                self.angle = self.speed_v.angle_to(Vector2(0,-1))

    def update(self):
        self.v.x = self.v.x + self.speed_v.x
        self.v.y = self.v.y + self.speed_v.y
        self.rect.x = self.v.x
        self.rect.y = self.v.y

    def draw(self):
        self.screen.blit(pygame.transform.rotate(self.image,self.angle),self.rect)

