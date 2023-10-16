import pygame,sys,random
if __name__=='__main__':
    pygame.init()
    red = (255,0,0)
    green = (0,255,0)
    tela_x=600
    tela_y=800
    rows = 5
    cols = 5
    pygame.display.set_caption(('space invanders'))
    tela=pygame.display.set_mode((tela_x,tela_y))
    clock=pygame.time.Clock()
    bg = pygame.image.load("bg.png")
    class Aliens(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("alien" + str(random.randint(1,5)) + ".png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.move_d = 1
            self.move_c = 0
        def update(self):
            self.rect.x += self.move_d
            self.move_c += 1
            if abs(self.move_c) > 75:
                self.move_d *= -1
                self.move_c *= self.move_d

    class Balas(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("bullet.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
        def update(self):
            self.rect.y -= 5
            if self.rect.bottom < 0:
                self.kill()
    class Nave(pygame.sprite.Sprite):
        def __init__(self,x,y,vida):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("spaceship.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x,y]
            self.vida_c = vida
            self.vida_f = vida
            self.utimo_tiro = pygame.time.get_ticks()
        def update(self):
            speed = 8
            cooldown = 500
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < tela_x:
                self.rect.x += speed
            time_now = pygame.time.get_ticks()
            if key[pygame.K_SPACE] and time_now - self.utimo_tiro > cooldown:
                bala = Balas(self.rect.centerx, self.rect.top)
                bala_group.add(bala)
                self.utimo_tiro = time_now
            pygame.draw.rect(tela,red,(self.rect.x,(self.rect.bottom + 10),self.rect.width,15))
            if self.vida_f > 0:
                pygame.draw.rect(tela, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_f/self.vida_c)), 15))
    nave_group = pygame.sprite.Group()
    bala_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    def create_aliens():
        for row in range(rows):
            for item in range(cols):
                alien = Aliens(100 + item * 100, 100 + row * 70)
                alien_group.add(alien)
    create_aliens()
    nave = Nave(int(tela_x / 2),tela_y - 100, 3)
    nave_group.add(nave)

    def draw_bg():
        tela.blit(bg,(0,0))
    while True:
        draw_bg()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        nave.update()
        alien_group.update()
        bala_group.update()
        alien_group.draw(tela)
        nave_group.draw(tela)
        bala_group.draw(tela)
        pygame.display.update()
        tela.fill((30,30,30))
        clock.tick(60)