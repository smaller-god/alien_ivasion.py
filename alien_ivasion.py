import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion():
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # Группа для снарядов
        self.aliens = pygame.sprite.Group() # Группа для пришельцев
        self._create_fleet()  # Создаёт флот пришельцев
        self.stars = pygame.sprite.Group() # Группа для звёзд



        #Задание фонового цвета
        self.bg_image = pygame.image.load('images/background.jpg') # В данном случае подтягиваем картинку на фон

    def run_game(self):
        """Запускает основной цикл игры"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._check_fleet_edges()
            self.bullets.update()
            self._update_screen()
            self.clock.tick(60) # Ограничение FPS
            
    def _check_events(self):
        """Обрабатывает события клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создаёт новый снаряд и добавляет его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        # Обновление позиции снарядов
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)


                # Обновляем пришельцев перед проверкой коллизии
                self.aliens.update()

                # Проверка попаданий в пришельцев
                # При обнаружении попадания удаляет снаряд и пришельца
                collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)


                if collision:
                    for aliens in collision.values(): # Удаляем каждого пришельца из коллизии
                        for alien in aliens:
                            self.aliens.remove(alien)
                

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев на флоте"""
        self.aliens.update()

    def _create_fleet(self):
        """Создаёт флот пришельцев"""
        # Создание пришельца и добавление других, пока остаётся место
        # Расстояние между пришельцами составляет одну ширину и одну высоту
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_y = alien_height # Изначально позиция по y

        while current_y < (self.settings.screen_height - 3 * alien_height):
            current_x = alien_width # Начальная позиция по X для нового ряда

            while current_x < (self.settings.screen_width - 2 * alien_width):
                self.create_alien(current_x, current_y)
                current_x += 2 * alien_width # Смещаемся по X

            current_y += 2 * alien_width # После окончания ряда двигаемся вниз

    def create_alien(self, x_position, y_position):
        """Создаёт пришельца и размещает его в ряду"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцами края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break # Достаточно одного для смены направления

    def _change_fleet_direction(self):
        """Отпускает весь флот и меняет направление движения"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 # Меняем направление

      
    def _update_screen(self):
        """Обновляет экраны"""
        self.screen.blit(self.bg_image, (0, 0)) # Рисуем фон

        # Отрисовываем корабль
        self.ship.blitme()

        # Отрисовываем всех пришельцев
        self.aliens.draw(self.screen)

        # Отрисовываем все снаряды
        for bullet in self.bullets:
            bullet.draw_bullet()

        pygame.display.flip()

if __name__ == "__main__":
    # Создание экземлпяра и запуск игры
    ai = AlienInvasion()
    ai.run_game()

