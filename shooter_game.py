#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, weight, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (weight, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
    def fire(self):
        bullet=Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15 )
        bullets.add(bullet)

        
lost = 0 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()
        
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
        




player = Player('rocket.png',350,400,80,100,10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,10))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, win_width-80), -40, 80, 50, randint(1,10))
    asteroids.add(asteroid)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
win = font2.render('YOU WIN', True, (60, 219, 15))
lose = font2.render('YOU LOSE', True, (219, 15, 15))
reload1 = font2.render('Wait, reload...', True, (219, 15, 15))

rel_time = False
num_fire=0
score=0
clock = time.Clock()
FPS = 60
finish = False
run=True
while run:
    window.blit(background, (0, 0))
    player.reset()
    
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire +=1
                    player.fire()
                    fire_sound.play()
                
                if num_fire >=5 and rel_time ==  False:
                    rel_time = True
                    start_time = timer()
    


                 


    
    if finish != True:
        text_score = font1.render('Счет: ' + str(score), 1, (255, 255, 255))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_score, (10,10))
        window.blit(text_lose, (10,40))
        if sprite.spritecollide(player, monsters, False) or lost > 3:
            finish = True
        
        if sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose,(200,200))
            
        collides_list = sprite.groupcollide(monsters, bullets, True,True)
        for i in collides_list:
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,10))
            monsters.add(monster)
            score+=1
        if score >= 10:
            finish = True
            window.blit(win,(300,225))
        
        if rel_time == True:
            cur_time = timer()
            if cur_time - start_time < 3:
                window.blit(reload1, (260,460))
            else:
                num_fire = 0
                rel_time = False


          
        
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        display.update()
        time.delay(50)
    time.delay(50)

    