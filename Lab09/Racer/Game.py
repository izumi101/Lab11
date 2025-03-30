import pygame, sys
from pygame.locals import *
import random, time

pygame.init() # Инициализация Pygame

FPS = 60 # Кадры в секунду
FramePerSec = pygame.time.Clock() # Объект Clock для контроля FPS

BLUE = (0, 0, 255) # Синий цвет
RED = (255, 0, 0) # Красный цвет
GREEN = (0, 255, 0) # Зеленый цвет
BLACK = (0, 0, 0) # Черный цвет
WHITE = (255, 255, 255) # Белый цвет

SCREEN_WIDTH = 400 # Ширина экрана
SCREEN_HEIGHT = 600 # Высота экрана
SPEED = 5 # Начальная скорость врагов
SCORE = 0 # Начальный счет
COINS_COLLECTED = 0 # Начальное количество собранных монет
COIN_SPEED_INCREASE_THRESHOLD = 5 # Порог монет для увеличения скорости

font = pygame.font.SysFont("Verdana", 60) # Шрифт для большого текста
font_small = pygame.font.SysFont("Verdana", 20) # Шрифт для маленького текста
game_over = font.render("Game Over", True, BLACK) # Текст "Game Over"

background = pygame.image.load("//Users/ali.nd/Desktop/PP2/Lab08/racer/background.png") # Загрузка фона

DISPLAYSURF = pygame.display.set_mode((400, 600)) # Создание экрана
DISPLAYSURF.fill(WHITE) # Заполнение экрана белым цветом
pygame.display.set_caption("Game") # Заголовок окна

class Enemy(pygame.sprite.Sprite): # Класс врага
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ali.nd/Desktop/PP2/Lab08/racer/enemy.png") # Загрузка изображения врага
        self.rect = self.image.get_rect() # Получение прямоугольника врага
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) # Начальная позиция врага

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED) # Движение врага вниз
        if self.rect.bottom > 600: # Если враг вышел за экран
            SCORE += 1 # Увеличение счета
            self.rect.top = 0 # Возвращение врага наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) # Новая позиция врага

class Player(pygame.sprite.Sprite): # Класс игрока
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ali.nd/Desktop/PP2/Lab08/racer/Player.png") # Загрузка изображения игрока
        self.rect = self.image.get_rect() # Получение прямоугольника игрока
        self.rect.center = (160, 520) # Начальная позиция игрока

    def move(self):
        pressed_keys = pygame.key.get_pressed() # Получение нажатых клавиш
        if self.rect.left > 0 and pressed_keys[K_LEFT]: # Движение влево
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]: # Движение вправо
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite): # Класс монеты
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ali.nd/Desktop/PP2/Lab08/racer/coin.jpg") # Загрузка изображения монеты
        self.image = pygame.transform.scale(self.image, (30, 30)) # Изменение размера монеты
        self.rect = self.image.get_rect() # Получение прямоугольника монеты
        self.spawn_coin() # Создание монеты

    def spawn_coin(self):
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40) # Случайная позиция x
            y = random.randint(0, SCREEN_HEIGHT // 2) # Случайная позиция y
            if not (E1.rect.left - 40 < x < E1.rect.right + 40 and E1.rect.top - 40 < y < E1.rect.bottom + 40): # Избегание столкновения с врагом
                self.rect.center = (x, y)
                break

    def move(self):
        self.rect.move_ip(0, SPEED) # Движение монеты вниз
        if self.rect.top > SCREEN_HEIGHT: # Если монета вышла за экран
            self.spawn_coin() # Создание новой монеты

P1 = Player() # Создание игрока
E1 = Enemy() # Создание врага
C1 = Coin() # Создание монеты

enemies = pygame.sprite.Group() # Группа врагов
enemies.add(E1) # Добавление врага в группу
coins = pygame.sprite.Group() # Группа монет
coins.add(C1) # Добавление монеты в группу
all_sprites = pygame.sprite.Group() # Группа всех спрайтов
all_sprites.add(P1) # Добавление игрока
all_sprites.add(E1) # Добавление врага
all_sprites.add(C1) # Добавление монеты

INC_SPEED = pygame.USEREVENT + 1 # Событие увеличения скорости
pygame.time.set_timer(INC_SPEED, 1000) # Таймер увеличения скорости

def countdown(): # Функция обратного отсчета
    for i in range(3, 0, -1): # Цикл от 3 до 1
        count_text = font.render(str(i), True, BLACK) # Создание текста с цифрой
        DISPLAYSURF.blit(background, (0, 0)) # Отображение фона
        DISPLAYSURF.blit(count_text, (SCREEN_WIDTH // 2 - count_text.get_width() // 2, SCREEN_HEIGHT // 2 - count_text.get_height() // 2)) # Отображение цифры
        pygame.display.update() # Обновление экрана
        time.sleep(1) # Задержка в 1 секунду
    go_text = font.render("GO!", True, BLACK) # Создание текста "GO!"
    DISPLAYSURF.blit(background, (0, 0)) # Отображение фона
    DISPLAYSURF.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - go_text.get_height() // 2)) # Отображение "GO!"
    pygame.display.update() # Обновление экрана
    time.sleep(1) # Задержка в 1 секунду

countdown() # Запуск отсчета

while True: # Основной игровой цикл
    for event in pygame.event.get(): # Обработка событий
        if event.type == INC_SPEED: # Увеличение скорости
            SPEED += 0.5
        if event.type == QUIT: # Выход из игры
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0)) # Отображение фона

    scores = font_small.render(str(SCORE), True, BLACK) # Отображение счета
    DISPLAYSURF.blit(scores, (10, 10))

    coins_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK) # Отображение монет
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    for entity in all_sprites: # Отображение спрайтов
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(P1, enemies): # Столкновение с врагом
        pygame.mixer.Sound('/Users/ali.nd/Desktop/PP2/Lab08/racer/crash.wav').play() # Звук столкновения
        time.sleep(1)

        DISPLAYSURF.fill(RED) # Красный экран
        DISPLAYSURF.blit(game_over, (30, 250)) # Отображение "Game Over"

        pygame.display.update() # Обновление экрана
        for entity in all_sprites: # Удаление спрайтов
            entity.kill()
        time.sleep(2) # Задержка
        pygame.quit() # Выход из игры
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins): # Столкновение с монетой
        COINS_COLLECTED += 1 # Увеличение монет
        C1.spawn_coin() # Создание новой монеты
        if COINS_COLLECTED % COIN_SPEED_INCREASE_THRESHOLD == 0: # Увеличение скорости
            SPEED += 1

    pygame.display.update() # Обновление экрана
    FramePerSec.tick(FPS) # Контроль FPS
    