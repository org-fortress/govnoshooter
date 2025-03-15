from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"), (700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 665:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", 15, self.rect.centerx - 6, self.rect.top, 15, 20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.x = randint(80, 500 - 80)
            self.rect.y = 0
            self.speed = randint(2, 4)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()



font.init()
font1 = font.SysFont('Arial', 36)
player = Player('rocket.png', 10, 400, 400, 65, 65)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(2, 4), randint(0, 635), 0, 65, 65)
    monsters.add(enemy)
clock = time.Clock()
you_lose = font1.render('YOU LOSE!', 1, (255,0,0))
you_win = font1.render('YOU WIN!!!!', 1, (255, 231, 0))
FPS = 60
game = True
finish = False
while game:
    if finish != True:
        window.blit(background, (0,0))
        monsters.update()
        monsters.draw(window)
        player.update()
        player.reset()
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        text_score = font1.render('Счёт: ' + str(score), 1, (255,255,255))
        window.blit(text_lose, (0,0))
        window.blit(text_score, (0, 30))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(you_lose, (250,210))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for monster in sprites_list:
            score += 1
            enemy = Enemy('ufo.png', randint(2, 4), randint(0, 635), 0, 65, 65)
            monsters.add(enemy)
        if score > 10:
            finish = True
            window.blit(you_win, (250,250))
        bullets.update()
        bullets.draw(window)
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    display.update()