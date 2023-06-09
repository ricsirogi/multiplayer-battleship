
import pygame
import pygame_textinput
from pygame_widgets_byme import *
import img
import sys
import re


def exit_command():
    print("Exitting...")
    sys.exit(0)


"""
if we need custom grids

text = input_box.value
if re.fullmatch(r"\d+,\s*\d+", text) is not None:
    text += " "
    if grid_exists:
        del grid
    grid = Grid.Grid((200, 200), [int(text[0:text.find(",")]), int(text[text.find(",") + 1:-1])], [50, 50], [
        255, 255, 200], [0, 255, 0], 1, screen)
    grid_exists = True"""


def follow_mouse(square: Sprite.Sprite):
    if square.follow:
        mouse_pos = pygame.mouse.get_pos()
        square.x = mouse_pos[0]
        square.y = mouse_pos[1]

        if pygame.mouse.get_pressed()[1] and pygame.mouse.get_pressed()[1] != square.was_rotated:
            square.rotation += 1
            square.rotate(90)

        square.was_rotated = pygame.mouse.get_pressed()[1]


def grid_stuff():
    global active_ship

    grid.draw()

    if active_ship != -1:
        grid.get_mouse(active_ship)
        placed_ship = grid.placed_ship()
        active_ship = -1 if placed_ship else active_ship
        return placed_ship


def button_stuff():
    for button in buttons:
        button.get_mouse()
        button.draw()


def ship_stuff(grid_locked_sprite_this_frame):
    global active_ship

    temp = active_ship

    if active_ship != -1:
        follow_mouse(ships[active_ship])

    if not grid_locked_sprite_this_frame:
        returned_values = []
        for ship in ships:
            ship.check_click(active_ship)
            ship.draw(screen)
            returned_values.append(ship.return_value())

        for i in returned_values:
            if i == None:
                continue
            if i == -1:
                active_ship = -1
            else:
                active_ship = i
    if active_ship != temp:
        print(temp, "->", active_ship)


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

grid = Grid.Grid((200, 200), [10, 10], [50, 50], [
    255, 255, 200], [0, 255, 0], 1, screen)

ships = [Sprite.Sprite(clock, img.ship_images[i], i*70, i) for i in range(5)]

exit_button = Button.Button("EXIT", EXIT_BUTTON_POS, EXIT_BUTTON_SIZE,
                            EXIT_BUTTON_A_COLOR, EXIT_BUTTON_IA_COLOR, EXIT_BUTTON_TEXT_COLOR, lambda: exit_command(), screen, [1000, 800], 50)
"""grid_make_button = Button.Button("MAKE!", GRID_MAKE_BUTTON_POS, GRID_MAKE_BUTTON_SIZE,
                                 GRID_MAKE_BUTTON_A_COLOR, GRID_MAKE_BUTTON_IA_COLOR, GRID_MAKE_BUTTON_TEXT_COLOR, lambda: grid_make_command(), screen, [1000, 800],)
"""
buttons = [exit_button]
input_box = pygame_textinput.TextInputVisualizer()
active_ship = -1

# passing the objects to eachother, so they can communicate and stuff

for i in ships:
    i.get_grid(grid)

grid.get_ships(ships)

while True:
    temp = active_ship
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    if pygame.key.get_pressed()[pygame.key.key_code("d")] and pygame.mouse.get_pressed()[0]:
        print("Debugging...")
    screen.fill([255, 255, 255])

    button_stuff()

    print("active_ship before grid:", active_ship)
    grid_locked_sprite_this_frame = grid_stuff()
    print("active_ship after grid:", active_ship, "\n")

    print("active_ship before ship:", active_ship)
    ship_stuff(grid_locked_sprite_this_frame)
    print("active_ship after ship:", active_ship, "\n\n")

    input_box.update(events)  # type: ignore

    screen.blit(input_box.surface, INPUT_BOX_POS)
    pygame.display.update()
    """if active_ship != temp:
        print(active_ship, temp)
        clock.tick(0.5)"""
    clock.tick(5)
