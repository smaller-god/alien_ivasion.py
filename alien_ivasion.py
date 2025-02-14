import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
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

        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # Группа для снарядов
        self.aliens = pygame.sprite.Group() # Группа для пришельцев
        self._create_fleet()  # Создаёт флот пришельцев
        self.stars = pygame.sprite.Group() # Группа для звёзд
        self.game_active = False # Запускает игру в неактивном состоянии

        # Создаёт кнопку Play
        self.play_button = Button(self, "Play")

        #Задание фонового цвета
        self.bg_image = pygame.image.load('images/background.png') # В данном случае подтягиваем картинку на фон


    def run_game(self):
        """Запускает основной цикл игры"""
        while True:
            self._check_events()

            if self.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Сброс игровой статистики
            self.stats.reset_stats()
            self.game_active = True

            # Очистка групп aliens и bullets
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)
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

                self.check_bullet_alien_collision()

    def check_bullet_alien_collision(self):
        """Обрабатывает коллизии снарядов с пришельцами"""
        # Удаление снарядов и пришельцев, учавствующих в коллизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()

                

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев на флоте"""
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверка, сталкиваются ли пришельцы с нижним краем экрана
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля и пришельца"""
        if self.stats.ships_left > 0:
            # Уменьшение ships_lef
            self.stats.ships_left -= 1

            # Очистка групп aliens и bullets
            self.aliens.empty()
            self.bullets.empty()

         # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.game_active = False

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
                current_x += int(alien_width * 1.5) # Смещаемся по X

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

    def _check_aliens_bottom(self):
        """Проверяем, добрались ли пришельцы до нижнего края экрана"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Происходит то же самое, что при столкновении с кораблём
                self._ship_hit()
                break


      
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

        # Кнопка Play отображается в том случае, если игра не активна
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == "__main__":
    # Создание экземлпяра и запуск игры
    ai = AlienInvasion()
    ai.run_game()

