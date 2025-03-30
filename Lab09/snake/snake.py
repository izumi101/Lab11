import pygame
import random
import sys

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Размер окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Demo")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.Font(None, 30)

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Настройки змейки
snake_pos = [100, 50]  # Начальная позиция головы змейки
snake_body = [[100, 50], [90, 50], [80, 50]]  # Тело змейки
snake_direction = "RIGHT"
change_to = snake_direction
speed = 5  # Начальная скорость

# Функция генерации еды с разными весами
def generate_food():
    """Генерирует случайное положение еды и случайный вес (1, 2 или 3 очка)."""
    while True:
        food_x = random.randrange(0, WIDTH, 10)
        food_y = random.randrange(0, HEIGHT, 10)
        if [food_x, food_y] not in snake_body:  # Проверяем, не попадает ли еда на тело змейки
            return [food_x, food_y], random.choice([1, 2, 3])  # Возвращаем позицию и вес еды

food_pos, food_weight = generate_food()
food_spawn = True
food_timer = 300  # Таймер исчезновения еды (в кадрах)

# Счёт и уровни
game_score = 0
level = 1

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and snake_direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                change_to = "RIGHT"

    # Движение змейки
    snake_direction = change_to
    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10

    # Вставка новой позиции
    snake_body.insert(0, list(snake_pos))

    # Проверка съедения еды
    if snake_pos == food_pos:
        food_spawn = False
        game_score += food_weight  # Добавляем очки согласно весу еды
        food_timer = 300  # Сбрасываем таймер еды

        # Каждые 4 очка — новый уровень
        if game_score % 4 == 0:
            level += 1
            speed += 2  # Увеличение скорости на каждом уровне
    else:
        snake_body.pop()

    # Таймер исчезновения еды
    if food_timer > 0:
        food_timer -= 1
    else:
        food_spawn = False  # Еда исчезает, создаём новую

    # Генерация новой еды, если её нет
    if not food_spawn:
        food_pos, food_weight = generate_food()
        food_spawn = True
        food_timer = 300  # Ставим новый таймер

    # Проверка столкновения со стенами
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        isRunning = False

    # Проверка столкновения с самой собой
    for block in snake_body[1:]:
        if snake_pos == block:
            isRunning = False

    # Отрисовка элементов на экране
    screen.fill(BLACK)
    
    # Отрисовка змейки
    for p in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(p[0], p[1], 10, 10))

    # Отрисовка еды разными цветами в зависимости от её веса
    food_colors = {1: RED, 2: (255, 165, 0), 3: (255, 255, 0)}  # Красный, оранжевый, жёлтый
    pygame.draw.rect(screen, food_colors[food_weight], pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Отображение счёта и уровня
    score_text = font.render(f"Score: {game_score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(speed)  # Управление скоростью змейки

# Экран завершения игры
game_over_text = font.render("GAME OVER", True, WHITE)
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (WIDTH / 2, HEIGHT / 2)
screen.blit(game_over_text, game_over_rectangle)
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
