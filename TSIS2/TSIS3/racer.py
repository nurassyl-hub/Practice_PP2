import os
import random
import pygame

from persistence import add_score
from ui import draw_text, WHITE, BLACK, YELLOW

# --- Constants ---
WIDTH = 600
HEIGHT = 800
ROAD_LEFT = 90
ROAD_RIGHT = 510
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
FINISH_DISTANCE = 3000
ASSET_DIR = "assets"

CAR_COLORS = {
    "blue": (40, 110, 230),
    "red": (220, 50, 50),
    "green": (40, 180, 80),
    "yellow": (230, 210, 40)
}

DIFFICULTY_CONFIG = {
    "easy": {"enemy_speed": 4, "spawn_delay": 75, "obstacle_delay": 130},
    "normal": {"enemy_speed": 5, "spawn_delay": 55, "obstacle_delay": 100},
    "hard": {"enemy_speed": 7, "spawn_delay": 38, "obstacle_delay": 75}
}

def load_image(name, size=None):
    path = os.path.join(ASSET_DIR, name)
    try:
        image = pygame.image.load(path).convert_alpha()
        if size is not None:
            image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError):
        return None

def load_sound(name):
    path = os.path.join(ASSET_DIR, name)
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        return None

class Player:
    def __init__(self, color_name):
        self.w, self.h = 48, 80
        self.color_name = color_name
        self.file_map = {
            "green": "Player_gre.png",
            "yellow": "Player_yel.png",
            "red": "Player_red.png",
            "blue": "Player.png"
        }
        self.image = self.load_player_asset()
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 130
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def load_player_asset(self):
        filename = self.file_map.get(self.color_name, "Player.png")
        image = load_image(filename, (self.w, self.h))
        return image if image else load_image("Player.png", (self.w, self.h))

    def update(self, keys, nitro_active=False):
        move_speed = self.speed + 4 if nitro_active else self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.x += move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: self.y -= move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: self.y += move_speed
        self.x = max(ROAD_LEFT + 5, min(self.x, ROAD_RIGHT - self.w - 5))
        self.y = max(100, min(self.y, HEIGHT - self.h - 20))
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, CAR_COLORS.get(self.color_name, WHITE), self.rect, border_radius=10)

class EnemyCar:
    def __init__(self, lane, speed):
        self.w, self.h = 48, 80
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.w // 2
        self.y = -self.h
        self.speed = speed
        self.image = load_image("Enemy.png", (self.w, self.h))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = random.choice([(160, 30, 30), (30, 30, 160), (40, 150, 80)])

    def update(self, scroll_speed):
        self.y += self.speed + scroll_speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.image: screen.blit(self.image, self.rect)
        else: pygame.draw.rect(screen, self.color, self.rect, border_radius=8)

class Coin:
    def __init__(self, lane):
        self.value = random.choice([1, 1, 2, 5])
        self.size = 35
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -30
        self.image = load_image("coin.png", (self.size, self.size))
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def update(self, scroll_speed):
        self.y += 5 + scroll_speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        if self.image: screen.blit(self.image, self.rect)
        else: pygame.draw.circle(screen, YELLOW, (self.x, int(self.y)), 15)
        draw_text(screen, str(self.value), self.rect.centerx - 6, self.rect.centery - 12, BLACK)

class Obstacle:
    def __init__(self, lane, kind):
        self.kind = kind
        self.w, self.h = LANE_WIDTH - 24, 38
        self.x = ROAD_LEFT + lane * LANE_WIDTH + 12
        self.y = -45
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.label, self.color, self.image = "O", (90, 60, 40), None
        if self.kind == "barrier":
            self.color, self.label = (220, 80, 30), "B"
            self.image = load_image("barrier.png", (self.w, self.h))
        elif self.kind == "oil":
            self.color, self.label = (20, 20, 20), "OIL"
            self.image = load_image("oil.png", (self.w, self.h))

    def update(self, scroll_speed):
        self.y += 4 + scroll_speed
        self.rect.y = int(self.y)

    def draw(self, screen):
        if self.image: screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
            draw_text(screen, self.label, self.rect.centerx - 10, self.rect.centery - 12, WHITE)

class PowerUp:
    def __init__(self, lane):
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -30
        self.radius = 20
        
        # Mapping your specific filenames and extensions
        file_map = {
            "nitro": "nitro.png",      # Your uploaded JPG
            "shield": "shield.png",   # Your uploaded WebP
            "repair": "gaika.png"     # Your uploaded wrench image
        }
        
        filename = file_map.get(self.kind)
        # Load and scale to fit the road
        self.image = load_image(filename, (80, 80))
        
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 50, 50)

    def update(self, scroll_speed):
        self.y += 5 + scroll_speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            # Fallback circle if image fails to load
            pygame.draw.circle(screen, WHITE, (self.x, int(self.y)), self.radius)

