import pygame
pygame.init()


class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 0, 255)

    def drawButtons(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
