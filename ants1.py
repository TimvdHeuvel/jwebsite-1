import pygame
import math
import pygame.math as pm
import numpy as np
import sys
import colorsys
pygame.init()

screenwidth = 1500
screenheight = 750
maxspeed = 5
antcount = 100
grid = [[0 for _ in range(15)] for _ in range(15)]


screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('BALLS!!!!!!!!!!')

x,y = 200,200
clock = pygame.time.Clock()
ants = []
foods = []
specs = []
speclife = 800
#ic = 0

class Spec:
    def __init__(self, x, y, type,):
        self.x = x
        self.y = y
        self.life = speclife
        #if type is 1, it's a home spec, if it's 2 it's a food spec
        self.type = type
    
    #def render(self):
    #    pygame.draw.circle(screen, (85, 30, 55), (self.x, self.y), 2.5)
    
    def render(self):
        if(self.type == 1):
            pygame.draw.circle(screen, (0, 0, self.life * (125 / speclife)), (self.x, self.y), 2.5)
        else:
            pygame.draw.circle(screen, (self.life * (85 / speclife), self.life * (30 / speclife), self.life * (55 / speclife)), (self.x, self.y), 2.5)

class Base:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.foodcount = 0
    
    def render(self):
        pygame.draw.circle(screen, (110, 85, 60), (self.x, self.y), 20)

class Food:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
    
    def render(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 2)

class Ant:
    def __init__(self, x, y, xv, yv, color, angle,): #xv, yv):
        self.x = x
        self.y = y
        self.xv = np.random.uniform(-1, 1)
        self.yv = np.random.uniform(-1, 1)
        self.hasfood = 1
        self.color = color
        self.current_angle = angle
        #self.homespecs = []
        self.spectimer = 5

    def follow_pheromones(self):
        # Define the regions to check
        front_region = self.get_region_position(0)
        left_region = self.get_region_position(-np.pi/4)
        right_region = self.get_region_position(np.pi/4)

        # Count the number of specs in each region
        front_count = self.count_specs_in_region(front_region)
        left_count = self.count_specs_in_region(left_region)
        right_count = self.count_specs_in_region(right_region)

        # Determine the region with the maximum spec density
        max_count = max(front_count, left_count, right_count)

        # Adjust the angle based on the region with the maximum spec density
        if max_count == 0:
            return 0
        elif max_count == right_count:
            return np.pi/4
        elif max_count == left_count:
            return -np.pi/4
        else:
            return 0
        
    def get_region_position(self, angle_offset):
        # Calculate the position in front of the ant with a given angle offset
        angle = self.current_angle + angle_offset
        x_offset = 25 * np.cos(angle)  # Adjust the distance and size of the region
        y_offset = 25 * np.sin(angle)
        #pygame.draw.circle(screen, (50, 50, 50), (self.x + x_offset, self.y + y_offset), 15)
        return self.x + x_offset, self.y + y_offset

    def count_specs_in_region(self, position):
        # Count the number of specs near a given position
        region_radius = 15  # Adjust the radius of the region to check
        count = 0
        for spec in specs:
            if math.dist((spec.x, spec.y), position) < region_radius:
                if(spec.type != self.hasfood):
                    count += 1
        return count

    def move(self):
        random_angle = np.random.uniform(-np.pi / 6, np.pi / 6) + self.follow_pheromones()

        # Combine the random movement and following pheromones
        self.current_angle = math.atan2(self.yv, self.xv) + random_angle

        speed = 1
        dx = speed * np.cos(self.current_angle)
        dy = speed * np.sin(self.current_angle)
        
        self.x += dx
        self.y += dy

        damping = 0.3
        self.xv = damping * self.xv + (1 - damping) * np.cos(self.current_angle)
        self.yv = damping * self.yv + (1 - damping) * np.sin(self.current_angle)

        if(self.x > screenwidth ):
            self.xv *= -1
            self.x = screenwidth - 2
        elif(self.x < 0):
            self.xv *= -1
            self.x = 2
        elif(self.y > screenheight):
            self.yv *= -1
            self.y = screenheight - 2
        elif(self.y < 0):
            self.yv *= -1
            self.y = 2

        

    def collision(self):
        for food in foods:
            if(math.dist((self.x, self.y), (food.x, food.y)) < 5):
                foods.remove(food)
                self.hasfood = 2
                self.xv *= -1
                self.yv *= -1
    
    def basecheck(self):
        if(math.dist((self.x, self.y), (antbase.x, antbase.y)) < 20):
                self.hasfood = 1
                self.xv *= -1
                self.yv *= -1
                antbase.foodcount += 1
                if(antbase.foodcount > 3):
                    a = Ant(antbase.x, antbase.y, 0, 0, 10, 0)
                    ants.append(a)
                    antbase.foodcount = 0
                    print(ants.count)


    def spawnSpec(self):
        if(self.hasfood == 1):
            s = Spec(self.x, self.y, 1)
        else:
            s = Spec(self.x, self.y, 2)
        specs.append(s)
        self.spectimer = 50

    def rgb(ant):
        rgb = colorsys.hsv_to_rgb(((ant.color - maxsize) / (minsize - maxsize)) / 6, 1, 1)
    
        rgb = [int(val * 255) for val in rgb]
    
        return rgb
    
    def distance_to_spec(self, spec):
        return math.dist((self.x, self.y), (spec.x, spec.y))

    def render(self):
        color = (255, 165, 79)
        if(self.hasfood == 2):
            color = (255, 100, 100)
            pygame.draw.circle(screen, (0,255,0), (self.x + self.xv * 4, self.y + self.yv * 5), 2)
        else:
            pygame.draw.circle(screen, (215, 125, 35), (self.x + self.xv * 4, self.y + self.yv * 4), 3)
        pygame.draw.circle(screen, color, (self.x, self.y), 4)


