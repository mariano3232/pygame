import pygame

class Character:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 140)
        self.vel_y = 0
        self.jumping = False
        self.dash = False
        self.dash_timer = 0
        self.recovery = False
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

    def move(self, screen_width, screen_height, floor_height):
        SPEED = 7
        JUMPING_SPEED = 8
        DASH_SPEED = 25  
        DASH_DURATION = 10  
        GRAVITY = 1
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        # Movimiento horizontal
        if key[pygame.K_a] and not self.jumping and not self.recovery:
            dx = -SPEED
        if key[pygame.K_d] and not self.jumping and not self.recovery:
            dx = SPEED

        # Jump
        if key[pygame.K_w] and not self.jumping and not self.recovery:
            self.vel_y = -20
            self.jumping = 'neutral'
            if key[pygame.K_d]:
                self.jumping = 'right'
            elif key[pygame.K_a]:
                self.jumping = 'left'

        self.vel_y += GRAVITY
        dy = self.vel_y
        if self.rect.bottom + dy > screen_height - floor_height:
            dy = screen_height - floor_height - self.rect.bottom
            if self.jumping : self.recovery = 3
            self.jumping = False
        if self.jumping == 'right':
            dx = JUMPING_SPEED
        elif self.jumping == 'left':
            dx = -JUMPING_SPEED
        elif self.jumping == 'neutral':
            dx = 0
        # Dash
        if key[pygame.K_y] and self.dash_timer == 0 and not self.recovery and not self.dash and (not self.jumping or self.rect.bottom < 300):
            self.dash_timer = DASH_DURATION
            self.dash  = DASH_SPEED
            if key[pygame.K_a]:
                self.dash  = -DASH_SPEED

        if self.dash:
            #dash saltando
            if self.jumping :
                if self.dash > 0 : self.jumping = 'right' 
                else : self.jumping = 'left'
            #Duracion y recovery
            self.vel_y = 0
            if self.dash_timer > 0:
                dx=self.dash
                self.dash_timer -= 1
            else:
                self.recovery = 7
                if self.jumping : self.recovery = 15
                self.dash = False

        #Recovery
        if self.recovery > 0:
            self.recovery -= 1
            if self.recovery == 0 : self.recovery=False
        # Bordes
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        self.rect.y += dy
        self.rect.x += dx
