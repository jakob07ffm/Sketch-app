import pygame
import sys

pygame.init()

win_width, win_height = 800, 600

LIGHT_GRAY = (245, 245, 245)
DARK_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
ACCENT_COLOR = (52, 152, 219)
SOFT_BLACK = (33, 33, 33)
TRANSPARENT = (0, 0, 0, 0)

highlight_surface = pygame.Surface((win_width, win_height), pygame.SRCALPHA)

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Modern Sketch App")

win.fill(WHITE)

text_mode = False
eraser_mode = False
draw_mode = True
highlight_mode = False
start_pos = None
prev_mouse_pos = None
t_mouse_pos = 0, 60
text_dragging = False

key_log = []

button_width, button_height = 100, 40
button_radius = 10

eraser_size = 20  # Size of the eraser

# Button positions at the bottom
text_mode_button = pygame.Rect(50, win_height - 60, button_width, button_height)
eraser_mode_button = pygame.Rect(160, win_height - 60, button_width, button_height)
clear_screen_button = pygame.Rect(270, win_height - 60, button_width, button_height)
draw_mode_button = pygame.Rect(380, win_height - 60, button_width, button_height)
highlight_mode_button = pygame.Rect(490, win_height - 60, button_width, button_height)

def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_mode_button.collidepoint(mouse_pos):
                text_mode = True
                eraser_mode = False
                draw_mode = False
                highlight_mode = False
            elif eraser_mode_button.collidepoint(mouse_pos):
                eraser_mode = True
                text_mode = False
                draw_mode = False
                highlight_mode = False
            elif clear_screen_button.collidepoint(mouse_pos):
                win.fill(WHITE)
                key_log.clear()
                text_mode = False
                eraser_mode = False
                draw_mode = True
                highlight_mode = False
                highlight_surface.fill(TRANSPARENT)
            elif draw_mode_button.collidepoint(mouse_pos):
                draw_mode = True
                text_mode = False
                eraser_mode = False
                highlight_mode = False
            elif highlight_mode_button.collidepoint(mouse_pos):
                highlight_mode = True
                text_mode = False
                eraser_mode = False
                draw_mode = False
            elif draw_mode and event.button == 1:
                start_pos = pygame.mouse.get_pos()
            elif highlight_mode and event.button == 1:
                start_pos = pygame.mouse.get_pos()
            elif text_mode and event.button == 1 and pygame.Rect(t_mouse_pos[0], t_mouse_pos[1], 100, 40).collidepoint(mouse_pos):
                text_dragging = True

        if event.type == pygame.MOUSEMOTION:
            if highlight_mode and pygame.mouse.get_pressed()[0]:
                end_pos = pygame.mouse.get_pos()
                if start_pos is not None:
                    pygame.draw.line(highlight_surface, SOFT_BLACK, start_pos, end_pos, 3)  # Draw with soft black
                    start_pos = end_pos
            if eraser_mode and pygame.mouse.get_pressed()[0]:
                pygame.draw.circle(win, WHITE, mouse_pos, eraser_size)
            prev_mouse_pos = mouse_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if draw_mode and event.button == 1 and start_pos is not None and not eraser_mode:
                end_pos = pygame.mouse.get_pos()
                pygame.draw.line(win, SOFT_BLACK, start_pos, end_pos, 2)
                start_pos = None
            elif highlight_mode and start_pos is not None:
                start_pos = None
            elif text_dragging:
                text_dragging = False

        if event.type == pygame.KEYDOWN and text_mode:
            pressed_key = pygame.key.name(event.key)
            if pressed_key == "space":
                key_log.append(" ")
            elif pressed_key == "backspace":
                if key_log:
                    key_log.pop()
            else:
                key_log.append(pressed_key)

    if text_mode:
        x_offset = 0
        for key in key_log:
            text = font.render(' '.join(key), True, SOFT_BLACK)
            win.blit(text, (t_mouse_pos[0] + x_offset, t_mouse_pos[1]))
            x_offset += text.get_width() + 1

    if text_dragging:
        t_mouse_pos = mouse_pos


    for button, label in [(text_mode_button, "Text"), (eraser_mode_button, "Eraser"),
                          (clear_screen_button, "Clear"), (draw_mode_button, "Draw"),
                          (highlight_mode_button, "Free Draw")]:
        if button.collidepoint(mouse_pos):
            draw_rounded_rect(win, button, ACCENT_COLOR, button_radius)
        else:
            draw_rounded_rect(win, button, LIGHT_GRAY, button_radius)

        text = font.render(label, True, DARK_GRAY if not button.collidepoint(mouse_pos) else WHITE)
        win.blit(text, (button.x + (button_width - text.get_width()) // 2, button.y + (button_height - text.get_height()) // 2))


    win.blit(highlight_surface, (0, 0))

    pygame.display.update()

pygame.quit()
sys.exit()