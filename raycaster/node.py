import pygame

class Node:
    def __init__(self, x, y,):
        self.x = x
        self.y = y

    def render(self, screen):
        #print("heyy")
        pygame.draw.circle(screen, (0, 150, 150), (self.x, self.y), 3)
