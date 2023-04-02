
import pygame
import pygame_textinput
from pygame_widgets_byme import *
import sys
import re


def exit_command():
    print("Exitting...")
    sys.exit(0)


def grid_make_command():
    global grid, grid_exists
    text = input_box.value
    if re.fullmatch(r"\d+,\s*\d+", text) is not None:
        text += " "
        if grid_exists:
            del grid
        grid = Grid.Grid((200, 200), [int(text[0:text.find(",")]), int(text[text.find(",") + 1:-1])], [50, 50], [
            255, 255, 200], [0, 255, 0], 1, screen, square)
        grid_exists = True


def square_stuff():
    follow_mouse(square)
    square.draw(screen)
    pass


def follow_mouse(square: Sprite.Sprite):
    if square.follow:
        mouse_pos = pygame.mouse.get_pos()
        square.x = mouse_pos[0]
        square.y = mouse_pos[1]
        if square.rotation % 2 == 1 and square.follow:
            square.x -= 51

        if pygame.mouse.get_pressed()[1] and pygame.mouse.get_pressed()[1] != square.was_clicked:
            square.rotation += 1
            square.rotate(-90)

        square.was_clicked = pygame.mouse.get_pressed()[1]


def button_stuff():
    for button in buttons:
        button.get_mouse()
        button.draw()


def grid_stuff():
    grid.draw()  # type: ignore
    grid.get_mouse()  # type: ignore


# Make the blank screen and initialize pygame
pygame.init()
SIZE = (1000, 800)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Crazy stuff")
screen.fill([255, 255, 255])

# constant stuff

EXIT_BUTTON_SIZE = (100, 50)
EXIT_BUTTON_POS = (500, 500)
EXIT_BUTTON_A_COLOR = [255, 0, 0]
EXIT_BUTTON_IA_COLOR = [100, 0, 0]
EXIT_BUTTON_TEXT_COLOR = [0, 0, 0]
EXIT_BUTTON_MARGIN = 50

GRID_MAKE_BUTTON_SIZE = (130, 50)
GRID_MAKE_BUTTON_POS = (0, 750)
GRID_MAKE_BUTTON_A_COLOR = [0, 0, 200]
GRID_MAKE_BUTTON_IA_COLOR = [100, 0, 50]
GRID_MAKE_BUTTON_TEXT_COLOR = [0, 0, 0]
GRID_MAKE_BUTTON_MARGIN = 50

INPUT_BOX_POS = (160, 770)

clock = pygame.time.Clock()
square = Sprite.Sprite(clock)
exit_button = Button.Button("EXIT", EXIT_BUTTON_POS, EXIT_BUTTON_SIZE,
                            EXIT_BUTTON_A_COLOR, EXIT_BUTTON_IA_COLOR, EXIT_BUTTON_TEXT_COLOR, lambda: exit_command(), screen, [1000, 800], 50)
grid_make_button = Button.Button("MAKE!", GRID_MAKE_BUTTON_POS, GRID_MAKE_BUTTON_SIZE,
                                 GRID_MAKE_BUTTON_A_COLOR, GRID_MAKE_BUTTON_IA_COLOR, GRID_MAKE_BUTTON_TEXT_COLOR, lambda: grid_make_command(), screen, [1000, 800],)
buttons = [exit_button, grid_make_button]
grid = None
input_box = pygame_textinput.TextInputVisualizer()
grid_exists = False


while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill([255, 255, 255])

    button_stuff()
    if grid_exists:
        grid_stuff()
    square_stuff()

    input_box.update(events)  # type: ignore

    screen.blit(input_box.surface, INPUT_BOX_POS)
    pygame.display.update()
    clock.tick(75)
