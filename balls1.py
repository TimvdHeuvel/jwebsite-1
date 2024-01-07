import pygame
import math
import numpy as np
import sys
import colorsys
pygame.init()

screenwidth = 1500
screenheight = 750

screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('BALLS!!!!!!!!!!')

x,y = 200,200
clock = pygame.time.Clock()
balls = []

class Ball:
    def __init__(self, mass, x, y, xv, yv):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.mass = mass

    def move(self):
        #if self.y > screenheight-10:
        #    self.yv *= -1
        #    self.y = screenheight-10
        #elif self.y < 10:
        #    self.yv *= -1
        #    self.y = 10

        #if self.x > screenwidth - 10:
        #    self.xv *= -1
        #    self.x = screenwidth - 10
        #elif self.x < 10:
        #    self.xv *= -1
        #    self.x = 10
        #else:
        #if(math.sqrt(self.xv**2 + self.yv**2) < 3):
        G = 3

        for b1 in balls:
            if b1 != self:
                angle = math.atan2(b1.y - self.y, b1.x - self.x)
                distance = math.dist((self.x, self.y), (b1.x, b1.y))
                self.xv += ((G * (self.mass * b1.mass) / (distance**2 / 3)) / self.mass) * math.cos(angle)
                self.yv += ((G * (self.mass * b1.mass) / (distance**2 / 3)) / self.mass) * math.sin(angle)
        

        self.x += self.xv
        self.y += self.yv
    
    def collision(self):
        for b1 in balls:
            if b1 == self:
                continue  # Skip self-comparison
            distance = math.dist((self.x, self.y), (b1.x, b1.y))
            if distance < 1.03 * self.mass + 1.03 * b1.mass:  # Adjust the collision radius as needed

                total_mass = self.mass + b1.mass
                #smass = self.mass
                #bmass = b1.mass
                sx = self.xv
                sy = self.yv
                bx = b1.xv
                by = b1.yv

                self.xv = (((self.mass - b1.mass) * sx + 2 * b1.mass * bx) / total_mass) * 0.95
                b1.xv = (((b1.mass - self.mass) * bx + 2 * self.mass * sx) / total_mass) * 0.95

                self.yv = (((self.mass - b1.mass) * sy + 2 * b1.mass * by) / total_mass) * 0.95
                b1.yv = (((b1.mass - self.mass) * by + 2 * self.mass * sy) / total_mass) * 0.95
                
                if(self.yv > 2):
                    self.yv = 0.5
                if(self.xv > 2):
                    self.xv = 0.5
                if(b1.yv > 2):
                    b1.yv = 0.5
                if(b1.xv > 10):
                    b1.xv = 0.5

                angle = math.atan2(b1.y - self.y, b1.x - self.x)
                overlap = (1.03 * self.mass + 1.03 * b1.mass) - distance  # Overlap distance
                selfmoveX = overlap * 0.5 * math.cos(angle)
                selfmoveY = overlap * 0.5 * math.sin(angle)
                othermoveX = overlap * 0.5 * math.cos(angle)
                othermoveY = overlap * 0.5 * math.sin(angle)
                # Move both balls away from each other based on overlap
                self.solve(b1, selfmoveX, selfmoveY, othermoveX, othermoveY)



    
    def solve(self, other, distSX, distSY, distOX, distOY):
        self.x -= distSX
        self.y -= distSY
        other.x += distOX
        other.y += distOY


    def rgb(ball):
        # colorsys.hsv_to_rgb returns RGB values in the range [0, 1]
        #print(ball.mass)
        #print((ball.mass - maxsize) / (minsize - maxsize))
        rgb = colorsys.hsv_to_rgb(((ball.mass - maxsize) / (minsize - maxsize)) / 6, 1, 1)
    
        # Convert the range [0, 1] to [0, 255]
        rgb = [int(val * 255) for val in rgb]
    
        return rgb

    def render(self):
        pygame.draw.circle(screen, self.rgb(), (self.x, self.y), self.mass + 0.9)

#mean_size = 11  # Adjust this value to set the mean of the distribution (mid-size)
#std_dev = 5  # Adjust this value to control the spread of the distribution

minsize = 5
maxsize = 25
#size_samples = np.clip(np.random.normal(loc=mean_size, scale=std_dev, size=200), minsize, maxsize)
ballcount = 100

for i in range(ballcount):
    #size = int(size_samples[i])
    b = Ball(np.random.randint(minsize, maxsize), np.random.randint(0, screenwidth), np.random.randint(0, screenheight), np.random.randint(-1, 1), np.random.randint(-1, 1))
    balls.append(b)

def explode(xpos, ypos):
    for ball in balls:
        #print(i)
        angle = math.atan2(ball.y - ypos, ball.x - xpos)
        distance = math.dist((ball.x, ball.y), (xpos, ypos))
        ball.xv += ((4 * 11 / (distance / 15)) / 1) * math.cos(angle)
        ball.yv += ((4 * 11 / (distance / 15)) / 1) * math.sin(angle)

def reset():
    #for ball in balls:
    #print(i)
    balls.clear()
    for i in range(ballcount):
    #size = int(size_samples[i])
        b = Ball(np.random.randint(minsize, maxsize), np.random.randint(0, screenwidth), np.random.randint(0, screenheight), np.random.randint(-1, 1), np.random.randint(-1, 1))
        balls.append(b)

def spawnball(xpos, ypos):
    b = Ball(np.random.randint(minsize, maxsize), xpos, ypos, -2.5, 2.5)
    balls.append(b)

substeps = 1
mouse_button_down = False

while True:
    screen.fill('black')
    for i in range(substeps):
        for b1 in balls:
            b1.move()
            b1.collision()
    for b1 in balls:
        b1.render()
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        #explode(mouse_x, mouse_y)
        #for b2 in balls:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            explode(mouse_x, mouse_y)
        elif events.type == pygame.MOUSEBUTTONDOWN and events.button == 2:
            reset()
        elif events.type == pygame.MOUSEBUTTONDOWN and events.button == 3:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            spawnball(mouse_x, mouse_y)

    pygame.display.update()
    clock.tick(50)