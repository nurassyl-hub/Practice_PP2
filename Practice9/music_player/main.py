import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 26, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

MUSIC_DIR = "music/"
playlist = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]
current_idx = 0
is_playing = False
song_length = 0 

def play_song():
    global is_playing, song_length
    if playlist:
        path = os.path.join(MUSIC_DIR, playlist[current_idx])

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        
        temp_sound = pygame.mixer.Sound(path)
        song_length = temp_sound.get_length()
        
        is_playing = True

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((25, 25, 35)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not is_playing: play_song()
                else: pygame.mixer.music.unpause()
            elif event.key == pygame.K_s:
                pygame.mixer.music.pause()
            elif event.key == pygame.K_n:
                current_idx = (current_idx + 1) % len(playlist)
                play_song()
            elif event.key == pygame.K_b:
                current_idx = (current_idx - 1) % len(playlist)
                play_song()

    if playlist:
        song_title = f"Playing: {playlist[current_idx]}"
        screen.blit(font.render(song_title, True, (255, 255, 255)), (50, 80))

        bar_x, bar_y, bar_max_width, bar_height = 50, 200, 500, 15

        pygame.draw.rect(screen, (60, 60, 80), (bar_x, bar_y, bar_max_width, bar_height))

        if is_playing:
            current_ms = pygame.mixer.music.get_pos()
            
            if current_ms != -1 and song_length > 0:
                current_sec = current_ms / 1000
                
                progress_pixel_width = (current_sec / song_length) * bar_max_width
                
                if progress_pixel_width > bar_max_width:

                    progress_pixel_width = bar_max_width
                pygame.draw.rect(screen, (0, 200, 255), (bar_x, bar_y, progress_pixel_width, bar_height))

                time_txt = small_font.render(f"{int(current_sec)}s ", True, (180, 180, 180))
                screen.blit(time_txt, (bar_x, bar_y + 25))

    hint = small_font.render("[P] Play  [S] Pause  [N] Next  [B] Back", True, (100, 100, 120))
    screen.blit(hint, (50, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()