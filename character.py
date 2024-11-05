import pygame

class Character:
    def __init__(self, x, y, controls):
        self.rect = pygame.Rect(x, y, 90, 140)
        self.controls = controls
        self.vel_y = 0
        self.jumping = False
        self.dash = False
        self.dash_timer = 0
        self.startup = 0
        self.recovery = 0
        self.attacking = 0
        self.attack_data = {
            'startup': 10,
            'active': 10,
            'recovery': 10,
            'rect': pygame.Rect(self.rect.centerx + 40, self.rect.centery -40, 100, 30)
        }

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        if self.attacking:
            pygame.draw.rect(screen, (255,0,0), self.attack_data['rect'])
    
    def attack(self):
        attack_data = {
            'startup': 4,
            'active': 2,
            'recovery': 2,
            'rect': pygame.Rect(self.rect.centerx + 40, self.rect.centery -40, 100, 30)
        }
        self.attack_data = attack_data
        self.startup = attack_data['startup']
        self.attacking = attack_data['active']

    def move(self, screen, screen_width, screen_height, floor_height):
        SPEED = 7
        JUMPING_SPEED = 8
        DASH_SPEED = 25  
        DASH_DURATION = 10  
        GRAVITY = 1
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        hitbox = pygame.Rect(0,0,300,150)
        pygame.draw.rect(screen, (255,0,0), hitbox)

        #Ataque
        if key[self.controls['attack']]:
            self.attack()
        
        if self.startup > 0 : self.startup -= 1
        if self.attacking > 0 and not self.startup : self.attacking -= 1
        if self.attacking == 1 : self.recovery = self.attack_data['recovery']
        # Movimiento horizontal
        if key[self.controls['left']] and not self.jumping and not self.recovery and not self.startup:
            dx = -SPEED
        if key[self.controls['right']] and not self.jumping and not self.recovery and not self.startup:
            dx = SPEED

        # Jump
        if key[self.controls['up']] and not self.jumping and not self.recovery:
            self.vel_y = -20
            self.jumping = 'neutral'
            if key[self.controls['right']]:
                self.jumping = 'right'
            elif key[self.controls['left']]:
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
        if key[self.controls['dash']] and self.dash_timer == 0 and not self.recovery and not self.dash and (not self.jumping or self.rect.bottom < 300):
            self.dash_timer = DASH_DURATION
            self.dash  = DASH_SPEED
            if key[self.controls['left']]:
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
