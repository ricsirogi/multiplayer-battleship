import pygame


class Button(object):
    global grid, grid_exists

    def __init__(self, text: str, pos: tuple[int, int], size: tuple[int, int], a_color: list[int], ia_color: list[int], text_color: list[int], command, screen, screen_size, exit_button_margin=None):
        self.text = text
        self.size = size
        self.a_color = a_color
        self.ia_color = ia_color
        self.text_color = text_color
        self.command = command
        self.screen = screen
        if exit_button_margin is None:
            self.pos = pos
        else:
            self.pos = (screen_size[0] - self.size[0] - exit_button_margin,
                        screen_size[1] - self.size[1] - exit_button_margin)

        self.rect = pygame.Rect(self.pos, self.size)
        self.font = pygame.font.SysFont("Arial", 50)

        self.mouse_is_on = False

    def get_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_is_on = self.rect.collidepoint(mouse_pos)
        if self.mouse_is_on and pygame.mouse.get_pressed()[0]:
            self.command()

    def draw(self):
        if self.mouse_is_on:
            color = self.a_color
        else:
            color = self.ia_color

        pygame.draw.rect(self.screen, color, self.rect)
        self.screen.blit(self.font.render(
            self.text, True, self.text_color), self.rect)