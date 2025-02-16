class GameStats:
    """Отслеживает статистику для игры"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0 # Рекорд не должен сбрасываться
        self.level = 1
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def load_high_score(self):
        """Загружает рекорд из файла"""
        try:
            with open("record.txt", 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Сохраняет рекорд в файл"""
        with open('record.txt', 'w') as file:
            file.write(str(self.high_score))