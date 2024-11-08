import pygame

class Character:
    def __init__(self, x, y, controls,attacks):
        self.rect = pygame.Rect(x, y, 90, 140)
        self.controls = controls
        self.attacks = attacks
        self.vel_y = 0
        self.facing_right = True
        #status
        self.knockback = 0
        self.startup = 0
        self.recovery = 0
        self.attacking = 0
        self.jumping = False
        self.dash = False
        self.dash_timer = 0
        #attack
        self.attack_data = {
            'startup': 0,
            'active': 0,
            'recovery': 0,
            'position':[0,0],
            'width':0,
            'height':0,
        }

    def draw(self, screen, color, enemy):
        pygame.draw.rect(screen, color, self.rect)

        if self.attacking and not self.startup:
            hitbox = pygame.Rect(
                self.rect.centerx + self.attack_data['position'][0] if self.facing_right else self.rect.centerx - self.attack_data['position'][0] - self.attack_data['width'],
                self.rect.centery + self.attack_data['position'][1],
                self.attack_data['width'],
                self.attack_data['height'],
            )

            hits = hitbox.colliderect(enemy.rect)
            if (hits) :
                enemy.vel_y = -5
                enemy.knockback = 20

            pygame.draw.rect(screen, (255,0,0), hitbox)

    
    def attack(self, attack_data):
        self.attack_data = attack_data
        self.startup = attack_data['startup']
        self.attacking = attack_data['active']

    def move(self, screen, screen_width, screen_height, floor_height, enemy):
        SPEED = 7
        JUMPING_SPEED = 8
        DASH_SPEED = 25  
        DASH_DURATION = 10  
        GRAVITY = 1
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        #Dirección
        if self.rect.centerx > enemy.rect.centerx : self.facing_right = False
        else: self.facing_right = True

        #Ataques
        if key[self.controls['attack1']] and not self.recovery and not self.startup and not self.attacking and not self.knockback:
            self.attack(self.attacks[0])
        if key[self.controls['attack2']] and not self.recovery and not self.startup and not self.attacking and not self.knockback:
            self.attack(self.attacks[1])
        if key[self.controls['attack3']] and not self.recovery and not self.startup and not self.attacking and not self.knockback:
            self.attack(self.attacks[2])
        
        if self.startup > 0 : self.startup -= 1
        if self.attacking > 0 and not self.startup : self.attacking -= 1
        if self.attacking == 1 : self.recovery = self.attack_data['recovery']
        # Movimiento horizontal
        if key[self.controls['left']] and not self.jumping and not self.recovery and not self.startup and not self.attacking and not self.knockback:
            dx = -SPEED
        if key[self.controls['right']] and not self.jumping and not self.recovery and not self.startup and not self.attacking and not self.knockback:
            dx = SPEED
        # knockback
        if self.knockback>0:
            dx = -self.knockback if self.facing_right else self.knockback
            self.knockback-=1

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
        if self.jumping == 'right' and not self.knockback:
            dx = JUMPING_SPEED
        elif self.jumping == 'left' and not self.knockback:
            dx = -JUMPING_SPEED
        elif self.jumping == 'neutral' and not self.knockback:
            dx = 0
        # Dash
        if key[self.controls['dash']] and self.dash_timer == 0 and not self.recovery and not self.dash and (not self.jumping or self.rect.bottom < 300):
            self.dash_timer = DASH_DURATION
            self.dash  = DASH_SPEED if self.facing_right else -DASH_SPEED
            if key[self.controls['left']] and self.facing_right:
                self.dash  = -DASH_SPEED
            if key[self.controls['right']] and not self.facing_right:
                self.dash  = DASH_SPEED

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
        #Colisiones 
        if self.rect.colliderect(enemy.rect):
            # horizontales
            if self.rect.right > enemy.rect.left and self.rect.left < enemy.rect.left:
                self.rect.right = enemy.rect.left
            elif self.rect.left < enemy.rect.right and self.rect.right > enemy.rect.right:
                self.rect.left = enemy.rect.right
            # Corner
            if self.rect.centerx == enemy.rect.centerx and self.rect.bottom < enemy.rect.bottom :    
                if self.rect.centerx > screen_width/2:
                    dx = -10
                else : dx = 10

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
