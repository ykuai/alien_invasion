import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard():
    """显示得分信息的类"""
    def __init__(self,ai_settings,screen,stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # 显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        # 准备初始得分图像
        self.prep_score()
        self.prep_ships()

    def prep_score(self):
        # 将得分转换为一副渲染的图像
        rounded_score = int(round(self.stats.score,-1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image,self.score_rect)
        # 绘制飞船
        #for ship in self.ships:
        #   self.screen.blit(ship.image, ship.rect,(119,0,75,87))