import pygame
from pygame.sprite import Sprite

class Bullet(pygame.sprite.Sprite):
    """Класс для управления снарядами, выпущенными кораблём"""

    def __init__(self, ai_game):
        """Создаёт объект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

        self.image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height))
        self.image.fill(self.color)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # Обновление точной позиции снаряда
        self.y -= self.settings.bullet_speed
        # Обновление позиции треугольника
        self.rect.y = self.y
        self.rect.x = self.rect.x

    def draw_bullet(self):
        """Выводит снаряды на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)