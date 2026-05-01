import pygame
import sys
import math
import datetime

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TOOLBAR_HEIGHT = 100 # Increased height to fit new buttons

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# Modes
MODE_BRUSH = "brush"
MODE_RECT = "rectangle"
MODE_CIRCLE = "circle"
MODE_ERASER = "eraser"
MODE_SQUARE = "square"
MODE_TRI_RIGHT = "right_tri"
MODE_TRI_EQU = "equ_tri"
MODE_RHOMBUS = "rhombus"
MODE_LINE = "line"
MODE_FILL = "fill"
MODE_TEXT = "text"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Paint Program")
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, width, height, color, text="", text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 20) # Smaller font for more buttons

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class ColorPalette:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, GRAY]
        self.color_rects = []
        self.selected_color = BLACK
        for i, color in enumerate(self.colors):
            rect = pygame.Rect(x + i * 35, y, 30, 30)
            self.color_rects.append((rect, color))

    def draw(self, surface):
        for rect, color in self.color_rects:
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            if color == self.selected_color:
                pygame.draw.rect(surface, WHITE, rect, 3)

    def check_click(self, pos):
        for rect, color in self.color_rects:
            if rect.collidepoint(pos):
                self.selected_color = color
                return True
        return False

def draw_smooth_line(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    if distance == 0:
        pygame.draw.circle(surface, color, start, radius)
        return
    for i in range(distance):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), radius)

def flood_fill(surface, x, y, fill_color):
    # Get the color of the pixel we clicked on
    target_color = surface.get_at((x, y))
    
    # If the colors are already the same, do nothing to avoid infinite loop
    if target_color == fill_color:
        return

    # Use a stack for the iterative approach
    stack = [(x, y)]
    width, height = surface.get_size()

    while stack:
        curr_x, curr_y = stack.pop()

        # Check bounds and if the current pixel matches our target color
        if 0 <= curr_x < width and 0 <= curr_y < height:
            if surface.get_at((curr_x, curr_y)) == target_color:
                # Change the color
                surface.set_at((curr_x, curr_y), fill_color)
                
                # Add neighbors to the stack (Up, Down, Left, Right)
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))

