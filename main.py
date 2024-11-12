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

# test_sheet = pygame.image.load("assets/images/wizard.png").convert_alpha()
# TEST_ANIMATION_STEPS = [8,8,1,8,8,3,7]

test_sheet = pygame.image.load("assets/images/spritesheetfix.png").convert_alpha()
TEST_ANIMATION_STEPS = [5,6]

TEST_CHARACTER_DATA = {
    #Tamaño de cada cuadrado de la sprite sheet en px:
    'sheet_square_size': 458,
    'scale': 0.5,
    'offset':[75,50]
}

# TEST_CHARACTER_DATA = {
#     #Tamaño de cada cuadrado de la sprite sheet en px:
#     'sheet_square_size': 162,
#     'scale': 2.5,
#     'offset':[270,280]
# }

controls1 = {
    'left':pygame.K_a,
    'right':pygame.K_d,
    'up':pygame.K_w,
    'dash':pygame.K_g,
    'attack1':pygame.K_t,
    'attack2':pygame.K_y,
}
controls2 = {
    'left':pygame.K_LEFT,
    'right':pygame.K_RIGHT,
    'up':pygame.K_UP,
    'dash':pygame.K_m,
    'attack1':pygame.K_j,
    'attack2':pygame.K_k,
}

attacks = [
    { 
        'startup': 60,
        'active': 12,
        'recovery': 12,
        'damage':100,
        'position': [40,-40],
        'width':30,
        'height':30,
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

# print("TEST_CHARACTER_DATA :",TEST_CHARACTER_DATA)
fighter_1 = Character(200, SCREEN_HEIGHT - FLOOR_HEIGHT - 140, controls1, attacks, test_sheet, TEST_ANIMATION_STEPS, TEST_CHARACTER_DATA)
fighter_2 = Character(700, SCREEN_HEIGHT - FLOOR_HEIGHT - 140, controls2, attacks, test_sheet, TEST_ANIMATION_STEPS, TEST_CHARACTER_DATA)

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
    fighter_1.update()
    fighter_2.update()
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