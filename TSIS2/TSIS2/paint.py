import pygame
from datetime import datetime
from tools import flood_fill, draw_shape

pygame.init()

# Screen settings
WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 100
CANVAS_Y = TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
text_font = pygame.font.SysFont("Arial", 32)

# Main drawing canvas
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (210, 210, 210)
DARK_GRAY = (100, 100, 100)
RED = (220, 0, 0)
GREEN = (0, 170, 0)
BLUE = (0, 80, 220)
YELLOW = (240, 210, 0)
PURPLE = (150, 0, 180)
ORANGE = (255, 130, 0)

current_color = BLACK
background_color = WHITE

# Tool state
tool = "pencil"
brush_size = 5

drawing = False
start_pos = None
last_pos = None
current_mouse_pos = None

# Text tool state
text_active = False
text_pos = None
text_value = ""

# Toolbar buttons
tool_buttons = [
    ("Pencil(P)", "pencil", pygame.Rect(10, 10, 90, 30)),
    ("Line(L)", "line", pygame.Rect(110, 10, 80, 30)),
    ("Rect(R)", "rectangle", pygame.Rect(200, 10, 80, 30)),
    ("Circle(C)", "circle", pygame.Rect(290, 10, 90, 30)),
    ("Square(S)", "square", pygame.Rect(390, 10, 90, 30)),
    ("RightTri(A)", "right_triangle", pygame.Rect(490, 10, 110, 30)),
    ("EqTri(Q)", "equilateral_triangle", pygame.Rect(610, 10, 90, 30)),
    ("Rhombus(H)", "rhombus", pygame.Rect(710, 10, 110, 30)),
    ("Fill(F)", "fill", pygame.Rect(830, 10, 70, 30)),
    ("Text(T)", "text", pygame.Rect(910, 10, 70, 30)),
    ("Eraser(E)", "eraser", pygame.Rect(10, 50, 90, 30)),
]

color_buttons = [
    (BLACK, pygame.Rect(130, 50, 30, 30)),
    (RED, pygame.Rect(170, 50, 30, 30)),
    (GREEN, pygame.Rect(210, 50, 30, 30)),
    (BLUE, pygame.Rect(250, 50, 30, 30)),
    (YELLOW, pygame.Rect(290, 50, 30, 30)),
    (PURPLE, pygame.Rect(330, 50, 30, 30)),
    (ORANGE, pygame.Rect(370, 50, 30, 30)),
    (WHITE, pygame.Rect(410, 50, 30, 30)),
]

size_buttons = [
    ("1 small", 2, pygame.Rect(470, 50, 80, 30)),
    ("2 medium", 5, pygame.Rect(560, 50, 95, 30)),
    ("3 large", 10, pygame.Rect(665, 50, 80, 30)),
]


def screen_to_canvas(pos):
    """Convert screen position to canvas position."""
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def is_on_canvas(pos):
    """Checks if mouse is inside canvas area."""
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def save_canvas():
    """Save canvas as PNG with timestamp."""
    filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


def draw_toolbar():
    """Draw top toolbar with tools, colors, sizes, and status."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Draw tool buttons
    for label, value, rect in tool_buttons:
        if tool == value:
            color = (170, 220, 255)
        else:
            color = (235, 235, 235)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)

        text = font.render(label, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 6))

    # Draw color buttons
    for color_value, rect in color_buttons:
        pygame.draw.rect(screen, color_value, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)

        if current_color == color_value:
            pygame.draw.rect(screen, BLACK, rect, 4)

    # Draw size buttons
    for label, value, rect in size_buttons:
        if brush_size == value:
            color = (170, 220, 255)
        else:
            color = (235, 235, 235)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)

        text = font.render(label, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 6))

    # Info text
    info = f"Tool: {tool} | Brush: {brush_size}px | Ctrl+S: Save"
    info_text = font.render(info, True, BLACK)
    screen.blit(info_text, (760, 55))


def handle_toolbar_click(pos):
    """Handle clicks on toolbar buttons."""
    global tool, current_color, brush_size

    for label, value, rect in tool_buttons:
        if rect.collidepoint(pos):
            tool = value
            return True

    for color_value, rect in color_buttons:
        if rect.collidepoint(pos):
            current_color = color_value
            return True

    for label, value, rect in size_buttons:
        if rect.collidepoint(pos):
            brush_size = value
            return True

    return False


def draw_text_preview():
    """Draw active text preview while typing."""
    if text_active and text_pos is not None:
        preview_text = text_value + "|"
        rendered = text_font.render(preview_text, True, current_color)
        screen.blit(rendered, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))


def draw_live_preview():
    """Draw temporary preview for line and shape tools."""
    if drawing and start_pos and current_mouse_pos:
        preview_tools = [
            "line",
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ]

        if tool in preview_tools:
            preview_surface = canvas.copy()
            draw_shape(
                preview_surface,
                tool,
                current_color,
                start_pos,
                current_mouse_pos,
                brush_size
            )
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))


def confirm_text():
    """Render typed text permanently onto canvas."""
    global text_active, text_value, text_pos

    if text_active and text_pos is not None and text_value:
        rendered = text_font.render(text_value, True, current_color)
        canvas.blit(rendered, text_pos)

    text_active = False
    text_value = ""
    text_pos = None


def cancel_text():
    """Cancel current text typing."""
    global text_active, text_value, text_pos

    text_active = False
    text_value = ""
    text_pos = None


running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            # Ctrl + S saves canvas
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_s:
                    save_canvas()

            # Text typing mode
            elif text_active:
                if event.key == pygame.K_RETURN:
                    confirm_text()
                elif event.key == pygame.K_ESCAPE:
                    cancel_text()
                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]
                else:
                    text_value += event.unicode

            # Normal shortcuts
            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_a:
                    tool = "right_triangle"
                elif event.key == pygame.K_q:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if mouse_pos[1] < TOOLBAR_HEIGHT:
                handle_toolbar_click(mouse_pos)

            elif is_on_canvas(mouse_pos):
                canvas_pos = screen_to_canvas(mouse_pos)

                if tool == "fill":
                    flood_fill(canvas, canvas_pos, current_color)

                elif tool == "text":
                    text_active = True
                    text_pos = canvas_pos
                    text_value = ""

                elif tool == "pencil":
                    drawing = True
                    last_pos = canvas_pos

                elif tool == "eraser":
                    drawing = True
                    last_pos = canvas_pos

                else:
                    drawing = True
                    start_pos = canvas_pos
                    current_mouse_pos = canvas_pos

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

            if drawing and is_on_canvas(mouse_pos):
                canvas_pos = screen_to_canvas(mouse_pos)
                current_mouse_pos = canvas_pos

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, background_color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos

            if drawing and is_on_canvas(mouse_pos):
                end_pos = screen_to_canvas(mouse_pos)

                if tool not in ["pencil", "eraser"]:
                    draw_shape(
                        canvas,
                        tool,
                        current_color,
                        start_pos,
                        end_pos,
                        brush_size
                    )

            drawing = False
            start_pos = None
            last_pos = None
            current_mouse_pos = None

    # Draw preview after event processing
    if drawing:
        draw_live_preview()

    draw_text_preview()
    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
