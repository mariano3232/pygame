import pygame

class Character:
    def __init__(self, x, y, controls, attacks, sheet, animation_steps, animation_data):
        self.rect = pygame.Rect(x, y, 70, 130)
        self.health = 1000
        self.controls = controls
        self.attacks = attacks
        self.vel_y = 0
        self.facing_right = True
        #animations
        self.animation_steps= animation_steps
        self.animation_list= self.load_images(sheet, animation_steps, animation_data)
        self.animation_data=animation_data
        self.sheet_square_size = animation_data['sheet_square_size']
        self.action = 0 #0:idle, 1:piña,
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        #status / timers
        self.knockback = 0
        self.startup = 0
        self.recovery = 0
        self.attacking = 0
        self.jumping = False
        self.dash = False
        self.dash_timer = 0
        #attack
        self.attack_hitted = False
        self.attack_data = {
            'startup': 0,
            'active': 0,
            'recovery': 0,
            'damage':0,
            'position':[0,0],
            'width':0,
            'height':0,
        }
    def load_images(self, sheet, steps, animation_data) :
        scale = animation_data['scale']
        animations_list = []
        square_size = 410
        for y,animation in enumerate(steps):
            current_animation_list=[]
            for i in range (animation):
                # current_image = sheet.subsurface(i*square_size , y*square_size, square_size, square_size)
                current_image = sheet.subsurface(i*square_size , y*square_size, square_size, 400)
                scaled_current_image = pygame.transform.scale(current_image,(square_size*scale, square_size*scale))
                current_animation_list.append(scaled_current_image)
            animations_list.append(current_animation_list)
        return animations_list
        
    def draw(self, screen, color, enemy):
        #Rectangulo / hurtbox / collision box
        # pygame.draw.rect(screen, color, self.rect)
        # sprite
        img = self.image
        correction = 0
        if not self.facing_right:
            img = pygame.transform.flip(self.image,1,0)
            correction = -30

        screen.blit(img, (self.rect.x - self.animation_data['offset'][0] -correction, self.rect.y - self.animation_data['offset'][1]))
        #attack/hitbox/damage
        if self.attacking and not self.startup:
            hitbox = pygame.Rect(
                self.rect.centerx + self.attack_data['position'][0] if self.facing_right else self.rect.centerx - self.attack_data['position'][0] - self.attack_data['width'],
                self.rect.centery + self.attack_data['position'][1],
                self.attack_data['width'],
                self.attack_data['height'],
            )
            hits = hitbox.colliderect(enemy.rect)
            if (hits) :
                if not self.attack_hitted :
                    enemy.vel_y = -5
                    enemy.knockback = 20
                    enemy.health -= self.attack_data['damage']
                    self.attack_hitted = True

            pygame.draw.rect(screen, (255,0,0), hitbox)

    def update(self):
        # print("self.animation_list[0] :",self.animation_list[0])
        if pygame.time.get_ticks() % 12 == 0 :
            # print("self.action :",self.action)
            # print("self.frame_index :",self.frame_index)
            self.image = self.animation_list[self.action][self.frame_index]
            self.frame_index += 1
            if self.frame_index == self.animation_steps[self.action] : self.frame_index = 0

    def attack(self, attack_data):
        self.attack_hitted = False
        self.attack_data = attack_data
        self.startup = attack_data['startup']
        self.attacking = attack_data['active']
        self.frame_index = 0

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
            self.action=1
        if key[self.controls['attack2']] and not self.recovery and not self.startup and not self.attacking and not self.knockback:
            self.attack(self.attacks[1])
        
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
            if self.recovery == 0 : 
                self.recovery=False
                self.frame_index = 0
                self.action=0
        # Bordes
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        self.rect.y += dy
        self.rect.x += dx