minsize = 5
maxsize = 10
antbase = Base(0,0)
antbase.x = np.random.randint(100, screenwidth - 100)
antbase.y = np.random.randint(100, screenheight - 100)

for i in range(antcount):
    a = Ant(antbase.x, antbase.y, 0, 0, 10, 0)
    ants.append(a)
    s = Spec(antbase.x, antbase.y, 1)

def reset():
    ants.clear()
    for i in range(antcount):
        b = Ant(screenheight/2, screenwidth/2, 0.5, 0)
        ants.append(b)

def spawnball(xpos, ypos):
    b = Ant(np.random.randint(minsize, maxsize), xpos, ypos, -2.5, 2.5)
    ants.append(b)

def spawnfood(xpos, ypos):
    for i in range(10):
        f = Food(np.random.randint(xpos-10, xpos+10), np.random.randint(ypos-10, ypos+10))
        foods.append(f)          #finish spawn food function

def spawnspecs():
    for ant in ants:
        ant.spawnSpec()

substeps = 1
mouse_button_down = False
spawnfoods = False

while True:
    screen.fill('black')
    for i in range(substeps):
        for ant in ants:
            ant.spectimer -= 1
            ant.move()
            if(ant.hasfood == 1):
                ant.collision()
            else:
                ant.basecheck()
            if(ant.spectimer < 1):
                ant.spawnSpec()
    for spec in specs:
        spec.life -= 1
        spec.render()
        if(spec.life < 1):
            specs.remove(spec)
    for ant in ants:
        ant.render()
    for f in foods:
        f.render()
    antbase.render()
        #for b2 in balls:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
            mouse_button_down = True
        elif events.type == pygame.MOUSEBUTTONUP and events.button == 1:
            mouse_button_down = False
        elif events.type == pygame.MOUSEMOTION and mouse_button_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            spawnfood(mouse_x, mouse_y)
        elif events.type == pygame.MOUSEBUTTONDOWN and events.button == 2:
            specs.clear()
        elif events.type == pygame.MOUSEBUTTONDOWN and events.button == 3:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #spawnball(mouse_x, mouse_y)

    pygame.display.update()
    clock.tick(50)