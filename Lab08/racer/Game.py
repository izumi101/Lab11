# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing pygame
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("//Users/ali.nd/Desktop/PP2/Lab08/racer/background.png")

# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy class
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("/Users/ali.nd/Desktop/PP2/Lab08/racer/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("/Users/ali.nd/Desktop/PP2/Lab08/racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/ali.nd/Desktop/PP2/Lab08/racer/coin.jpg")
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the coin
        self.rect = self.image.get_rect()
        self.spawn_coin()
    
    def spawn_coin(self):
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            if not (E1.rect.left - 40 < x < E1.rect.right + 40 and E1.rect.top - 40 < y < E1.rect.bottom + 40):
                self.rect.center = (x, y)
                break
    
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn_coin()

# Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    # Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Drawing background
    DISPLAYSURF.blit(background, (0,0))
    
    # Displaying scores
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    
    # Displaying collected coins
    coins_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))
    
    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    # Check for collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('/Users/ali.nd/Desktop/PP2/Lab08/racer/crash.wav').play()
          time.sleep(1)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()
    
    # Check for collision between player and coin
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        C1.spawn_coin()
    
    pygame.display.update()
    FramePerSec.tick(FPS)

