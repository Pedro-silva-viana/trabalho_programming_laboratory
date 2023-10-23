import pygame,sys,random
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

if __name__=='__main__':
    pygame.init()
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    tela_x=600
    tela_y=800

    rows = 5
    cols = 5
    alien_cooldawn = 1000
    last_alien_shot = pygame.time.get_ticks()
    countdown = 3
    gameover = 0

    last_count = pygame.time.get_ticks()

    fonte30 = pygame.font.SysFont('Constantia', 30)
    fonte40 = pygame.font.SysFont('Constantia', 40)

    def texto(texto, fonte, cor, x, y):
        imagem = fonte.render(texto, True, cor)
        tela.blit(imagem, (x, y))

    pygame.display.set_caption(('space invanders'))
    tela=pygame.display.set_mode((tela_x,tela_y))
    clock=pygame.time.Clock()
    bg = pygame.image.load("bg.png")

    explosion_fx = pygame.mixer.Sound('explosion.wav')
    explosion_fx.set_volume(0.25)

    explosion2_fx = pygame.mixer.Sound('explosion2.wav')
    explosion2_fx.set_volume(0.25)

    laser_fx = pygame.mixer.Sound('laser.wav')
    laser_fx.set_volume(0.25)

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

    class Explosao(pygame.sprite.Sprite):
            def __init__(self, x, y, tamanho):
                pygame.sprite.Sprite.__init__(self)
                self.imagens = []

                for i in range(1, 6):
                    imagem = pygame.image.load(f'exp{i}.png')
                    if tamanho == 1:
                        imagem = pygame.transform.scale(imagem, (20, 20))
                    if tamanho == 2:
                        imagem = pygame.transform.scale(imagem, (40, 40))
                    if tamanho == 3:
                        imagem = pygame.transform.scale(imagem, (160, 160))
                    
                    self.imagens.append(imagem)

                self.index = 0
                self.image = self.imagens[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = [x, y]
                self.contador = 0


            def update(self):
                velocidade_explosao = 3
                self.contador += 1

                if self.contador >= velocidade_explosao and self.index < len(self.imagens) - 1:
                    self.contador = 0
                    self.index += 1
                    self.image = self.imagens[self.index]

                if self.contador >= velocidade_explosao and self.index >= len(self.imagens) - 1:
                    self.kill()

    class Abalas(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("alien_bullet.png")
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
        def update(self):
            self.rect.y += 3
            if self.rect.top > tela_y:
                self.kill()
            if pygame.sprite.spritecollide(self, nave_group, False):
                self.kill()
                explosion2_fx.play()
                nave.vida_f -= 1
                explosao = Explosao(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosao)
                     
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
            if pygame.sprite.spritecollide(self, alien_group, True):
                self.kill()
                explosion_fx.play()
                explosao = Explosao(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosao)

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
            gameover = 0
            cooldown = 500
            key = pygame.key.get_pressed()
            if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.rect.left > 0:
                self.rect.x -= speed
            if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.rect.right < tela_x:
                self.rect.x += speed
            time_now = pygame.time.get_ticks()
            if key[pygame.K_SPACE] and time_now - self.utimo_tiro > cooldown:
                laser_fx.play()
                bala = Balas(self.rect.centerx, self.rect.top)
                bala_group.add(bala)
                self.utimo_tiro = time_now
            pygame.draw.rect(tela,red,(self.rect.x,(self.rect.bottom + 10),self.rect.width,15))
            if self.vida_f > 0:
                pygame.draw.rect(tela, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_f/self.vida_c)), 15))
            elif self.vida_f <= 0:
                explosao = Explosao(self.rect.centerx, self.rect.centery, 3)
                explosion_group.add(explosao)
                self.kill()
                gameover = -1
            return gameover

    nave_group = pygame.sprite.Group()
    abala_group = pygame.sprite.Group()
    bala_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
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

        if countdown == 0:
            time_now = pygame.time.get_ticks()
            if time_now - last_alien_shot > alien_cooldawn and len(abala_group) < 5 and len(alien_group) > 0:
                attacking_alien = random.choice(alien_group.sprites())
                abala = Abalas(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                abala_group.add(abala)
                lest_alien_shot = time_now

            if len(alien_group) == 0:
                gameover = 1

            if gameover == 0:
                gameover = nave.update()

                alien_group.update()
                abala_group.update()
                bala_group.update()
            else:
                if gameover == -1:
                    texto('VOCÊ PERDEU!', fonte40, white, int(tela_x / 2 - 140), int(tela_y / 2 + 50))
                else:
                    texto('VOCÊ VENCEU!', fonte40, white, int(tela_x / 2 - 140), int(tela_y / 2 + 50))
        
        if countdown > 0:
            texto('PREPARE-SE!', fonte40, white, int(tela_x / 2 - 110), int(tela_y / 2 + 50))
            texto(str(countdown), fonte40, white, int(tela_x / 2 - 10), int(tela_y / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

        explosion_group.update()

        abala_group.draw(tela)
        alien_group.draw(tela)
        nave_group.draw(tela)
        bala_group.draw(tela)
        explosion_group.draw(tela)

        pygame.display.update()
        tela.fill((30,30,30))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()