class RacerGame:
    def __init__(self, screen, clock, settings, player_name):
        self.screen, self.clock, self.settings, self.player_name = screen, clock, settings, player_name
        self.config = DIFFICULTY_CONFIG[settings.get("difficulty", "normal")]
        self.player = Player(settings.get("car_color", "blue"))
        self.road_image = load_image("AnimatedStreet.png", (ROAD_WIDTH, HEIGHT))
        self.sound_enabled = settings.get("sound", True)
        self.crash_sound = load_sound("crash.wav") if self.sound_enabled else None
        if self.sound_enabled:
            path = os.path.join(ASSET_DIR, "background.wav")
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1)

        self.enemies, self.coins, self.obstacles, self.powerups = [], [], [], []
        self.frame = self.road_offset = self.distance = self.coins_count = self.score = 0
        self.active_power, self.power_timer, self.shield = None, 0, False
        self.game_over = self.finished = False
        # В конце метода run в классе RacerGame

    def spawn_objects(self):
        scaling = self.distance // 500
        if self.frame % max(20, self.config["spawn_delay"] - scaling) == 0:
            self.enemies.append(EnemyCar(random.randint(0, LANE_COUNT-1), self.config["enemy_speed"] + scaling))
        if self.frame % 80 == 0: self.coins.append(Coin(random.randint(0, LANE_COUNT-1)))
        if self.frame % self.config["obstacle_delay"] == 0:
            self.obstacles.append(Obstacle(random.randint(0, LANE_COUNT-1), random.choice(["barrier", "oil", "pothole"])))
        if self.frame % 400 == 0: self.powerups.append(PowerUp(random.randint(0, LANE_COUNT-1)))

    def handle_collision(self, hit_type):
        if self.shield and hit_type in ["enemy", "barrier"]:
            self.shield = False
            self.active_power = None
            return
        if hit_type in ["enemy", "barrier"]:
            if self.crash_sound: self.crash_sound.play()
            self.game_over = True
        elif hit_type == "oil": self.player.speed = max(4, self.player.speed - 1)

    def update(self):
        self.frame += 1
        nitro = (self.active_power == "nitro")
        scroll = 5 + (3 if nitro else 0)
        self.player.update(pygame.key.get_pressed(), nitro)
        self.road_offset = (self.road_offset + scroll) % HEIGHT
        self.distance += scroll // 2
        self.score = (self.coins_count * 20) + self.distance
        if self.power_timer > 0: self.power_timer -= 1
        else: self.active_power = None
        self.spawn_objects()
        for lst in [self.enemies, self.coins, self.obstacles, self.powerups]:
            for obj in lst: obj.update(scroll)
        for e in self.enemies[:]:
            if self.player.rect.colliderect(e.rect): self.handle_collision("enemy")
        for c in self.coins[:]:
            if self.player.rect.colliderect(c.rect): 
                self.coins_count += c.value
                self.coins.remove(c)
        for o in self.obstacles[:]:
            if self.player.rect.colliderect(o.rect): 
                self.handle_collision(o.kind)
                self.obstacles.remove(o)
        for p in self.powerups[:]:
            if self.player.rect.colliderect(p.rect):
                self.active_power, self.power_timer = p.kind, 240
                if p.kind == "shield": self.shield = True
                self.powerups.remove(p)
        if self.distance >= FINISH_DISTANCE: self.finished = self.game_over = True

    def draw(self):
        # 1. Отрисовка фона и дороги
        self.screen.fill((60, 150, 70))
        if self.road_image:
            self.screen.blit(self.road_image, (ROAD_LEFT, self.road_offset))
            self.screen.blit(self.road_image, (ROAD_LEFT, self.road_offset - HEIGHT))
        
        # 2. Отрисовка игровых объектов
        for lst in [self.coins, self.powerups, self.obstacles, self.enemies]:
            for obj in lst: 
                obj.draw(self.screen)
        
        self.player.draw(self.screen)

        # 3. ВЕРХНЯЯ ПАНЕЛЬ (Интерфейс)
        # Рисуем белую подложку высотой 100 пикселей
        pygame.draw.rect(self.screen, (245, 245, 245), (0, 0, WIDTH, 100))
        
        # Настройки координат для колонок
        col1 = 20
        col2 = WIDTH // 3 + 20
        col3 = (WIDTH // 3) * 2 + 20
        row1 = 15
        row2 = 55

        # Колонна 1: Имя и Счет
        draw_text(self.screen, f"Name: {self.player_name}", col1, row1, BLACK)
        draw_text(self.screen, f"Score: {self.score}", col1, row2, BLACK)

        # Колонна 2: Монеты и Дистанция
        draw_text(self.screen, f"Coins: {self.coins_count}", col2, row1, BLACK)
        draw_text(self.screen, f"Distance: {self.distance}m", col2, row2, BLACK)

        # Колонна 3: Остаток пути и Power-up
        remaining = max(0, FINISH_DISTANCE - self.distance)
        draw_text(self.screen, f"Remaining: {remaining}m", col3, row1, BLACK)
        
        # Отображаем текущую силу (если нет — пишем "None")
        power_str = str(self.active_power).capitalize() if self.active_power else "None"
        draw_text(self.screen, f"Power: {power_str}", col3, row2, (200, 0, 0) if self.active_power else BLACK)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.mixer.music.stop()
                    return "quit", self.score, self.distance, self.coins_count
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.mixer.music.stop()
        add_score(self.player_name, self.score, self.distance, self.coins_count)
        return ("finished" if self.finished else "game_over"), self.score, self.distance, self.coins_count