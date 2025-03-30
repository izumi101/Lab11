import pygame
import math

def main():
    pygame.init() # Инициализация Pygame
    screen = pygame.display.set_mode((640, 480)) # Создание окна
    clock = pygame.time.Clock() # Создание объекта Clock для контроля FPS
    
    radius = 15 # Радиус кисти
    x = 0 # Координата X
    y = 0 # Координата Y
    mode = 'blue' # Текущий режим рисования (цвет)
    points = [] # Список точек для рисования линий
    shapes = [] # Список прямоугольников
    circles = [] # Список кругов
    triangles = [] # Список треугольников
    rhombuses = [] # Список ромбов

    drawing = False # Флаг рисования
    start_pos = None # Начальная позиция для рисования фигур
    drawing_rect = False # Флаг рисования прямоугольника
    drawing_circle = False # Флаг рисования круга
    drawing_triangle = False # Флаг рисования треугольника
    drawing_rhombus = False # Флаг рисования ромба

    while True:
        
        pressed = pygame.key.get_pressed() # Получение нажатых клавиш
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT] # Проверка нажатия клавиши Alt
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL] # Проверка нажатия клавиши Ctrl
        
        for event in pygame.event.get(): # Обработка событий
            
            # Определение, был ли нажат X, Ctrl+W или Alt+F4
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # Определение, была ли нажата клавиша буквы
                if event.key == pygame.K_r:
                    mode = 'red' # Красный цвет
                elif event.key == pygame.K_g:
                    mode = 'green' # Зеленый цвет
                elif event.key == pygame.K_b:
                    mode = 'blue' # Синий цвет
                elif event.key == pygame.K_e:   # Ластик
                    mode = 'eraser'
                elif event.key == pygame.K_s:
                    mode = 'square' # Квадрат
                elif event.key == pygame.K_c:
                    mode = 'circle' # Круг
                elif event.key == pygame.K_t:
                    mode = 'triangle' # Треугольник
                elif event.key == pygame.K_h:
                    mode = 'rhombus' # Ромб

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 'square':    # Квадрат
                    start_pos = event.pos
                    drawing_rect = True
                elif mode == 'circle':  # Круг
                    start_pos = event.pos
                    drawing_circle = True
                elif mode == 'triangle': # Треугольник
                    start_pos = event.pos
                    drawing_triangle = True
                elif mode == 'rhombus': # Ромб
                    start_pos = event.pos
                    drawing_rhombus = True
                else:
                    drawing = True
                    points.append(((None,None),mode))
                points.append(((None,None), mode))
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing_rect and start_pos:      # Квадрат
                    end_pos = event.pos
                    shapes.append((start_pos, end_pos, mode))
                    drawing_rect = False
                elif drawing_circle and start_pos:  # Круг
                    end_pos = event.pos
                    circles.append((start_pos, end_pos, mode))
                    drawing_circle = False
                elif drawing_triangle and start_pos: # Треугольник
                    end_pos = pygame.mouse.get_pos()
                    triangles.append((start_pos, end_pos, mode))
                    drawing_triangle = False
                elif drawing_rhombus and start_pos:
                    end_pos = pygame.mouse.get_pos()
                    rhombuses.append((start_pos, end_pos, mode))
                    drawing_rhombus = False
                drawing = False
            
            if event.type == pygame.MOUSEMOTION and drawing:
                # Если мышь движется во время рисования, добавляем точку в список
                position = event.pos
                points.append((position, mode))
                
        screen.fill((0, 0, 0)) # Заполнение экрана черным цветом
        for rect in shapes:
            start, end, rect_mode = rect
            drawRectangle(screen, start, end, rect_mode) # Рисование прямоугольника
        
        for circle in circles:
            start, end, circle_mode = circle
            drawCircle(screen, start, end, circle_mode) # Рисование круга
        
        for triangle in triangles:
            start, end, triangle_mode = triangle
            drawTriangle(screen, start, end, triangle_mode) # Рисование треугольника
        
        for rhombus in rhombuses:
            start, end, rhombus_mode = rhombus
            drawRhombus(screen, start, end, rhombus_mode) # Рисование ромба

        # Рисование всех точек
        i = 0
        while i < len(points) - 1:
            if points[i][0] != (None,None) and points[i+1][0] != (None,None):
                drawLineBetween(screen, i, points[i], points[i + 1], radius, points[i][1]) # Рисование линии между точками
            i += 1

        if drawing_rect and start_pos:
            end_pos = pygame.mouse.get_pos()
            drawRectangle(screen, start_pos, end_pos, mode) # Рисование прямоугольника в реальном времени
        
        if drawing_circle and start_pos:
            end_pos = pygame.mouse.get_pos()
            drawCircle(screen, start_pos, end_pos, mode) # Рисование круга в реальном времени
        
        if drawing_triangle and start_pos:
            end_pos = pygame.mouse.get_pos()
            drawTriangle(screen, start_pos, end_pos, mode) # Рисование треугольника в реальном времени

        if drawing_rhombus and start_pos:
            end_pos = pygame.mouse.get_pos()
            drawRhombus(screen, start_pos, end_pos, mode) # Рисование ромба в реальном времени

        pygame.display.flip() # Обновление экрана
        
        clock.tick(60) # Установка FPS

