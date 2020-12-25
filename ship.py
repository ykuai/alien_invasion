import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        # 初始化飞船并设置初始位置
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("images/ship1.png")
        self.rect = pygame.Rect(0,0,75,87)
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.screen_rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect,(119,0,75,87))

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx