import pygame 

pygame.init()
WIDTH, HEIGHT = 500, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()
running = True
x, y = 100, 100
radius = 20
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 20
    if pressed[pygame.K_DOWN]: y += 20
    if pressed[pygame.K_LEFT]: x -= 20
    if pressed[pygame.K_RIGHT]: x += 20
    screen.fill((0, 0, 0))
    x = max(radius, min(x, WIDTH-radius))
    y = max(radius, min(y, HEIGHT-radius))

    pygame.draw.circle(screen, (0, 0, 255), (x, y), radius)
    pygame.display.flip()
    clock.tick(60)


