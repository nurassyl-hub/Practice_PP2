import pygame, sys, os, json
from pygame.locals import *
import random, time

def load_data(filename, default):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return default

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Initialize files
settings = load_data("racer/settings.json", {"sound": True, "car_color": "blue", "difficulty": "Medium"})
leaderboard = load_data("racer/scores.json", [])

#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("racer/AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")

class Button:
    def __init__(self, text, x, y, width, height, color):
        # Defines the physical area where the mouse can click
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface):
        # Draws the colored rectangle on the screen
        pygame.draw.rect(surface, self.color, self.rect)
        # Places the text on top of the rectangle
        txt_surface = font_small.render(self.text, True, WHITE)
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        # Checks if the mouse coordinates (pos) are inside our button's rectangle
        return self.rect.collidepoint(pos)
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):

        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/oil_spills.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        self.rect.move_ip(0, SPEED)
        # Reset if it goes off screen
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.value = 1
    def move(self):
        self.rect.move_ip(0, 5)
        if (self.rect.top > 600):
            self.value = random.randint(1, 3)
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])
        # You can replace these with specific images like "racer/nitro.png"
        self.image = pygame.image.load("racer/"+ self.type + ".png") 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.active = False

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.kill()
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_path = f"racer/Player_{settings['car_color']}.png"
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,3)
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
def get_username():
    user_name = ""
    entering = True
    while entering:
        DISPLAYSURF.fill(WHITE)
        msg = font_small.render("Enter Name: " + user_name, True, BLACK)
        DISPLAYSURF.blit(msg, (100, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN: entering = False
                elif event.key == K_BACKSPACE: user_name = user_name[:-1]
                else: user_name += event.unicode
            if event.type == QUIT: pygame.quit(); sys.exit()
    return user_name
def show_settings():
    showing = True
    # Buttons for Difficulty
    easy_btn = Button("Easy", 50, 100, 80, 40, GREEN)
    med_btn = Button("Med", 150, 100, 80, 40, BLUE)
    hard_btn = Button("Hard", 250, 100, 80, 40, RED)
    
    # Buttons for Car Color
    red_car = Button("Red", 50, 250, 80, 40, RED)
    blue_car = Button("Blue", 150, 250, 80, 40, BLUE)
    green_car = Button("Green", 250, 250, 80, 40, GREEN)
    
    # Toggle Sound & Back
    sound_btn = Button("Sound: ON" if settings["sound"] else "Sound: OFF", 100, 350, 200, 40, BLACK)
    back_btn = Button("Save & Back", 100, 450, 200, 40, BLACK)

    while showing:
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(font_small.render(f"Difficulty: {settings['difficulty']}", True, BLACK), (50, 70))
        DISPLAYSURF.blit(font_small.render(f"Car Color: {settings['car_color']}", True, BLACK), (50, 220))
        
        for b in [easy_btn, med_btn, hard_btn, red_car, blue_car, green_car, sound_btn, back_btn]:
            b.draw(DISPLAYSURF)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if easy_btn.is_clicked(event.pos): settings["difficulty"] = "Easy"
                if med_btn.is_clicked(event.pos): settings["difficulty"] = "Medium"
                if hard_btn.is_clicked(event.pos): settings["difficulty"] = "Hard"
                if red_car.is_clicked(event.pos): settings["car_color"] = "red"
                if blue_car.is_clicked(event.pos): settings["car_color"] = "blue"
                if green_car.is_clicked(event.pos): settings["car_color"] = "green"
                if sound_btn.is_clicked(event.pos):
                    settings["sound"] = not settings["sound"]
                    sound_btn.text = "Sound: ON" if settings["sound"] else "Sound: OFF"
                if back_btn.is_clicked(event.pos):
                    save_data("racer/settings.json", settings) # Save preferences
                    showing = False
def show_leaderboard():
    showing = True
    back_btn = Button("Back", 150, 500, 100, 40, BLUE)
    while showing:
        DISPLAYSURF.fill(WHITE)
        title = font_small.render("TOP 10 LEADERBOARD", True, BLACK)
        DISPLAYSURF.blit(title, (100, 20))
        
        for i, entry in enumerate(leaderboard[:10]):
            text = f"{i+1}. {entry['name']} - {entry['score']} pts ({entry['dist']}m)"
            DISPLAYSURF.blit(font_small.render(text, True, BLACK), (50, 60 + i*30))
        
        back_btn.draw(DISPLAYSURF)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and back_btn.is_clicked(event.pos): showing = False
            if event.type == QUIT: pygame.quit(); sys.exit()

def game_loop(username):
    global SPEED, COIN, DISTANCE
    # Reset Variables
    SPEED = 5 if settings['difficulty'] == "Medium" else (3 if settings['difficulty'] == "Easy" else 7)
    COIN = 0
    DISTANCE = 0                   
    #Setting up Sprites        
    P1 = Player()
    E1 = Enemy()
    C1 = Coin()
    O1 = Obstacle()
    #Creating Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coins = pygame.sprite.Group()
    coins.add(C1)
    obstacles = pygame.sprite.Group()
    obstacles.add(O1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(C1)
    all_sprites.add(O1)
    #Adding a new User event 
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1500)
    # Timer to spawn a power-up every 10 seconds
    SPAWN_POWERUP = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_POWERUP, 5000)
    b1_y = 0
    b2_y = -600
    power_ups = pygame.sprite.Group()
    active_shield = False
    nitro_finish_time = 0
    current_powerup_img = None
    running = True
    #Game Loop
    while running:
        b1_y += SPEED
        b2_y += SPEED
        current_time = time.time()
        #Cycles through all events occurring  
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.2 
            if event.type == SPAWN_POWERUP:
                new_power = PowerUp()
                power_ups.add(new_power)
                all_sprites.add(new_power) 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        DISPLAYSURF.blit(background, (0, b1_y))
        DISPLAYSURF.blit(background, (0, b2_y))
        if b1_y > 600:
            b1_y = -600
            DISTANCE += 30
        elif b2_y > 600:
            b2_y = -600
            DISTANCE += 30
        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        DISPLAYSURF.blit(font_small.render(str(C1.value), True, BLACK), C1.rect.center)
        DISPLAYSURF.blit(font_small.render(f'{COIN} coin', True, BLACK), (330,10))
        DISPLAYSURF.blit(font_small.render(f'{DISTANCE} m', True, BLACK), (330,30))
        # Check for Nitro expiration
        if nitro_finish_time !=0:
            DISPLAYSURF.blit(font_small.render(f'{nitro_finish_time - current_time}', True, BLACK), (300,50))
            if current_time> nitro_finish_time:
                SPEED -= 5  # Return to normal speed
                nitro_finish_time = 0
                new_power.active = False
        
        if pygame.sprite.spritecollideany(P1, coins):
            COIN += C1.value
            C1.rect.top = 601
            SPEED += 0.2
        if pygame.sprite.spritecollideany(P1, obstacles):
            #slow the player down
            SPEED = max(2, SPEED - 1) 
            O1.rect.top = 601
        #To be run if collision occurs between Player and Power Up
        p_hit = pygame.sprite.spritecollideany(P1, power_ups)
        if p_hit:
            current_powerup_img = p_hit.image
            if p_hit.type == "nitro":
                SPEED += 5
                nitro_finish_time = current_time + 3 # 3 seconds duration
                active_shield = False
            elif p_hit.type == "shield":
                active_shield = True
                nitro_finish_time = 0
            elif p_hit.type == "repair":
                active_shield = False
                nitro_finish_time = 0
            #Clears the nearest enemy
                for enemy in enemies:
                    enemy.rect.top = 601
            p_hit.kill()
        if active_shield:
        # If you have a specific shield icon, blit it here
            DISPLAYSURF.blit(current_powerup_img, (330, 70)) 
        elif nitro_finish_time > current_time:
        # Show the nitro icon while it's active
            DISPLAYSURF.blit(current_powerup_img, (330, 70))
        #To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollideany(P1, enemies):
            if active_shield:
                active_shield = False  # Shield absorbs the hit
                # Reset enemy position 
                for enemy in enemies:
                    enemy.rect.top = 601
            else:
                if settings["sound"]:
                    pygame.mixer.Sound('racer/crash.wav').play()
                final_score = (COIN * 100) + (DISTANCE // 10) # Score Calculation
                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(game_over, (30,250))
                DISPLAYSURF.blit(font_small.render(f'COINS: {COIN}', True, BLACK), (30, 350))
                DISPLAYSURF.blit(font_small.render(f'DISTANCE: {DISTANCE}', True, BLACK), (30, 370))
                DISPLAYSURF.blit(font_small.render(f'Score: {final_score}', True, BLACK), (30, 390))
                for entity in all_sprites:
                    entity.kill()
                pygame.display.update()
                time.sleep(3)
                running = False
        pygame.display.update()
        FramePerSec.tick(FPS)
    leaderboard.append({"name": username, "score": final_score, "dist": DISTANCE})
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    save_data("racer/scores.json", leaderboard[:10])
    return final_score
def main_menu():
    play_btn = Button("Play", 150, 150, 100, 50, GREEN)
    high_btn = Button("Scores", 150, 220, 100, 50, BLUE)
    sett_btn = Button("Settings", 150, 290, 100, 50, BLACK)
    quit_btn = Button("Quit", 150, 360, 100, 50, RED)
    while True:
        DISPLAYSURF.fill(WHITE)
        play_btn.draw(DISPLAYSURF)
        high_btn.draw(DISPLAYSURF)
        quit_btn.draw(DISPLAYSURF)
        sett_btn.draw(DISPLAYSURF)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if play_btn.is_clicked(event.pos):
                    name = get_username()
                    game_loop(name)
                if high_btn.is_clicked(event.pos):
                    show_leaderboard()
                if sett_btn.is_clicked(event.pos): 
                    show_settings()
                if quit_btn.is_clicked(event.pos):
                    pygame.quit(); sys.exit()
            if event.type == QUIT:
                pygame.quit(); sys.exit()

main_menu()