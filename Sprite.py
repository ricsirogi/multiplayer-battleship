import pygame
import time


class Sprite(object):
    def __init__(self, clock: pygame.time.Clock, img: pygame.Surface, pos_x: int, ship_number: int):
        self.image = img
        self.x = pos_x
        self.y = 0
        self.follow = False
        self.pressed = False
        self.clock = clock
        self.was_rotated = False
        self.rotation = 0
        self.locked = False
        self.ship_number = ship_number
        self.rotate(90)
        self.time_of_pickup = 0
        self.time_of_last_click = 0
        self.time_of_lock = 0
        self.returned_value = None
        self.temp = 0

    def set_follow(self, new_follow: bool):
        self.follow = new_follow
        if self.follow:
            self.locked = False

    def check_click(self, other_active_ship_exists: int) -> int | None:
        if time.time() - 1 > self.temp:
            print(self.follow)
            self.temp = time.time()

        if time.time() - 0.2 < self.time_of_last_click:
            return
        click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.x <= mouse_pos[0] <= (self.x + self.image.get_width()) and self.y <= mouse_pos[1] <= (self.y + self.image.get_height()) and True in click:
            if click[0] and other_active_ship_exists == -1 and time.time() - 1 > self.time_of_last_click:
                print("clicked")
                # when the sprite is following the mouse I don't want to click it
                if self.follow or time.time() - 1 < self.time_of_lock:
                    print("followed or too early :C",
                          self.follow, self.time_of_lock)
                    return

                if self.locked:
                    self.time_of_pickup = time.time()
                    self.grid.locked_ships[str(self.ship_number)] = None
                self.follow = True
                self.locked = False
                print("picked up!")
                self.time_of_last_click = time.time()
                self.returned_value = self.ship_number
                return
            elif click[2]:
                print("reset!")
                self.follow = False
                self.returned_value = -1
                return
        self.returned_value = None

    def lock_in_grid(self, pos: tuple[int, int]) -> bool:
        if not self.locked:
            if time.time() - 1 > self.time_of_pickup:
                print("locked in grid!")
                self.x, self.y = pos[0], pos[1]
                self.locked = True
                self.follow = False
                self.time_of_lock = time.time()
                self.returned_value = None
                return True
            else:
                return False
        else:
            return False

    def get_grid(self, grid):
        self.grid = grid

    def rotate(self, angle: int):
        self.image = pygame.transform.rotate(self.image, angle)

    def return_value(self):
        return self.returned_value

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))
