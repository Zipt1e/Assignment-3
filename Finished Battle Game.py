#Download pygame library first then import 
import pygame
import sys
import random
import button


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

#define game variables 
current_fighter = 1 
total_fighters = 2
action_cooldown = 0 
action_wait_time = 90
attack = False
potion = False
potion_effect = 15 
clicked = False 
game_over = 0

#Create game name 
pygame.display.set_caption('Assignment 3 - Battle Game')

#define fonts 
font = pygame.font.SysFont('Times New Roman', 26,)

#define the colours for the font 
red = (255, 0, 0)
green = (0, 255, 0)

#Load images 
#Backgournd image 
background_img = pygame.image.load('Battle Game/img/Background/background.png').convert_alpha()
#Panel image 
panel_img = pygame.image.load('Battle Game/img/Panel/panel.png').convert_alpha()
#button
potion_img = pygame.image.load('Battle Game/img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('Battle Game/img/Icons/potion.png').convert_alpha()

victory_img = pygame.image.load('Battle Game/img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('Battle Game/img/Icons/defeat.png').convert_alpha()
#arrow image 
arrow_img = pygame.image.load('Battle Game/img/Arrow/1.png').convert_alpha() 

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
     knight_health_bar = draw_text(f'{knight.name} HP:{knight.hp}', font, green, 120, HEIGHT - bottom_panel +15)
     #show bandit health 
     bandit_health_bar = draw_text(f'{bandit.name} HP:{bandit.hp}', font, green, 520, HEIGHT - bottom_panel +15)

#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions, lives):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.lives = lives
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()

        #load idle images 
        temp_list = []
        for i in range(1,2): 
            img = pygame.image.load(f'Battle Game/img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()/3, img.get_height()/3)) #This line is added in to reduce the size of the images as they too big 
            temp_list.append(img)
        self.animation_list.append(temp_list)

#### ADD THIS 
        #load hurt images 
        temp_list = []
        for i in range(1,4): 
            img = pygame.image.load(f'Battle Game/img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()/3, img.get_height()/3)) #This line is added in to reduce the size of the images as they too big 
            temp_list.append(img) 
            self.animation_list.append(temp_list) 
        #load death images 
        temp_list = []
        for i in range(1,5): 
            img = pygame.image.load(f'Battle Game/img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()/3, img.get_height()/3)) #This line is added in to reduce the size of the images as they too big 
            temp_list.append(img) 
            self.animation_list.append(temp_list) 
 ### END of add 

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
        # Handle animation
        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation finishes, reset to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
## END add 

    def idle (self):
        self.action = 0
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        # do some damage to the enemy
        rand = random.randint(-10,-1)
        damage = max(0, self.strength + rand)
        target.hp -= damage
### ADD 
        #run enemy hurt animation 
        target.hurt()
##END ADD 
    
        #check if target has died 
        if target.hp < 1: 
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text) 



        # Update the health bar after the attack
        knight_health_bar.hp = target.hp
        bandit_health_bar.hp = target.hp
        
        #set variables to attack animation 
        self.action = 1 
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()

## ADD this   
        #set variables to attack animation 
    def hurt (self):
        self.action = 2
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()
## end of addition 
        
## add me 
    def death (self):
        self.action = 3
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()
## end of add 


    def draw(self):
        screen.blit(self.image, self.rect)

class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Battle Game/img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.x -= -15
		if pygame.sprite.spritecollide(bandit, bullet_group, True):
			self.kill()
    

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y 
        self.hp = hp 
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health on bar (green / red) 
        self.hp=hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 200 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0

	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()


damage_text_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


knight = Fighter(100, 260, 'Knight', 30, 10, 3, 3)
bandit = Fighter(650, 270, 'Bandit', 20, 6, 1, 1)

bandit_list = []
bandit_list.append(bandit)

knight_health_bar = HealthBar(100, HEIGHT - bottom_panel +60, knight.hp, knight.max_hp)
bandit_health_bar = HealthBar(500, HEIGHT - bottom_panel +60, bandit.hp, bandit.max_hp)

potion_button = button.Button(screen, 100, HEIGHT - bottom_panel + 90, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)
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

#draw the damage text
    
    bullet_group.update()
    damage_text_group.update()
    damage_text_group.draw(screen)
    bullet_group.draw(screen)

    #control player actions 
    #reset action variables 
    attack = False 
    potion = False
    target = None
    pygame.mouse.set_visible(True) #make mouse visible when not on the bandit 
    pos = pygame.mouse.get_pos()
    if bandit.rect.collidepoint(pos):
        #hide mouse 
        pygame.mouse.set_visible(False)
        #show sword in place of mouse cursor 
        screen.blit(arrow_img, pos)
        if clicked == True:
            attack = True 
            target = bandit
            bullet = Bullets(knight.rect.right, knight.rect.centery)
            bullet_group.add(bullet)
	
    if potion_button.draw():
        potion = True
	#show number of potions remaining
    draw_text(str(knight.potions), font, red, 150, HEIGHT - bottom_panel + 90)

 
    # Player action 
    if knight.alive and current_fighter == 1:
        action_cooldown += 1
        if action_cooldown >= action_wait_time:
                # Look for player action
                # Attack 
            if attack == True and target != None:
                knight.attack(bandit)
                current_fighter += 1
                action_cooldown = 0 # Reset the cooldown
            if potion == True:
                if knight.potions > 0:
							#check if the potion would heal the player beyond max health
                        if knight.max_hp - knight.hp > potion_effect:
                            heal_amount = potion_effect
                        else:
                                heal_amount = knight.max_hp - knight.hp
                                knight.hp += heal_amount
                                knight.potions -= 1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                else:
                    game_over = -1

    #enemy action 
    for bandit in (bandit_list):
        if bandit.alive == True:
            if current_fighter == 2:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
#check if bandit needs to heal first
                    if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
						#check if the potion would heal the bandit beyond max health
                        if bandit.max_hp - bandit.hp > potion_effect:
                            heal_amount = potion_effect
                        else:
                            heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
						#attack
                    else:
                #attack 
                        bandit.attack(knight)
                        current_fighter += 1
                        action_cooldown = 0 
        else:
            current_fighter += 1 


    #reset when fighters have had a turn 
    if current_fighter > total_fighters:
        current_fighter = 1
	#check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1


	#check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0



    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True 
        else:
            clicked = False 

    pygame.display.update()

  
pygame.quit()


