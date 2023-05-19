import pygame
from sys import exit
from random import randint

pygame.init()

screen = pygame.display.set_mode((450, 650))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

background = pygame.image.load('images/background.png').convert()
background = pygame.transform.scale(background, (500, 700))

bird_image = pygame.image.load("images/flappy_bird.png").convert_alpha()
pygame.display.set_icon(bird_image)

game_active = True
score = bird_gravity = highest_score = 0
timer = pygame.time.get_ticks()    

font1 = pygame.font.Font('font/flappy-font.ttf', 60)  
score_label = font1.render(f'{score}', False, 'white')

font2 = pygame.font.Font('font/flappy-font.ttf', 30)     

wing_sound = pygame.mixer.Sound('audio/sfx_wing.wav')
score_sound = pygame.mixer.Sound('audio/sfx_point.wav')
hit_sound = pygame.mixer.Sound('audio/sfx_hit.wav')

class FlappyBird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.image = pygame.transform.scale(self.image, (55, 40))
        self.rect = self.image.get_rect()
        self.rect.x = 10

class CollideSurface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (500, 110))
        self.rect = self.image.get_rect()
        self.rect.y = 540

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        super().__init__()
        self.image = pygame.image.load('images/pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 700))
        self.rect = self.image.get_rect()
        if flip: 
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect.x = x
        self.rect.y = y

def pipe(pipe_up, pipe_down, x = 470):
    y_cord = randint(-630, -358)
    y_cord -= pipe_up.rect.y
    pipe_up.rect.y += y_cord
    pipe_down.rect.y += y_cord
    pipe_down.rect.x = x                             
    pipe_up.rect.x = x

bird_object = FlappyBird()
collide_surf = CollideSurface()

pipe_up1 = Pipe(270, -488, 1)
pipe_down1 = Pipe(270, 340, 0)

pipe_up2 = Pipe(540, -610, 1)
pipe_down2 = Pipe(540, 218, 0)

bird_container = pygame.sprite.Group()
pipe_container = pygame.sprite.Group()
surface_container = pygame.sprite.Group()

bird_container.add(bird_object)

pipe_container.add(pipe_down1)
pipe_container.add(pipe_up1)
pipe_container.add(pipe_down2)
pipe_container.add(pipe_up2)

surface_container.add(collide_surf)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            if game_active:
                wing_sound.play()
                bird_gravity = -7
            else:
                score = 0
                score_label = font1.render('0', False, 'white')
                bird_gravity = 0
                bird_object.rect.y = 0                          # type: ignore
                game_active = True                          
                pipe(pipe_up1, pipe_down1, 270)
                pipe(pipe_up2, pipe_down2, 540)

        if event.type==pygame.MOUSEBUTTONDOWN and game_active:
            wing_sound.play()
            bird_gravity = -7

    if game_active:
        bird_gravity += 0.5
        bird_object.rect.y += bird_gravity                      # type: ignore
        screen.blit(background, (0, 0))
        pipe_container.draw(screen)
        bird_container.draw(screen)
        surface_container.draw(screen) 
        screen.blit(score_label, (225, 30))

        pipe_down1.rect.x -= 2                                  # type: ignore
        pipe_up1.rect.x -= 2                                    # type: ignore
        pipe_down2.rect.x -= 2                                  # type: ignore
        pipe_up2.rect.x -= 2                                    # type: ignore
        
        if pipe_down1.rect.right < 0:                           # type: ignore
            pipe(pipe_up1, pipe_down1)
        elif pipe_down2.rect.right < 0:                         # type: ignore
            pipe(pipe_up2, pipe_down2)

        if (bird_object.rect.right==pipe_down1.rect.centerx or  # type: ignore
            bird_object.rect.right==pipe_down2.rect.centerx):   # type: ignore
            score_sound.play()
            score += 1
            score_label = font1.render(f'{score}', False, 'white')
        
        if (pygame.sprite.groupcollide(bird_container, pipe_container, False, False) or 
            pygame.sprite.groupcollide(bird_container, surface_container, False, False)):
            hit_sound.play()
            screen.fill((51, 165, 255))
            game_active = False
            if highest_score < score:
                highest_score = score

    else:
        screen.blit(font2.render(f'Score: {score}', False, 'white'), (150, 30))
        screen.blit(font2.render(f'Highest Score: {highest_score}', False, 'white'), (90, 70))
        screen.blit(font2.render('Press space to continue...', False, 'white'), (30, 200))
    
    pygame.display.update()
    clock.tick(60)
