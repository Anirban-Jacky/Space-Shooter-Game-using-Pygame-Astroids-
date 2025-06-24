import pygame
import random
from os import path

img_dir=path.join(path.dirname(__file__),"img")

WIDTH = 700
HEIGHT = 640
FPS = 60
POWER_TIME=5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASTEROIDS")
clock = pygame.time.Clock()

font_name=pygame.font.match_font("arial")
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)

def newmob():
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield(surf,x,y,per):
    if per<0:
        per=0
    Bar_L=200
    Bar_H=10
    fill=(per/100)*Bar_L
    outline_rect=pygame.Rect(x,y,Bar_L,Bar_H)
    fill_rect=pygame.Rect(x,y,fill,Bar_H)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)   

def draw_lives(surf,x,y,live,img):
    for i in range(live):
        img_rect=img.get_rect()
        img_rect.x=x+40*i
        img_rect.y=y
        surf.blit(img,img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=player_img
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.radius=34
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius,1)
        self.rect.centerx= WIDTH/2
        self.rect.bottom= HEIGHT-15
        self.speedx=0
        self.shield=100
        self.shoot_delay=250
        self.last_shot=pygame.time.get_ticks()
        self.lives=3
        self.hidden=False
        self.hid_timer=pygame.time.get_ticks()
        self.power=1
        self.power_timer=pygame.time.get_ticks()

    def hide(self):
        self.hidden=True
        self.hid_timer=pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+200)   

    def powerup(self):
        self.power+=1
        self.power_timer=pygame.time.get_ticks()   

    def update(self):
        if self.power>=2 and pygame.time.get_ticks()-self.power_timer>POWER_TIME:
            self.power-=1
            self.power_timer=pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks()-self.hid_timer>1000:
            self.hidden=False
            self.rect.centerx=WIDTH/2
            self.rect.bottom=HEIGHT-15
        self.speedx=0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx=-5
        if keys[pygame.K_RIGHT]:
            self.speedx=5
        if keys[pygame.K_SPACE]:
            self.shoot()    
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right=WIDTH
        if self.rect.left < 0:
            self.rect.left = 0    
     
    def shoot(self):
        now = pygame.time.get_ticks()
        if now-self.last_shot>self.shoot_delay:
            self.last_shot=now
            if self.power==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_snd.play()
            if self.power==2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_snd.play() 
            if self.power>=3:
                bullet3=Bullet2(self.rect.centerx,self.rect.bottom)  
                all_sprites.add(bullet3)
                bullets.add(bullet3)  
                laser_shoot.play()   
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org=random.choice(stone_images )
        self.image=self.image_org.copy()
        #self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*0.7/2)
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius,1)
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-200,-40)
        self.speedy=random.randrange(1,8)
        self.speedx=random.randrange(-3,3)
        self.rot=0
        self.rot_speed=random.randrange(-5,5)
        self.last_update=pygame.time.get_ticks()
    
    def rotation(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>50:
            self.last_update=now
            self.rot=(self.rot+self.rot_speed)%360
            self.new_image=pygame.transform.rotate(self.image_org,self.rot)
            old_center=self.rect.center
            self.image=self.new_image
            self.rect=self.image.get_rect()
            self.rect.center=old_center
    def update(self):
        self.rotation()
        self.rect.x+=self.speedx
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT+10 or self.rect.left<-20 or self.rect.right>WIDTH+20:
            self.rect.x=random.randrange(WIDTH-self.rect.width)
            self.rect.y=random.randrange(-200,-40)
            self.speedy=random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(laser_img,(23,50))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10

    def update(self):
        self.rect.y+=self.speedy
        #goes of the screen kills it
        if self.rect.bottom<0:
            self.kill()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #self.image=pygame.transform.scale(laser_img2,(166,15))
        self.image=laser_img2
        #self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-10

    def update(self):
        self.rect.y+=self.speedy
        #goes of the screen kills it
        if self.rect.bottom<0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explosion_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=75

    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(explosion_anim[self.size]):
                self.kill()
            else:
                center=self.rect.center
                self.image=explosion_anim[self.size][self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center        

class Shield(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=shield_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=1

    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(shield_anim[self.size]):
                self.kill()
            else:
                center=self.rect.center
                self.image=shield_anim[self.size][self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center        

class Pow(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(["shield","gun"])
        self.image=powerup_anim[self.type]
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.speedy=2

    def update(self):
        self.rect.y+=self.speedy
        #goes of the screen kills it
        if self.rect.top>HEIGHT:
            self.kill()

def show_go_screen():
    screen.blit(bggo, (0,0))
    screen.blit(astro2, (WIDTH -600, HEIGHT-700))
    #draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    #draw_text(screen, "Arrow keys move, Space to fire", 22,
              #WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
#load all graphics
BG=pygame.image.load(path.join(img_dir,"galaxy5.jpg")).convert()
player_img=pygame.image.load(path.join(img_dir,"ship2.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (35, 29))
player_mini_img.set_colorkey(BLACK)
laser_img=pygame.image.load(path.join(img_dir,"laser_red.png")).convert()
laser_img2=pygame.image.load(path.join(img_dir,"laser_blue.png"))
stone_images=[]
stones=["stone_b_L.png","stone_b_M.png","stone_r_L.png",
        "stone_r_M.png","stone_w_L.png","stone_w_M.png","stone_s2.png"]
for img in stones:
    stone_images.append(pygame.image.load(path.join(img_dir,img))) 
explosion_anim={}
explosion_anim["lg"]=[]
explosion_anim["sm"]=[]
explosion_anim["player"]=[]
for i in range(9):
    file_name="regularExplosion0{}.png".format(i)
    img=pygame.image.load(path.join(img_dir,file_name)).convert()
    img.set_colorkey(BLACK)
    img_lg=pygame.transform.scale(img,(95,95))
    explosion_anim["lg"].append(img_lg)
    img_sm=pygame.transform.scale(img,(40,40)) 
    explosion_anim["sm"].append(img_sm)      
    filename = 'sonic{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename))
    imgs=pygame.transform.scale(img,(400,400))
    #img.set_colorkey(BLACK)
    explosion_anim['player'].append(imgs)  

shield_anim={}    
shield_anim["shield"]=[]
for i in range(1,16):
    filename = 'b_{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename))
    imgs=pygame.transform.scale(img,(120,130))
    shield_anim['shield'].append(imgs)  

powerup_anim={}
powerup_anim["gun"]= pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()
powerup_anim["shield"]=  pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()

bggo=pygame.image.load(path.join(img_dir, "galaxy7.jpg")).convert()
astro2=pygame.image.load(path.join(img_dir, "astro3.png")).convert()
astro2.set_colorkey(BLACK)


#game sounds
shoot_snd=pygame.mixer.Sound(path.join(img_dir,"Fire 4.wav"))  
expl_sound= pygame.mixer.Sound(path.join(img_dir,"Explosion.wav")) 
shield_sound= pygame.mixer.Sound(path.join(img_dir,"Powerup26.wav")) 
powerup_sound=pygame.mixer.Sound(path.join(img_dir,"Powerup5.wav"))  
player_hitsound=pygame.mixer.Sound(path.join(img_dir,"Hit_Hurt4.wav")) 
laser_shoot=pygame.mixer.Sound(path.join(img_dir,"Laser_Shoot11.wav"))
bgmusic=pygame.mixer.music.load(path.join(img_dir,"electronic-senses-filter-12.mp3"))
pygame.mixer.music.play(-1)


# Game loop
game_over=True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over=False
        #adding sprite to groups     
        all_sprites = pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        powerups=pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score=0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()
    #check for collisions between two group of sprites
    hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score+=50-hit.radius
        expl_sound.play()
        expl=Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)
        if random.random()>0.9:
            power=Pow(hit.rect.center)
            all_sprites.add(power)
            powerups.add(power)
        newmob()
    #check for collisions between a sprite and group of sprite or sprite
    hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield-=hit.radius*1.2
        expl=Explosion(hit.rect.center,"sm")
        all_sprites.add(expl)
        player_hitsound.play()
        shld=Shield(player.rect.center,"shield")
        all_sprites.add(shld)
       
        newmob()
        if player.shield<=0:
           expl_sound.play()
           death_explosion=Explosion(player.rect.center,"player")
           all_sprites.add(death_explosion)
           player.hide()
           player.lives-=1
           player.shield=100
    #check if powerup hits the player
    hits=pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        if hit.type=="shield":
            player.shield+=random.randrange(10,30)
            shield_sound.play()
            if player.shield>=100:
                player.shield=100
        if hit.type=="gun":
            player.powerup()
            powerup_sound.play()        
    if player.lives==0 and not death_explosion.alive():
            game_over=True
            

    # Draw / render
    #screen.fill(WHITE)
    screen.blit(BG,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,"Score:"+str(score),25,WIDTH/2,10)
    draw_shield(screen,5,5,player.shield)
    draw_lives(screen,WIDTH-120,20,player.lives,player_mini_img)
    #if lost:
        #screen.blit(bggo,(WIDTH/2-bggo.get_width()/2,150))
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()