def main():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)
    
    drawing = False
    start_pos = None
    last_pos = None 
    current_mode = MODE_BRUSH
    brush_size = 5
    current_color = BLACK
    
    typing = False
    text_input = ""
    text_pos = (0, 0)
    font_size = 30 # You can link this to brush_size later
    active_font = pygame.font.SysFont("Arial", font_size)
    
    # UI Setup
    buttons = [
        Button(10, 10, 70, 30, GRAY, "Brush"),
        Button(85, 10, 70, 30, GRAY, "Rect"),
        Button(160, 10, 70, 30, GRAY, "Circle"),
        Button(235, 10, 70, 30, GRAY, "Square"),
        Button(310, 10, 70, 30, GRAY, "R-Tri"),
        Button(385, 10, 70, 30, GRAY, "E-Tri"),
        Button(460, 10, 70, 30, GRAY, "Rhomb"),
        Button(535, 10, 70, 30, GRAY, "Eraser"),
        Button(610, 10, 70, 30, GRAY, "Line"), 
        Button(685, 10, 30, 30, GRAY, "F"),
        Button(720, 10, 30, 30, GRAY, "T"),
        Button(755, 10, 30, 30, WHITE, "Clr")
    ]
    
    color_palette = ColorPalette(10, 50)
    size_up_btn = Button(600, 50, 30, 30, GRAY, "+")
    size_down_btn = Button(640, 50, 30, 30, GRAY, "-")
    size_text_font = pygame.font.Font(None, 24)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    # Check Mode Buttons
                    if buttons[0].is_clicked(event.pos): current_mode = MODE_BRUSH
                    elif buttons[1].is_clicked(event.pos): current_mode = MODE_RECT
                    elif buttons[2].is_clicked(event.pos): current_mode = MODE_CIRCLE
                    elif buttons[3].is_clicked(event.pos): current_mode = MODE_SQUARE
                    elif buttons[4].is_clicked(event.pos): current_mode = MODE_TRI_RIGHT
                    elif buttons[5].is_clicked(event.pos): current_mode = MODE_TRI_EQU
                    elif buttons[6].is_clicked(event.pos): current_mode = MODE_RHOMBUS
                    elif buttons[7].is_clicked(event.pos): current_mode = MODE_ERASER
                    elif buttons[8].is_clicked(event.pos): current_mode = MODE_LINE
                    elif buttons[9].is_clicked(event.pos): current_mode = MODE_FILL
                    elif buttons[10].is_clicked(event.pos): current_mode = MODE_TEXT
                    elif buttons[11].is_clicked(event.pos): canvas.fill(WHITE)
    
                    if size_up_btn.is_clicked(event.pos):
                        brush_size = min(50, brush_size + 2)
                    elif size_down_btn.is_clicked(event.pos):
                        brush_size = max(1, brush_size - 2)
                    
                    color_palette.check_click(event.pos)
                    current_color = color_palette.selected_color
                else:
                    start_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                    if current_mode == MODE_FILL:
                    # Trigger the flood fill
                        flood_fill(canvas, start_pos[0], start_pos[1], current_color)
                    elif current_mode == MODE_TEXT:
                        typing = True
                        text_pos = start_pos
                        text_input = ""
                    else:
                        drawing = True
                        last_pos = start_pos
                        if current_mode in [MODE_BRUSH, MODE_ERASER]:
                            color = WHITE if current_mode == MODE_ERASER else current_color
                            pygame.draw.circle(canvas, color, start_pos, brush_size)

            
            elif event.type == pygame.MOUSEMOTION:
                if drawing and current_mode in [MODE_BRUSH, MODE_ERASER]:
                    if event.pos[1] > TOOLBAR_HEIGHT:
                        curr = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                        color = WHITE if current_mode == MODE_ERASER else current_color
                        draw_smooth_line(canvas, color, last_pos, curr, brush_size)
                        last_pos = curr

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and event.pos[1] > TOOLBAR_HEIGHT:
                    end_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                    
                    # --- SHAPE DRAWING LOGIC ---
                    
                    if current_mode == MODE_RECT:
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, current_color, rect, brush_size)
                        
                    elif current_mode == MODE_SQUARE:
                        # Find the side length based on the larger of the X or Y drag distance
                        side = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                        # Determine direction of drag
                        s_x = start_pos[0] if end_pos[0] > start_pos[0] else start_pos[0] - side
                        s_y = start_pos[1] if end_pos[1] > start_pos[1] else start_pos[1] - side
                        pygame.draw.rect(canvas, current_color, (s_x, s_y, side, side), brush_size)

                    elif current_mode == MODE_TRI_RIGHT:
                        # Three points: start, drag-end, and the corner meeting them
                        points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                        pygame.draw.polygon(canvas, current_color, points, brush_size)

                    elif current_mode == MODE_TRI_EQU:
                        # Calculate distance as base
                        dist = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        # Height of equilateral triangle is (sqrt(3)/2) * side
                        height = int(dist * math.sqrt(3) / 2)
                        # Points: Tip, bottom-left, bottom-right
                        points = [
                            start_pos,
                            (start_pos[0] - dist // 2, start_pos[1] + height),
                            (start_pos[0] + dist // 2, start_pos[1] + height)
                        ]
                        pygame.draw.polygon(canvas, current_color, points, brush_size)

                    elif current_mode == MODE_RHOMBUS:
                        # Defined by four mid-points of the bounding box created by the drag
                        mid_top = (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1])
                        mid_bottom = (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, end_pos[1])
                        mid_left = (start_pos[0], start_pos[1] + (end_pos[1] - start_pos[1]) // 2)
                        mid_right = (end_pos[0], start_pos[1] + (end_pos[1] - start_pos[1]) // 2)
                        pygame.draw.polygon(canvas, current_color, [mid_top, mid_right, mid_bottom, mid_left], brush_size)

                    elif current_mode == MODE_CIRCLE:
                        rad = int(math.hypot(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.circle(canvas, current_color, start_pos, rad, brush_size)

                    elif current_mode == MODE_LINE:
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)
                    
                drawing = False
                start_pos = None
            elif event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        # Confirm: Render text onto the permanent canvas
                        text_surface = active_font.render(text_input, True, current_color)
                        canvas.blit(text_surface, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel: Wipe the buffer
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        # Add typed character to buffer
                        text_input += event.unicode
                # Check for Ctrl + S
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"paint_{timestamp}.png"
                        pygame.image.save(canvas, filename)
                        print(f"Canvas saved successfully as {filename}")
        # Rendering
        screen.fill(GRAY)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))
        if typing:
            # Draw a small cursor line or just the text
            preview_surface = active_font.render(text_input + "|", True, current_color)
            # Adjust position to account for the toolbar offset
            screen.blit(preview_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))
        if drawing and start_pos:
            curr_x, curr_y = mouse_pos[0], mouse_pos[1] 
            if curr_y > TOOLBAR_HEIGHT:
                if current_mode == MODE_LINE:
                    # Draw directly to the SCREEN, not the canvas
                    # This makes it disappear as soon as the screen refreshes
                    pygame.draw.line(screen, current_color, 
                                        (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT), 
                                        (curr_x, curr_y), brush_size)
                if typing:
                    # Draw a small cursor line or just the text
                    preview_surface = active_font.render(text_input + "|", True, current_color)
                    # Adjust position to account for the toolbar offset
                    screen.blit(preview_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))
        # Toolbar UI
        pygame.draw.rect(screen, (220, 220, 220), (0, 0, SCREEN_WIDTH, TOOLBAR_HEIGHT))
        for b in buttons: b.draw(screen)
        color_palette.draw(screen)
        size_up_btn.draw(screen)
        size_down_btn.draw(screen)
        
        mode_label = size_text_font.render(f"Mode: {current_mode}", True, BLACK)
        screen.blit(mode_label, (400, 60))
        size_label = size_text_font.render(f"Size: {brush_size}", True, BLACK)
        screen.blit(size_label, (680, 60))
        
        pygame.display.flip()
        clock.tick(60)
    sys.exit
    pygame.quit()

if __name__ == "__main__":
    main()




