import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人类"""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载外星人图像，并设置rect属性
        image = pygame.image.load('images/enemy1.png')
        self.image = pygame.transform.scale(image,(80,int(80/image.get_rect().width * image.get_rect().height)))
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 储存外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            return True

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.y += self.ai_settings.fleet_drop_speed
        self.rect.y = self.y