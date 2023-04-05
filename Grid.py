import pygame
import math
import numpy as np
import Texts


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
        self.hits = {}
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

    def get_ships(self, ships: list):
        for c, i in enumerate(ships):
            self.ships[str(c)] = i

    def remove_from_grid(self, ship_num):
        self.locked_ships.pop(str(ship_num))

    def click(self, ship):
        pos = (ship.x, ship.y)

        closest_index = self.find_closest_cell(
            self.check_place_validity(ship))

        if closest_index == (0, 0):
            return
        print("after all that hard work the closest index is ", closest_index)
        successful_lock = ship.lock_in_grid(closest_index)
        if successful_lock:
            self.save_ship(ship, closest_index)
            self.returned_value = True
        else:
            self.returned_value = None

    def find_closest_cell(self, pos: tuple[int, int]) -> tuple[int, int]:
        if pos == (0, 0):
            return pos
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

        # THIS is the coordinates of the coordinate that is closest to the mouse
        closest_index = coords_list[closest_index]

        return tuple(closest_index)

    def check_place_validity(self, ship) -> tuple[int, int]:
        """
        checks wether the placement of the new ship is valid or not
        """
        ship_number = ship.ship_number
        ship_coordinate = (ship.x, ship.y)
        ship_rotation = ship.rotation
        # checking if it's outside of a grid
        if ship_number < 2:
            length = ship_number + 2
        else:
            length = ship_number + 1

        x = self.real_round((ship_coordinate[0] - self.pos[0]) / 50)
        y = self.real_round((ship_coordinate[1] - self.pos[1]) / 50)

        new_coordinate = list(ship_coordinate)
        validity = []
        # even numbers are horizontal, odd numbers are vertical
        if ship_rotation % 2 == 1:
            # x coordinate of wannabe-ship plus it's length
            if x + length <= 10:
                validity.append(True)
            else:
                validity.append(False)
                new_coordinate[0] -= ((length + x) - 10) * 50
        else:
            # x coordinate of wannabe-ship plus it's length
            if y + length <= 10:
                validity.append(True)
            else:
                validity.append(False)
                new_coordinate[1] -= ((length + y) - 10) * 50

        # checking if it's colliding with any other ships in the grid
        if self.check_hit(ship_coordinate, [ship.image.get_width(), ship.image.get_height()]):
            return (0, 0)
        else:
            return ship_coordinate if False not in validity else tuple(new_coordinate)

    def check_hit(self, hit_cord: tuple[int, int], ship_size: list[int] = [50, 50]) -> bool:
        if self.locked_ships != {}:
            hit = False
            hit_ship = None
            for i in self.locked_ships.values():
                checing_ship = i[0]
                checking_ship_rectangle = pygame.rect.Rect(
                    list(i[1]), [checing_ship.image.get_width(), checing_ship.image.get_height()])
                existing_ship_rectangle = pygame.rect.Rect(
                    hit_cord, ship_size)
                hit = checking_ship_rectangle.colliderect(
                    existing_ship_rectangle)
                if hit:
                    hit_ship = checing_ship
                    break
                else:
                    continue
            if hit and hit_ship is not None:
                x = self.real_round((hit_cord[0] - self.pos[0]) / 50)
                y = self.real_round((hit_cord[1] - self.pos[1]) / 50)
                hit_cord = (x, y)
                if hit_cord not in self.locked_ships[str(hit_ship.ship_number)][2]:
                    self.locked_ships[str(hit_ship.ship_number)][2].append(
                        hit_cord)
                    ship_number = hit_ship.ship_number
                    if ship_number < 2:
                        length = ship_number + 2
                    else:
                        length = ship_number + 1
                    if len(self.locked_ships[str(hit_ship.ship_number)][2]) == length:
                        hit_ship.die()
                return True
            else:
                return False
        else:
            return False

    def save_ship(self, ship, ship_coordinate: tuple[int, int]):
        self.locked_ships[str(ship.ship_number)] = [
            ship, ship_coordinate, []]  # The empty list is for storing the cordinates of the hits
        print(
            f"ship {ship.ship_number} saved at {self.locked_ships[str(ship.ship_number)][1]}")

    def real_round(self, number: float) -> int:
        """
        scuffed rounding
        """

        if number == int(number):
            return int(number)
        # print("checking the number:", number, "->", str(number/10)[3])
        if int(str(number/10)[3]) < 6:
            return int(number)
        else:
            return int(number) + 1

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
        for c, i in enumerate(Texts.numbers):
            pos_x = self.pos[0] + c * 50 + c * 1 + 15
            self.screen.blit(i, (pos_x, self.pos[1]-50))
        for c, i in enumerate(Texts.letters):
            pos_y = self.pos[1] + c * 50 + c * 1
            self.screen.blit(i, (self.pos[0]-40, pos_y))

    def __del__(self):
        for i in self.ships.values():
            if i is not None:
                i.set_follow(True)
