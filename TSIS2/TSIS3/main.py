import pygame
from ui import Button, draw_text, draw_title, get_text_input, BIG_FONT, FONT
from ui import BLACK, BLUE, GREEN, RED
from persistence import load_settings, save_settings, load_leaderboard
from racer import RacerGame, WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")
clock = pygame.time.Clock()

def main_menu(settings):
    buttons = {
        "play": Button("Play", (200, 220, 200, 55), GREEN),
        "leaderboard": Button("Leaderboard", (200, 295, 200, 55), BLUE),
        "settings": Button("Settings", (200, 370, 200, 55), BLUE),
        "quit": Button("Quit", (200, 445, 200, 55), RED),
    }
    while True:
        screen.fill((230, 230, 230))
        draw_title(screen, "TSIS3 Racer", WIDTH)
        for button in buttons.values(): button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            for name, btn in buttons.items():
                if btn.is_clicked(event): return name
        
        pygame.display.flip()
        clock.tick(60)

def settings_screen(settings):
    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]
    
    sound_btn = Button("", (180, 190, 240, 50), BLUE)
    color_btn = Button("", (180, 270, 240, 50), BLUE)
    diff_btn = Button("", (180, 350, 240, 50), BLUE)
    back_button = Button("Back", (200, 500, 200, 55), RED)
    
    while True:
        screen.fill((235, 235, 235))
        draw_title(screen, "Settings", WIDTH)
        
        sound_btn.text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_btn.text = f"Car color: {settings['car_color']}"
        diff_btn.text = f"Difficulty: {settings['difficulty']}"
        
        for b in [sound_btn, color_btn, diff_btn, back_button]: b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if sound_btn.is_clicked(event):
                settings["sound"] = not settings["sound"]
            elif color_btn.is_clicked(event):
                idx = (colors.index(settings["car_color"]) + 1) % len(colors)
                settings["car_color"] = colors[idx]
            elif diff_btn.is_clicked(event):
                idx = (difficulties.index(settings["difficulty"]) + 1) % len(difficulties)
                settings["difficulty"] = difficulties[idx]
            elif back_button.is_clicked(event):
                save_settings(settings)
                return "menu"
                
        pygame.display.flip()
        clock.tick(60)

def leaderboard_screen():
    back_button = Button("Back", (200, 690, 200, 50), RED)
    scores = load_leaderboard() # Load once for performance

    while True:
        screen.fill((240, 240, 240))
        draw_title(screen, "Leaderboard Top 10", WIDTH)
        y = 160
        
        draw_text(screen, "Rank", 55, 125)
        draw_text(screen, "Name", 130, 125)
        draw_text(screen, "Score", 285, 125)

        for i, item in enumerate(scores[:10], start=1):
            draw_text(screen, i, 65, y)
            draw_text(screen, item["name"], 130, y)
            draw_text(screen, item["score"], 285, y)
            y += 45

        back_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if back_button.is_clicked(event): return "menu"

        pygame.display.flip()
        clock.tick(60)

def game_over_screen(status, score, distance, coins):
    retry_button = Button("Retry", (200, 420, 200, 55), GREEN)
    menu_button = Button("Main Menu", (200, 500, 200, 55), BLUE)

    while True:
        screen.fill((235, 235, 235))

        title = "Finished!" if status == "finished" else "Game Over"

        draw_text(screen, title, WIDTH // 2, 150, BLACK, BIG_FONT, center=True)
        draw_text(screen, f"Score: {score}", WIDTH // 2, 240, BLACK, FONT, center=True)
        draw_text(screen, f"Distance: {distance}m", WIDTH // 2, 285, BLACK, FONT, center=True)
        draw_text(screen, f"Coins: {coins}", WIDTH // 2, 330, BLACK, FONT, center=True)

        retry_button.draw(screen)
        menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_button.is_clicked(event):
                return "retry"

            if menu_button.is_clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)

def main():
    settings = load_settings()
    while True:
        action = main_menu(settings)
        if action == "quit": break
        elif action == "play": 
            if run_game(settings) == "quit": break
        elif action == "settings": 
            if settings_screen(settings) == "quit": break
        elif action == "leaderboard":
            if leaderboard_screen() == "quit": break
    pygame.quit()

def run_game(settings):
    name = get_text_input(screen, clock, WIDTH, HEIGHT)
    if not name: return "menu"
    
    while True: # Цикл для возможности перезапуска (Retry)
        game = RacerGame(screen, clock, settings, name)
        status, score, dist, coins = game.run()
        
        if status == "quit": 
            return "quit"
        
        # Показываем экран Game Over после завершения заезда
        choice = game_over_screen(status, score, dist, coins)
        
        if choice == "retry":
            continue # Запускает цикл while True заново (новая игра)
        elif choice == "menu":
            return "menu" # Выходит в главное меню
        elif choice == "quit":
            return "quit"

if __name__ == "__main__":
    main()