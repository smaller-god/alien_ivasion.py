import sys
import pygame
import os
from pygame.sprite import Sprite

class Ship(pygame.sprite.Sprite):
    """Класс для управления кораблём"""

    def  __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение корабля и получает прямоугольник
        try:
            self.image = pygame.image.load(os.path.join('images', 'ship.png'))
        except pygame.error:
            print("Ошибка: Не удалось загрузить изображение корабля!")
            sys.exit()

        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        # Флаги перемещения: начинаем с неподвижного корабля
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию корабля с учётом флага"""
        # Обновляет атрибут x объекта ship, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """размещает корабль в центре нижней части экрана"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)