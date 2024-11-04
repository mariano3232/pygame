import pygame, sys 
from character import Character

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)
RED = (255,0,0)
BLUE = (0,0,255)

SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
FLOOR_HEIGHT=150
P1_HEIGHT = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("juegardium")
clock = pygame.time.Clock()
FPS = 60

p1x = 40
p1y = SCREEN_HEIGHT - FLOOR_HEIGHT - P1_HEIGHT
vel1x = 0.6
vel1y = 0
acc1x = 0
gravity = 0.01

fighter_1 = Character(200, SCREEN_HEIGHT - FLOOR_HEIGHT - 100)
fighter_2 = Character(700, SCREEN_HEIGHT - FLOOR_HEIGHT - 100)

def update_screen():
    #Fondo y piso:
    screen.fill(GREY)
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - FLOOR_HEIGHT , SCREEN_WIDTH,  FLOOR_HEIGHT))
    #Personajes :
    fighter_1.draw(screen, BLUE)
    fighter_2.draw(screen, RED)

while True : 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == 256:
            pygame.quit()
            sys.exit()
    
    key = pygame.key.get_pressed()
    if key:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT)
        # fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT)
    
    update_screen()
    pygame.display.update()