def drawLineBetween(screen, index, point1, point2, width, color_mode):
    start, color_mode = point1
    end, _ = point2
    
    if color_mode == 'blue':
        color = (0, 0, 255) # Синий цвет
    elif color_mode == 'red':
        color = (255, 0, 0) # Красный цвет
    elif color_mode == 'green':
        color = (0, 255, 0) # Зеленый цвет
    elif color_mode == 'eraser':
        color = (0,0,0) # Черный цвет (ластик)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width) # Рисование круга в каждой точке

def drawRectangle(screen, start, end, color_mode):
    if color_mode == 'blue':
        color = (0, 0, 255) # Синий цвет
    elif color_mode == 'red':
        color = (255, 0, 0) # Красный цвет
    elif color_mode == 'green':
        color = (0, 255, 0) # Зеленый цвет
    else:
        color = (255, 255, 255)  # Цвет по умолчанию (белый)

    rect_x = min(start[0], end[0])
    rect_y = min(start[1], end[1])
    rect_width = abs(start[0] - end[0])
    rect_height = abs(start[1] - end[1])

    pygame.draw.rect(screen, color, (rect_x, rect_y, rect_width, rect_height), 3) # Рисование прямоугольника

def drawCircle(screen, start, end, color_mode):
    if color_mode == 'blue':
        color = (0, 0, 255) # Синий цвет
    elif color_mode == 'red':
        color = (255, 0, 0) # Красный цвет
    elif color_mode == 'green':
        color = (0, 255, 0) # Зеленый цвет
    else:
        color = (255, 255, 255)  # Цвет по умолчанию (белый)

    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    radius = max(abs(start[0] - end[0]) // 2, abs(start[1] - end[1]) // 2)

    pygame.draw.circle(screen, color, (center_x, center_y), radius, 3) # Рисование круга

def drawTriangle(screen, start, end, color_mode):
    if color_mode == 'blue':
        color = (0, 0, 255) # Синий цвет
    elif color_mode == 'red':
        color = (255, 0, 0) # Красный цвет
    elif color_mode == 'green':
        color = (0, 255, 0) # Зеленый цвет
    else:
        color = (255, 255, 255)  # Цвет по умолчанию (белый)
    
    p1 = start
    p2 = (end[0], start[1])
    p3 = end
    
    pygame.draw.polygon(screen, color, (p1, p2, p3), 3) # Рисование треугольника

def drawRhombus(screen, start, end, color_mode):
    if color_mode == 'blue':
        color = (0, 0, 255) # Синий цвет
    elif color_mode == 'red':
        color = (255, 0, 0) # Красный цвет
    elif color_mode == 'green':
        color = (0, 255, 0) # Зеленый цвет
    else:
        color = (255, 255, 255)  # Цвет по умолчанию (белый)

    center_x = (start[0] + end[0]) // 2
    center_y = (start[1] + end[1]) // 2
    half_width = abs(start[0] - end[0]) // 2
    half_height = abs(start[1] - end[1]) // 2

    p1 = (center_x, center_y - half_height)
    p2 = (center_x + half_width, center_y)
    p3 = (center_x, center_y + half_height)
    p4 = (center_x - half_width, center_y)

    pygame.draw.polygon(screen, color, (p1, p2, p3, p4), 3) # Рисование ромба

main()