#sprite

import pygame
import random
import os
from pygame.constants import KEYDOWN
from pygame.draw import rect
FPS=60

BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
WIDTH=500
HEIGHT=600

#遊戲初始化 and 創建視窗

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("家宇戰ㄐ")
clock = pygame.time.Clock() 

#載入圖片
background_img =  pygame.image.load(os.path.join("img","background.png")).convert()
player_img =  pygame.image.load(os.path.join("img","player.png")).convert()
#rock_img =  pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img =  pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,30))
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #self.rect.x=200
        #self.rect.y=200
        self.radius=23
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx =WIDTH/2
        self.rect.bottom =HEIGHT-10
        self.speedx=8
        

    def update(self):
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x +=self.speedx
        if key_pressed[pygame.K_LEFT]:    
            self.rect.x -=self.speedx

        
        if self.rect.right > WIDTH:
          self.rect.right =WIDTH
        if self.rect.left < 0:
            self.rect.left =0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori=random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius=self.rect.width*0.9/2
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3) 
        
        self.rect.x=random.randrange(0,WIDTH - self.rect.width)
        self.rect.y=random.randrange(-200,-100)
        self.speedy=random.randrange(2,10)  
        self.speedx=random.randrange(-3,3)
        
    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center = center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right <0:
            self.rect.x=random.randrange(0,WIDTH - self.rect.width)
            self.rect.y=random.randrange(-200,-40)
            self.speedy=random.randrange(2,10)
            self.speedx=random.randrange(-3,3)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx= x
        self.rect.bottom=y
        self.speedy = -10
        

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill()


all_sprites=pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r= Rock()
    all_sprites.add(r)
    rocks.add(r)


#rock =Rock()
#all_sprites.add(rock)

#遊戲迴圈
running = True
while running:
    #Clock.tick=1秒鐘之內最多執行10次
    #clock.tick(10)
    clock.tick(FPS)

    #取得輸入
    #pygame.event.get會回傳此遊戲同時發生的案件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #更新遊戲

    all_sprites.update()
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        r=Rock()
        all_sprites.add(r)
        rocks.add(r)
    
    hits=pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hits:
        running =False


    #畫面顯示
    #fill(R,G,B)
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    screen.blit(background_img,(0,0))
    screen.blit(background_img,(0,0))
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    #
    pygame.display.update()
pygame.QUIT






