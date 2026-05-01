import pygame
import random
import sys
from pygame.locals import *
import json

SETTINGS_FILE = "snake/settings.json"
def load_settings():
    default_settings = {"grid": True, "sound": True, "snake_color": "GREEN"}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError):
        return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
# --- Constants & Configuration ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE 
pygame.init()
# Assets
font_large = pygame.font.Font(None, 74)
font_med = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 # --- Constants & Configuration ---

COLORS = {

    "BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "RED": (255, 0, 0),

    "GREEN": (0, 255, 0), "YELLOW": (255, 255, 0), "CYAN": (0, 255, 255),

    "PURPLE": (255, 0, 255), "LIGHT_BLUE": (100, 200, 255), "DARK_GREY": (20, 20, 20), "DARK_RED": (139, 0, 0), "BLUE": (0, 0, 255)

}


# Directions

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
def show_settings():
    settings = load_settings()
    running = True
    
    while running:
        screen.fill(COLORS["WHITE"])
        
        # Title
        title = font_large.render("SETTINGS", True, COLORS["BLACK"])
        screen.blit(title, (260, 50))

        # Define Buttons with exact coordinates
        # Toggles
        grid_txt = f"Grid: {'ON' if settings['grid'] else 'OFF'}"
        sound_txt = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        
        grid_btn = Button(grid_txt, 300, 150, 200, 50, COLORS["DARK_GREY"])
        sound_btn = Button(sound_txt, 300, 220, 200, 50, COLORS["DARK_GREY"])
        
        # Color Pickers (Small squares)
        color_label = font_med.render("Snake Color:", True, COLORS["BLACK"])
        screen.blit(color_label, (300, 300))
        
        green_btn = Button("", 300, 340, 40, 40, COLORS["GREEN"])
        cyan_btn  = Button("", 360, 340, 40, 40, COLORS["CYAN"])
        purple_btn = Button("", 420, 340, 40, 40, COLORS["PURPLE"])
        
        # Save Button
        save_btn = Button("Save & Back", 300, 450, 200, 50, COLORS["BLUE"])

        # Draw everything
        grid_btn.draw(screen)
        sound_btn.draw(screen)
        green_btn.draw(screen)
        cyan_btn.draw(screen)
        purple_btn.draw(screen)
        save_btn.draw(screen)

        # Highlight selected color
        current_col = COLORS[settings['snake_color']]
        selector_map = {"GREEN": 300, "CYAN": 360, "PURPLE": 420}
        pygame.draw.rect(screen, COLORS["BLACK"], (selector_map[settings['snake_color']], 340, 40, 40), 3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if grid_btn.is_clicked(event.pos):
                    settings["grid"] = not settings["grid"]
                if sound_btn.is_clicked(event.pos):
                    settings["sound"] = not settings["sound"]
                if green_btn.is_clicked(event.pos):
                    settings["snake_color"] = "GREEN"
                if cyan_btn.is_clicked(event.pos):
                    settings["snake_color"] = "CYAN"
                if purple_btn.is_clicked(event.pos):
                    settings["snake_color"] = "PURPLE"
                if save_btn.is_clicked(event.pos):
                    save_settings(settings)
                    running = False

def draw_grid(surface):
    # Grey color for subtle lines
    grid_color = (40, 40, 40) 

    # Draw vertical lines
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, grid_color, (x, 0), (x, SCREEN_HEIGHT))
        
    # Draw horizontal lines
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, grid_color, (0, y), (SCREEN_WIDTH, y))
def get_username():
    user_name = ""
    entering = True
    while entering:
        screen.fill(COLORS["WHITE"])
        msg = font_small.render("Enter Name: " + user_name, True, COLORS["BLACK"])
        screen.blit(msg, (100, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN: entering = False
                elif event.key == K_BACKSPACE: user_name = user_name[:-1]
                else: user_name += event.unicode
            if event.type == QUIT: pygame.quit(); sys.exit()
    return user_name

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
        txt_surface = font_small.render(self.text, True, COLORS["WHITE"])
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        # Checks if the mouse coordinates (pos) are inside our button's rectangle
        return self.rect.collidepoint(pos)
class Snake:

    def __init__(self):

        mid_x, mid_y = (GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2) * GRID_SIZE

        self.positions = [[mid_x, mid_y], [mid_x - GRID_SIZE, mid_y], [mid_x - 2*GRID_SIZE, mid_y]]

        self.direction = RIGHT

        self.grow_flag = False

        self.has_shield = False


    def move(self):

        new_head = [self.positions[0][0] + self.direction[0] * GRID_SIZE,

                    self.positions[0][1] + self.direction[1] * GRID_SIZE]

        self.positions.insert(0, new_head)

        if not self.grow_flag:

            self.positions.pop()

        else:

            self.grow_flag = False


    def change_direction(self, new_dir):

        # Prevent 180-degree turns

        if (new_dir[0] != -self.direction[0] or new_dir[1] != -self.direction[1]):

            self.direction = new_dir


    def shrink(self, amount):

        for _ in range(amount):

            if len(self.positions) > 1:

                self.positions.pop()


    def draw(self, surface):

        for i, pos in enumerate(self.positions):

            color = COLORS["YELLOW"] if self.has_shield else COLORS[snake_color]

            pygame.draw.rect(surface, color, (*pos, GRID_SIZE, GRID_SIZE))

            border = COLORS["WHITE"]

            pygame.draw.rect(surface, border, (*pos, GRID_SIZE, GRID_SIZE), 1)


class PowerUp:

    def __init__(self):

        self.active_on_field = False

        self.position = [0, 0]

        self.spawn_time = 0

        self.lifetime = 8000  # 8 seconds on field

        self.type = None # "SPEED", "SLOW", or "SHIELD"


    def spawn(self, forbidden):

        self.type = random.choice(["SPEED", "SLOW", "SHIELD"])

        self.color = COLORS["WHITE"]

        while True:

            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

            if pos not in forbidden:

                self.position, self.spawn_time, self.active_on_field = pos, pygame.time.get_ticks(), True

                break


    def draw(self, surface):

        if self.active_on_field:

            pygame.draw.rect(surface, self.color, (*self.position, GRID_SIZE, GRID_SIZE))


class Food:

    def __init__(self, snake_pos, wall_pos, food_type="NORMAL"):

        self.type = food_type

        self.active = True if food_type == "NORMAL" else False

        self.timer = pygame.time.get_ticks()

        self.lifetime = 5000

        self.respawn(snake_pos, wall_pos)


    def respawn(self, snake_pos, wall_pos):

        forbidden = set(tuple(p) for p in snake_pos) | wall_pos

       

        if self.type == "POISON":

            self.color = (139, 0, 0) # Dark Red

            self.points = 0

        else:

            rand_val = random.random()

            if rand_val < 0.1: self.color, self.points = COLORS["PURPLE"], 50

            elif rand_val < 0.3: self.color, self.points = COLORS["YELLOW"], 30

            else: self.color, self.points = COLORS["RED"], 10


        while True:

            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,

                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

            if pos not in forbidden:

                self.position = pos

                self.spawn_time = pygame.time.get_ticks()

                break


    def draw(self, surface):

        pygame.draw.rect(surface, self.color, (*self.position, GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(surface, COLORS["WHITE"], (*self.position, GRID_SIZE, GRID_SIZE), 2)


class Walls:

    def __init__(self):

        self.positions = set() # Use a set for instant collision detection


    def generate(self, level):

        if level < 2: return

        # wall generation

        bx, by = random.randint(3, GRID_WIDTH-8)*GRID_SIZE, random.randint(3, GRID_HEIGHT-8)*GRID_SIZE

        for i in range(min(level + 2, 8)):

            self.positions.add((bx, by + i*GRID_SIZE))


    def draw(self, surface):

        for pos in self.positions:

            pygame.draw.rect(surface, COLORS["LIGHT_BLUE"], (*pos, GRID_SIZE, GRID_SIZE))

            pygame.draw.rect(surface, COLORS["WHITE"], (*pos, GRID_SIZE, GRID_SIZE), 1)


def game_loop(name, grid):

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    back_btn = Button("Back to Menu", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 80, 200, 50, COLORS["BLUE"])

    def reset_game():

        s = Snake()

        w = Walls()

        w.generate(1)

        f = Food(s.positions, w.positions, "NORMAL")

        p = Food(s.positions, w.positions, "POISON") # Poison food

        p_up = PowerUp()

        return s, f, p, p_up, w, 0, 1, 0, 0, 0, 10


    snake, food, poison, power_up, walls, score, level, foods_eaten, effect_end,  speed_mod, speed = reset_game()


    game_active = True

    speed_mod = 1

    while True:

        # 1. Event Handling

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:

                if game_active:

                    controls = {pygame.K_UP: UP, pygame.K_w: UP, pygame.K_DOWN: DOWN, pygame.K_s: DOWN,

                                pygame.K_LEFT: LEFT, pygame.K_a: LEFT, pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT}

                    if event.key in controls:

                        snake.change_direction(controls[event.key])

                elif event.key == pygame.K_SPACE:

                    snake, food, poison, power_up, walls, score, level, foods_eaten, effect_end,  speed_mod, speed = reset_game()

                    game_active = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
                if back_btn.is_clicked(event.pos):
                    return

        if game_active:

            screen.fill(COLORS["BLACK"])
            if grid:
                draw_grid(screen)
            snake.draw(screen)


            current_time = pygame.time.get_ticks()

            if current_time - poison.timer > 5000: # Toggle every 5 seconds

                poison.active = not poison.active

                poison.timer = current_time

                if poison.active:

                    poison.respawn(snake.positions, walls.positions)

           

            if not power_up.active_on_field and random.random() < 0.01:

                power_up.spawn(set(tuple(p) for p in snake.positions) | walls.positions)

       

            if power_up.active_on_field and current_time - power_up.spawn_time > power_up.lifetime:

                power_up.active_on_field = False

           

            if current_time > effect_end:

                speed_mod = 0


            snake.move()

           

            head = tuple(snake.positions[0])

            # Collisions

            if head in walls.positions or list(head) in snake.positions[1:]:

                if snake.has_shield:

                    snake.has_shield = False # Block death once

                else:

                    game_active = False

            if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:

                game_active = False


            # Food Logic

            if head == food.position:

                pygame.mixer.Sound("snake/shhh.wav").play()

                snake.grow_flag = True

                score += food.points

                foods_eaten += 1

                if foods_eaten >= 3:

                    level += 1

                    foods_eaten = 0

                    speed += 2

                    walls.generate(level)

                food.respawn(snake.positions, walls.positions)

            # Poison food Logic

            if poison.active and head == poison.position:

                snake.shrink(2)

                if len(snake.positions) <= 1:

                    game_active = False

                else:

                    poison.active = False # Disappear after eating

                    poison.timer = current_time

            if power_up.active_on_field and head == power_up.position:

                power_up.active_on_field = False

                if power_up.type == "SPEED":

                    speed_mod, effect_end = 6, current_time + 5000

                elif power_up.type == "SLOW":

                    speed_mod, effect_end = -4, current_time + 5000

                elif power_up.type == "SHIELD":

                    snake.has_shield = True

           

            # Rendering

            walls.draw(screen)

            food.draw(screen)

            power_up.draw(screen)

            if poison.active:

                poison.draw(screen)


            # UI

            ui_text = f"Score: {score}  Level: {level}  Target: {foods_eaten}/3"

            screen.blit(font_small.render(ui_text, True, COLORS["WHITE"]), (10, 10))

        else:

            # Game Over Screen
            msg = pygame.font.Font(None, 72).render("GAME OVER", True, COLORS["RED"])
            score_final = font_med.render(f"Final Score: {score}", True, COLORS["WHITE"])
            retry = font_med.render("Press SPACE to Restart", True, COLORS["GREEN"])

            screen.blit(msg, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 80))
            screen.blit(score_final, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 10)) # New score line
            screen.blit(retry, (SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2 + 30))
            
            back_btn.draw(screen)

        pygame.display.flip()

        clock.tick(speed + speed_mod) 
if __name__ == "__main__":
    play_btn = Button("Play", 300, 200, 200, 50, COLORS["GREEN"])
    high_btn = Button("Scores", 300, 270, 200, 50, COLORS["BLUE"])
    sett_btn = Button("Settings", 300, 340, 200, 50, COLORS["DARK_GREY"])
    quit_btn = Button("Quit", 300, 410, 200, 50, COLORS["RED"])
    while True:
        screen.fill(COLORS["WHITE"])
        play_btn.draw(screen)
        high_btn.draw(screen)
        quit_btn.draw(screen)
        sett_btn.draw(screen)
        title_text = font_large.render("SNAKE GAME", True, COLORS["BLACK"])
        screen.blit(title_text, (240, 100))
        pygame.display.update()
        settings = load_settings()
        global snake_color
        snake_color = settings["snake_color"]
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if play_btn.is_clicked(event.pos):
                    name = get_username()
                    game_loop(name, settings["grid"])
                if high_btn.is_clicked(event.pos):
                    show_leaderboard()
                if sett_btn.is_clicked(event.pos): 
                    show_settings()
                if quit_btn.is_clicked(event.pos):
                    pygame.quit(); sys.exit()
            if event.type == QUIT:
                pygame.quit(); sys.exit()
