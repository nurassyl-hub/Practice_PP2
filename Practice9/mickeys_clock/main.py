import pygame
import datetime

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
center = (WIDTH // 2, HEIGHT // 2)
clock = pygame.time.Clock()

mickey = pygame.image.load("body.png")
hand_min = pygame.image.load("minute.png")
hand_sec = pygame.image.load("second.png")

def blit_rotate_center(surf, image, center, angle):
    # Rotate the image (negative angle for clockwise)
    rotated_image = pygame.transform.rotate(image, -angle)
    # Get the rect and keep the center locked
    new_rect = rotated_image.get_rect(center=center)
    surf.blit(rotated_image, new_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    
    angle_min = (now.minute * 6) + (now.second * 0.1)
    angle_sec = now.second * 6

    screen.fill((255, 255, 255))
    
    mickey_rect = mickey.get_rect(center=center)
    screen.blit(mickey, mickey_rect)
    
    blit_rotate_center(screen, hand_min, center, angle_min)

    blit_rotate_center(screen, hand_sec, center, angle_sec)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()