import pygame

class Settings():
    """储存所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.img = pygame.image.load("images/background1.jpg")
        self.screen_width = self.img.get_rect().width
        self.screen_height = self.img.get_rect().height
        self.bg_color = (230,230,230)
        # 飞船设置
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 5
        self.bullet_track_range = 300
        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.2
        self.bullet_speed_factor = 0.3
        # 外星人设置
        self.alien_speed_factor = 0.2
        self.fleet_drop_speed = 0.02
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50
    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.speedup_scale)