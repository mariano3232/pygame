import pygame, sys 
from character import Character
import pygame.font

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

font = pygame.font.Font(None, 20)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("juegardium")
clock = pygame.time.Clock()
FPS = 60

controls1 = {
    'left':pygame.K_a,
    'right':pygame.K_d,
    'up':pygame.K_w,
    'dash':pygame.K_g,
    'attack1':pygame.K_t,
    'attack2':pygame.K_y,
    'attack3':pygame.K_u,
}
controls2 = {
    'left':pygame.K_LEFT,
    'right':pygame.K_RIGHT,
    'up':pygame.K_UP,
    'dash':pygame.K_m,
    'attack1':pygame.K_j,
    'attack2':pygame.K_k,
    'attack3':pygame.K_l,
}

attacks1 = [
    { 
        'startup': 5,
        'active': 10,
        'recovery': 10,
        'damage':100,
        'position': [10,-40],
        'width':140,
        'height':30,
    },
    { 
        'startup': 20,
        'active': 15,
        'recovery': 20,
        'damage':100,
        'position': [10,-40],
        'width':150,
        'height':70,
    },
    { 
        'startup': 5,
        'active': 10,
        'recovery': 10,
        'damage':100,
        'position': [40,-140],
        'width':80,
        'height':100,
    },
]
attacks2 = [
    { 
        'startup': 5,
        'active': 5,
        'recovery': 5,
        'damage':100,
        'position': [10,-40],
        'width':100,
        'height':30,
    },
    { 
       'startup': 20,
        'active': 10,
        'recovery': 10,
        'damage':100,
        'position': [30,30],
        'width':150,
        'height':30,
    },
    { 
        'startup': 5,
        'active': 15,
        'recovery': 20,
        'damage':100,
        'position': [-100,-140],
        'width':200,
        'height':70,
    },
]

fighter_1 = Character(200, SCREEN_HEIGHT - FLOOR_HEIGHT - 140, controls1, attacks1)
fighter_2 = Character(700, SCREEN_HEIGHT - FLOOR_HEIGHT - 140, controls2, attacks2)

def update_screen():
    #Fondo y piso:
    screen.fill(LIGHTBLUE)
    pygame.draw.rect(screen, OLIVE, (0, SCREEN_HEIGHT - FLOOR_HEIGHT , SCREEN_WIDTH,  FLOOR_HEIGHT))
    #Personajes :
    fighter_1.draw(screen, BLUE, fighter_2)
    fighter_2.draw(screen, (255,255,0), fighter_1)
    #barras de vida
    vida_1 = font.render(str(fighter_1.health), True, (0, 0, 0))
    vida_2 = font.render(str(fighter_2.health), True, (0, 0, 0))
    pygame.draw.rect(screen, GREY, (20, 20 , 400,  30))
    pygame.draw.rect(screen, GREY, (SCREEN_WIDTH - 400 - 20, 20 , 400,  30))

    health_ratio_1 = fighter_1.health * 400 /1000
    health_ratio_2 = fighter_2.health * 400 /1000

    pygame.draw.rect(screen, RED, (20, 20 , health_ratio_1,  30))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 400 - 20, 20 , health_ratio_2,  30))

    screen.blit(vida_1, (10, 10))
    screen.blit(vida_2, (SCREEN_WIDTH - 100, 10))

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