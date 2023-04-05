import pygame
import math
import numpy as np


class Grid(object):
    def __init__(self, pos: tuple[int, int], row_column: list[int], cell_size: list[int], cell_color: list[int], border_color: list[int], border_size: int, screen: pygame.Surface):
        self.row_column = row_column
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.border_color = border_color
        self.border_size = border_size
        self.pos = pos
        self.x_positions = []
        self.y_positions = []
        self.cells = []
        self.screen = screen
        self.ships = {}
        self.locked_ships = {}
        self.returned_value = None
        self.was_clicked = False

        border_width = self.cell_size[0] * self.row_column[1] + \
            (self.row_column[1] + 1) * self.border_size
        border_height = self.cell_size[1] * self.row_column[0] + \
            (self.row_column[0] + 1) * self.border_size

        self.border = pygame.Rect(
            (self.pos), (border_width, border_height))

        for i in range(self.row_column[0]):
            self.cells.append([])
            pos_y = self.pos[1] + self.cell_size[1] * i + \
                self.border_size * i + self.border_size
            if pos_y not in self.y_positions:
                self.y_positions.append(pos_y)

            for j in range(self.row_column[1]):
                pos_x = self.pos[0] + self.cell_size[0] * j + \
                    self.border_size * j + self.border_size
                if pos_x not in self.x_positions:
                    self.x_positions.append(pos_x)
                self.cells[i].append(pygame.Rect(
                    (pos_x, pos_y), self.cell_size))

    def get_mouse(self, ship=None):
        clicked = pygame.mouse.get_pressed()
        if not clicked[0] and not clicked[2]:
            self.was_clicked = False
        if self.border.collidepoint(pygame.mouse.get_pos()) and (clicked[0] or clicked[2]) and not self.was_clicked:
            self.was_clicked = True
            self.click(self.ships[str(ship)])
            self.returned_value = True

    def get_ships(self, ships: list):
        for c, i in enumerate(ships):
            self.ships[str(c)] = i

    def click(self, ship):
        pos = [ship.x, ship.y]

        closest_candidates = []
        coords_list = []

        for x in self.x_positions:
            for y in self.y_positions:
                closest_candidates.append(
                    math.sqrt(abs((pos[0] - x) ** 2) + abs(pos[1] - y) ** 2))  # this is distance between mouse position and currently selected coord)
                coords_list.append([x, y])

        temp = np.array(closest_candidates)
        closest_candidates.sort()
        temp = np.where(temp == closest_candidates[0])[0]
        closest_index = temp[0]

        print("trying to lock ship", coords_list[closest_index])
        successful_lock = ship.lock_in_grid(
            coords_list[closest_index])  # THIS is the coordinates of the coordinate that is closest to the mouse
        if successful_lock:
            print("lock successful")
            self.locked_ships[str(ship.ship_number)] = ship
            self.returned_value = True
        else:
            print("lock unsuccessful")
            self.returned_value = None

    def placed_ship(self):
        if self.returned_value:
            self.returned_value = None
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(self.screen, self.border_color, self.border)
        for c, i in enumerate(self.cells):
            for j in self.cells[c]:
                pygame.draw.rect(self.screen, self.cell_color, j)

    def __del__(self):
        for i in self.ships.values():
            if i is not None:
                i.set_follow(True)
