class Settings:
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # Параметры экрана
        self.screen_width = 1366
        self.screen_height = 768
        self.bg_color = (0, 0, 0)


        # Настройки корабля
        self.ship_limit = 2

        # Параметры снаряда
        self.bullet_speed = 3
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (250, 60, 60)
        self.bullets_allowed = 99

        # Настройки пришельцев
        self.fleet_drop_speed = 5

        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельца
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, меняющиеся по ходу игры"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # Подсчёт очков
        self.alien_points = 50

        # fleet_direction = 1 означает движение вправо, а -1 -- влево
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пришельцев"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)