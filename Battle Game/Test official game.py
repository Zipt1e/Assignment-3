#Download pygame library first then import 
import pygame
import sys
import random

#Initialize a game 
pygame.init()

#Set frame rate
clock = pygame.time.Clock()
fps = 60

#Dimensions of the window 
bottom_panel = 200
WIDTH = 800
HEIGHT = 400 + bottom_panel


screen = pygame.display.set_mode((WIDTH,HEIGHT))

#Create game name 
pygame.display.set_caption('Assignement 3 - Battle Game')

#define game variables 
current_fighter = 1 
total_fighters = 2 
action_cooldown = 0 
action_wait_time = 90

#define fonts 
font = pygame.font.SysFont('Times New Roman', 24)

#define the colours for the font 
red = (255, 0, 0)
green = (0, 255, 0)

#Load images 
#Backgournd image 
background_img = pygame.image.load('Battle Game/img/Background/background.png').convert_alpha()
#Panel image 
panel_img = pygame.image.load('Battle Game/img/Panel/panel.png').convert_alpha()

#create fnuction for drawing text 
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#Function for drawing backgorund 
def draw_bg():
    screen.blit(background_img, (0,0))

#Function for drawing panel 
def draw_panel():
     screen.blit(panel_img, (0,HEIGHT - bottom_panel))
     #show knights health 
     draw_text(f'{knight.name} HP:{knight.hp}', font, green, 120, HEIGHT - bottom_panel +15)
     #show bandit health 
     draw_text(f'{bandit.name} HP:{bandit.hp}', font, green, 520, HEIGHT - bottom_panel +15)

#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions, lives):
        self.name = name     
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength 
        self.start_potions = potions
        self.lives = lives 
        self.alive = True 
        self.animation_list = []
        self.frame_index = 0 
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead 
        self.update_time = pygame.time.get_ticks()

        #load idle images 
        temp_list = []
        for i in range(1,8): 
            img = pygame.image.load(f'Battle Game/img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()/3, img.get_height()/3)) #This line is added in to reduce the size of the images as they too big 
            temp_list.append(img)
        self.animation_list.append(temp_list)

         #load attack images 
        temp_list = []
        for i in range(1,10): 
            img = pygame.image.load(f'Battle Game/img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()/3, img.get_height()/3)) #This line is added in to reduce the size of the images as they too big 
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list [self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        animation_cooldown = 100
        #Handle animation
        #Update image 
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update 
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation finishes, reset to the start 
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y 
        self.hp = hp 
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health on bar (green / red) 
        self.hp = hp
        #now ratio for green bar 
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 200 * ratio, 20))


knight = Fighter(100, 260, 'Knight', 30, 10, 3, 3)
bandit = Fighter(650, 270, 'Bandit', 20, 6, 1, 1)

bandit_list = []
bandit_list.append(bandit)

knight_health_bar = HealthBar(100, HEIGHT - bottom_panel +60, knight.hp, knight.max_hp)
bandit_health_bar = HealthBar(500, HEIGHT - bottom_panel +60, bandit.hp, bandit.max_hp)

############ Main game loop ############
run = True 
while run:

    clock.tick(fps)

    #Draw backgournd 
    draw_bg()

    #Draw panel 
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit_health_bar.draw(bandit.hp)

 # Draw fighters 
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

     # Player action 
    if knight.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # Look for player action
                # Attack 
                knight.attack(bandit)
                current_fighter += 1
                action_cooldown = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False 

    pygame.display.update()

pygame.quit()
sys.exit()