import pygame
import pygame_widgets as pw
import sys

SIZE = WIDTH, HEIGHT = 500, 500
WHITE = [255, 255, 255]
SCREEN = pygame.display.set_mode(SIZE)
SCREEN.fill(WHITE)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
