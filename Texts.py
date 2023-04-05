import pygame

pygame.font.init()

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
FONT_FAMILY = "Arial"
FONT_SIZE = 40

font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

numbers = [font.render(str(i + 1), True, [0, 0, 0]) for i in range(10)]
letters = [font.render(alphabet[i].upper(), True, [0, 0, 0])
           for i in range(10)]
