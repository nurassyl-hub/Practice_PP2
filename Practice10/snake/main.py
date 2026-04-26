import pygame
import random
import sys

# --- Constants & Configuration ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE

# Colors (Defined as a dict for cleaner access)
COLORS = {
    "BLACK": (0, 0, 0), "WHITE": (255, 255, 255), "RED": (255, 0, 0),
    "GREEN": (0, 255, 0), "YELLOW": (255, 255, 0), "CYAN": (0, 255, 255),
    "PURPLE": (255, 0, 255), "LIGHT_BLUE": (100, 200, 255), "DARK_GREY": (20, 20, 20)
}

# Directions
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

class Snake:
    def __init__(self):
        mid_x, mid_y = (GRID_WIDTH // 2) * GRID_SIZE, (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [[mid_x, mid_y], [mid_x - GRID_SIZE, mid_y], [mid_x - 2*GRID_SIZE, mid_y]]
        self.direction = RIGHT
        self.grow_flag = False

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

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = (0, 0, 255) if i == 0 else COLORS["GREEN"]
            pygame.draw.rect(surface, color, (*pos, GRID_SIZE, GRID_SIZE))
            border = COLORS["WHITE"] if i == 0 else COLORS["BLACK"]
            pygame.draw.rect(surface, border, (*pos, GRID_SIZE, GRID_SIZE), 1)

class Food:
    def __init__(self, snake_pos, wall_pos):
        self.respawn(snake_pos, wall_pos)

    def respawn(self, snake_pos, wall_pos):
        forbidden = set(tuple(p) for p in snake_pos) | wall_pos
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if pos not in forbidden:
                self.position = pos
                self.spawn_time = pygame.time.get_ticks()
                break

    def draw(self, surface):
        pygame.draw.rect(surface, COLORS["RED"], (*self.position, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, COLORS["WHITE"], (*self.position, GRID_SIZE, GRID_SIZE), 2)

class Walls:
    def __init__(self):
        self.positions = set() # Use a set for instant collision detection

    def generate(self, level):
        if level < 2: return
        
        if level % 2 == 0: # Add L-shapes
            bx, by = random.randint(3, GRID_WIDTH-8)*GRID_SIZE, random.randint(3, GRID_HEIGHT-8)*GRID_SIZE
            for i in range(5):
                self.positions.add((bx, by + i*GRID_SIZE))
                self.positions.add((bx + i*GRID_SIZE, by))
        else: # Add random dots
            for _ in range(3):
                pos = (random.randint(0, GRID_WIDTH-1)*GRID_SIZE, random.randint(0, GRID_HEIGHT-1)*GRID_SIZE)
                self.positions.add(pos)

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, COLORS["LIGHT_BLUE"], (*pos, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, COLORS["WHITE"], (*pos, GRID_SIZE, GRID_SIZE), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 34)
    
    def reset_game():
        s = Snake()
        w = Walls()
        w.generate(1)
        f = Food(s.positions, w.positions)
        return s, f, w, 0, 1, 0, 10 # snake, food, walls, score, level, eaten, speed

    snake, food, walls, score, level, foods_eaten, speed = reset_game()
    game_active = True

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
                    snake, food, walls, score, level, foods_eaten, speed = reset_game()
                    game_active = True

        if game_active:
            # 2. Update logic
            snake.move()
            head = tuple(snake.positions[0])

            # Collisions
            if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT or 
                head in walls.positions or list(head) in snake.positions[1:]):
                game_active = False
            
            # Food Logic
            if list(head) == list(food.position):
                snake.grow_flag = True
                score += 10
                foods_eaten += 1
                if foods_eaten >= 3:
                    level += 1
                    foods_eaten = 0
                    speed += 2
                    walls.generate(level)
                food.respawn(snake.positions, walls.positions)

            # 3. Rendering
            screen.fill(COLORS["BLACK"])
            walls.draw(screen)
            snake.draw(screen)
            food.draw(screen)
            
            # UI
            ui_text = f"Score: {score}  Level: {level}  Target: {foods_eaten}/3"
            screen.blit(font.render(ui_text, True, COLORS["WHITE"]), (10, 10))
        else:
            # Game Over Screen
            msg = pygame.font.Font(None, 72).render("GAME OVER", True, COLORS["RED"])
            retry = font.render("Press SPACE to Restart", True, COLORS["GREEN"])
            screen.blit(msg, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 - 50))
            screen.blit(retry, (SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2 + 20))

        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    main()