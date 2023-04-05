
import pygame
import pygame_textinput
from pygame_widgets_byme import *
import img
import sys
import re


class Main():
    def __init__(self):
        # Make the blank screen and initialize pygame
        pygame.init()
        self.SIZE = (1000, 800)
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Crazy stuff")
        self.screen.fill([255, 255, 255])

        # constant stuff

        self.EXIT_BUTTON_SIZE = (100, 50)
        self.EXIT_BUTTON_POS = (500, 500)
        self.EXIT_BUTTON_A_COLOR = [255, 0, 0]
        self.EXIT_BUTTON_IA_COLOR = [100, 0, 0]
        self.EXIT_BUTTON_TEXT_COLOR = [0, 0, 0]
        self.EXIT_BUTTON_MARGIN = 50
        self.EXIT_BUTTON_FONT_SIZE = 50

        self.GRID_MAKE_BUTTON_SIZE = (130, 50)
        self.GRID_MAKE_BUTTON_POS = (0, 750)
        self.GRID_MAKE_BUTTON_A_COLOR = [0, 0, 200]
        self.GRID_MAKE_BUTTON_IA_COLOR = [100, 0, 50]
        self.GRID_MAKE_BUTTON_TEXT_COLOR = [0, 0, 0]
        self.GRID_MAKE_BUTTON_MARGIN = 50
        self.GRID_MAKE_BUTTON_FONT_SIZE = 30

        self.GRID_BUTTON_POS = (200, 200)
        self.GRID_ROW_COLUMN = [10, 10]
        self.GRID_CELL_SIZE = [50, 50]
        self.GRID_CELL_COLOR = [200, 200, 200]
        self.GRID_BORDER_COLOR = [200, 0, 0]
        self.GRID_BORDER_SIZE = 1

        self.INPUT_BOX_POS = (160, 770)

        self.clock = pygame.time.Clock()

        self.grid = Grid.Grid(self.GRID_BUTTON_POS, self.GRID_ROW_COLUMN, self.GRID_CELL_SIZE,
                              self.GRID_CELL_COLOR, self.GRID_BORDER_COLOR, self.GRID_BORDER_SIZE, self.screen)

        self.ships = [Sprite.Sprite(self.clock, img.ship_images[i], i*70, i)
                      for i in range(5)]

        self.exit_button = Button.Button("EXIT", self.EXIT_BUTTON_POS, self.EXIT_BUTTON_SIZE,
                                         self.EXIT_BUTTON_A_COLOR, self.EXIT_BUTTON_IA_COLOR, self.EXIT_BUTTON_TEXT_COLOR, lambda: self.exit_command(), self.screen, self.EXIT_BUTTON_FONT_SIZE, 50)
        self.grid_make_button = Button.Button("SHOOT!", self.GRID_MAKE_BUTTON_POS, self.GRID_MAKE_BUTTON_SIZE,
                                              self.GRID_MAKE_BUTTON_A_COLOR, self.GRID_MAKE_BUTTON_IA_COLOR, self.GRID_MAKE_BUTTON_TEXT_COLOR, lambda: self.hit_command(), self.screen, self.GRID_MAKE_BUTTON_FONT_SIZE)
        self.buttons = [self.exit_button, self.grid_make_button]
        self.input_box = pygame_textinput.TextInputVisualizer()
        self.active_ship = -1

        # passing the objects to eachother, so they can communicate and stuff

        for i in self.ships:
            i.get_grid(self.grid)

        self.grid.get_ships(self.ships)

    def exit_command(self):
        print("Exitting...")
        sys.exit(0)

    def hit_command(self):
        text = self.input_box.value
        print(f"was clicked, text value:'{text}'")
        if re.fullmatch(r"\d+,\s*\d+", text) is not None:
            text += " "
            hit = self.grid.check_hit((int(text[0:text.find(",")]),
                                       int(text[text.find(",") + 1:-1])))
            if hit:
                print("hit!")

    """
    if we need custom grids

    text = input_box.value
    if re.fullmatch(r"\\d+,\\s*\\d+", text) is not None: # remove double backslash when you use this
        text += " "
        if grid_exists:
            del grid
        grid = Grid.Grid((200, 200), [int(text[0:text.find(",")]), int(text[text.find(",") + 1:-1])], [50, 50], [
            255, 255, 200], [0, 255, 0], 1, screen)
        grid_exists = True"""

    def follow_mouse(self):
        ship = self.ships[self.active_ship]
        if ship.follow:
            mouse_pos = pygame.mouse.get_pos()
            ship.x = mouse_pos[0] - int(ship.image.get_width()/2)
            ship.y = mouse_pos[1] - int(ship.image.get_height()/2)

            if pygame.mouse.get_pressed()[1] and pygame.mouse.get_pressed()[1] != ship.was_rotated:
                ship.rotation += 1
                ship.rotate(90)

            ship.was_rotated = pygame.mouse.get_pressed()[1]
            ship.draw(self.screen)

    def grid_stuff(self):
        self.grid.draw()

        if self.active_ship != -1:
            temp = self.active_ship
            self.grid.get_mouse(self.active_ship)
            placed_ship = self.grid.placed_ship()
            self.active_ship = -1 if placed_ship else self.active_ship
            if self.active_ship != temp:
                print("grid changed active ship:",
                      temp, "->", self.active_ship)
            return placed_ship

    def button_stuff(self):
        for button in self.buttons:
            button.get_mouse()
            button.draw()

    def ship_stuff(self, grid_locked_sprite_this_frame):
        temp = self.active_ship

        if self.active_ship != -1:
            self.follow_mouse()

        if not grid_locked_sprite_this_frame:
            returned_values = []
            for ship in self.ships:
                ship.check_click(self.active_ship)
                ship.draw(self.screen)
                returned_values.append(ship.return_value())

            for i in returned_values:
                if i == None:
                    continue
                if i == -1:
                    self.active_ship = -1
                else:
                    self.active_ship = i
        else:
            for c, ship in enumerate(self.ships):
                if c == self.active_ship:  # so there isn't a flicker when I rotate
                    continue
                ship.draw(self.screen)
        if self.active_ship != temp:
            print(temp, "->", self.active_ship)

    def mainloop(self):
        while True:
            temp = self.active_ship
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            if pygame.key.get_pressed()[pygame.key.key_code("d")] and pygame.mouse.get_pressed()[0]:
                print("Debugging...")
            self.screen.fill([255, 255, 255])

            self.button_stuff()

            grid_locked_sprite_this_frame = self.grid_stuff()

            self.ship_stuff(grid_locked_sprite_this_frame)

            self.input_box.update(events)  # type: ignore

            self.screen.blit(self.input_box.surface, self.INPUT_BOX_POS)
            pygame.display.flip()
            self.clock.tick(75)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
