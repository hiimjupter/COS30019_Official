import pygame
from helpers.constant import MEDIUM_FONT, COLORS


class Button:
    def __init__(self, screen, rect, text, font=MEDIUM_FONT, text_color=COLORS['BLUE'], button_color=COLORS['WHITE']):
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color

    def render(self):
        pygame.draw.rect(self.screen, self.button_color, self.rect)
        button_text = self.font.render(self.text, True, self.text_color)
        text_rect = button_text.get_rect(center=self.rect.center)
        self.screen.blit(button_text, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
