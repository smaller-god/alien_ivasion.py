class Settings:
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1366
        self.screen_height = 768
        self.bg_color = (0, 0, 0)


        # Настройки корабля
        self.ship_speed = 5
        self.ship_limit = 2

        # Параметры снаряда
        self.bullet_speed = 3
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (250, 60, 60)
        self.bullets_allowed = 99

        # Настройки пришельцев
        self.alien_speed = 1
        self.fleet_drop_speed = 5
        # fleet_direction = 1 означает движение вправо, а -1 -- влево
        self.fleet_direction = 1