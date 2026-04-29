import pygame
from collections import deque


def flood_fill(surface, start_pos, new_color):
    """
    Flood fill tool.
    It fills connected pixels with the same color as the clicked pixel.
    Uses pygame.Surface.get_at() and pygame.Surface.set_at().
    """
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    new_color = pygame.Color(new_color)

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def draw_square(surface, color, start_pos, end_pos, width):
    """
    Draws a square using start and end mouse positions.
    The side size is chosen from the smaller distance.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= side
    if y2 < y1:
        y1 -= side

    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, width)


def draw_right_triangle(surface, color, start_pos, end_pos, width):
    """
    Draws a right triangle inside the rectangle area.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, width):
    """
    Draws a simple equilateral-like triangle using mouse drag area.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos

    top = ((x1 + x2) // 2, y1)
    left = (x1, y2)
    right = (x2, y2)

    pygame.draw.polygon(surface, color, [top, left, right], width)


def draw_rhombus(surface, color, start_pos, end_pos, width):
    """
    Draws a rhombus using the bounding box.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    points = [
        (mid_x, y1),
        (x2, mid_y),
        (mid_x, y2),
        (x1, mid_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_shape(surface, tool, color, start_pos, end_pos, brush_size):
    """
    One helper function for all shape tools.
    Brush size is used as stroke thickness.
    """
    x1, y1 = start_pos
    x2, y2 = end_pos

    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    if tool == "line":
        pygame.draw.line(surface, color, start_pos, end_pos, brush_size)

    elif tool == "rectangle":
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "circle":
        pygame.draw.ellipse(surface, color, rect, brush_size)

    elif tool == "square":
        draw_square(surface, color, start_pos, end_pos, brush_size)

    elif tool == "right_triangle":
        draw_right_triangle(surface, color, start_pos, end_pos, brush_size)

    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, color, start_pos, end_pos, brush_size)

    elif tool == "rhombus":
        draw_rhombus(surface, color, start_pos, end_pos, brush_size)
