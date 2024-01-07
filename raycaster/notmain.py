import pygame

class Ray:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.endpoint = (self.x, self.y)
        self.length = length

    def render(self, screen):
        #print("heyy")
        pygame.draw.line(screen, (75, 75, 100), (self.x, self.y), self.endpoint, 2)
    
    def render_rect(self, screen, x, y, width, height):
        wallcolor = tuple(int(component * (1 - (1 / 500) * self.length)) for component in (129, 147, 126))
        for component in wallcolor:
            if(component < 0):
                wallcolor = (0, 0, 0)
        pygame.draw.rect(screen, wallcolor, (x, y, width, height))

    def cast(self, lines):
        return 0