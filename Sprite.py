import pygame


class Sprite(object):
    def __init__(self, clock):
        self.image = pygame.image.load(
            "weird shape.png").convert_alpha()
        self.x = 0
        self.y = 0
        self.follow = True
        self.pressed = False
        self.clock = clock
        self.was_clicked = pygame.mouse.get_pressed()[1]
        self.rotation = 0

    def set_follow(self, new_follow):
        self.follow = new_follow

    def lock_in_grid(self, pos: tuple[int, int]):
        self.x, self.y = pos[0], pos[1]

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))
