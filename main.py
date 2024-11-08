import pygame, sys 
from character import Character

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)
RED = (255,0,0)
BLUE = (0,0,255)
LIGHTBLUE = (0,255,255)
OLIVE = (128,128,0)

SCREEN_WIDTH=1000
SCREEN_HEIGHT=600
FLOOR_HEIGHT=150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("juegardium")
clock = pygame.time.Clock()
FPS = 60

controls1 = {
    'left':pygame.K_a,
    'right':pygame.K_d,
    'up':pygame.K_w,
    'dash':pygame.K_t,
    'attack':pygame.K_y,
}
controls2 = {
    'left':pygame.K_LEFT,
    'right':pygame.K_RIGHT,
    'up':pygame.K_UP,
    'dash':pygame.K_k,
    'attack':pygame.K_l,
}

fighter_1 = Character(200, SCREEN_HEIGHT - FLOOR_HEIGHT - 140, controls1)
fighter_2 = Character(700, SCREEN_HEIGHT - FLOOR_HEIGHT - 140, controls2)

def update_screen():
    #Fondo y piso:
    screen.fill(LIGHTBLUE)
    pygame.draw.rect(screen, OLIVE, (0, SCREEN_HEIGHT - FLOOR_HEIGHT , SCREEN_WIDTH,  FLOOR_HEIGHT))
    #Personajes :
    fighter_1.draw(screen, BLUE, fighter_2)
    fighter_2.draw(screen, (255,255,0), fighter_1)

while True : 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == 256:
            pygame.quit()
            sys.exit()
    
    key = pygame.key.get_pressed()
    if key:
        fighter_1.move(screen,SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT,fighter_2)
        fighter_2.move(screen,SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT,fighter_1)
    
    update_screen()
    pygame.display.update()