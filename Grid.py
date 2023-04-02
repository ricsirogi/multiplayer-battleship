import pygame
import math


class Grid(object):
    def __init__(self, pos: tuple[int, int], row_column: list[int], cell_size: list[int], cell_color: list[int], border_color: list[int], border_size: int, screen, square):
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
        self.square = square

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
            self.y_positions.append(pos_y)
            for j in range(self.row_column[1]):
                pos_x = self.pos[0] + self.cell_size[0] * j + \
                    self.border_size * j + self.border_size
                self.x_positions.append(pos_x)
                self.cells[i].append(pygame.Rect(
                    (pos_x, pos_y), self.cell_size))

    def get_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_is_on = self.border.collidepoint(mouse_pos)
        if self.mouse_is_on and pygame.mouse.get_pressed()[0]:
            self.click()
        elif self.mouse_is_on and pygame.mouse.get_pressed()[2]:
            print("This is as debug")

    def click(self):
        """

        closest = []
        coords_list = []

        for x in x_positions:
            for y in y_positions:
                closest.append(
                    math.sqrt( (mouse_pos[0] - x))^2 + ((mouse_pos[1] - (y))^2 # this is distance between mouse position and currently selected coord
                    )
                    coords_list.append([x, y])

        coords_list[indexOf(closest.min())] # THIS is the coordinates of the coordinate that is closest to the mouse
        """

        mouse_pos = pygame.mouse.get_pos()
        """self.closest_x = -1
        self.closest_y = -1

        for y in self.y_positions:
            if abs(self.closest_y - y) < abs(mouse_pos[1] - self.closest_y):
                self.closest_y = y

        for x in self.x_positions:
            if abs(self.closest_x - x) < abs(mouse_pos[0] - self.closest_x):
                self.closest_x = x"""

        closest_candidates = []
        coords_list = []

        for x in self.x_positions:
            for y in self.y_positions:
                closest_candidates.append(
                    math.sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2))  # this is distance between mouse position and currently selected coord)
                coords_list.append([x, y])

        temp = closest_candidates
        closest_candidates.sort()

        self.square.set_follow(False)
        self.square.lock_in_grid(
            print(coords_list[temp.index(closest_candidates[0])]))  # THIS is the coordinates of the coordinate that is closest to the mouse

    def draw(self):
        pygame.draw.rect(self.screen, self.border_color, self.border)
        for c, i in enumerate(self.cells):
            for j in self.cells[c]:
                pygame.draw.rect(self.screen, self.cell_color, j)

    def __del__(self):
        self.square.set_follow(True)
