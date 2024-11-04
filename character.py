import pygame

class Character:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,70,100)
        self.vel_y = 0
        self.jumping = False

    def draw(self,screen,color):
        pygame.draw.rect(screen, color, self.rect)

    def move(self, screen_width, screen_height, floor_height):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a ] and not self.jumping : dx = -SPEED
        if key[pygame.K_d ] and not self.jumping : dx = SPEED
        if key[pygame.K_w ] and not self.jumping :
            self.vel_y = -30
            self.jumping = True

        if self.rect.left + dx < 0 : dx = -self.rect.left
        if self.rect.right + dx > screen_width : dx = screen_width - self.rect.right

        self.vel_y +=GRAVITY
        dy = self.vel_y

        if self.rect.bottom + dy > screen_height - floor_height:
            dy = screen_height - floor_height - self.rect.bottom
            self.jumping = False

        self.rect.y += dy
        self.rect.x += dx