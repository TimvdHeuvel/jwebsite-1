import pygame
import sys
import math
import notmain as ray
import node as n


# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Controllable Sphere")

#vertices
nodes = []

# Sphere parameters
raylength = 300
raycount = 120
fov = 1
player_radius = 10
player_color = (255, 0, 0)  # Red

# Dot parameters
dot_radius = 2
dot_color = (0, 255, 0)  # Green

# Initial position and angle
x, y = width // 2, height // 2
angle = 0

# Movement speed
speed = 3.5
angle_speed = math.radians(4)  # 5 degrees in radians

# Function to find the closest node to the mouse position
def find_closest_node(mouse_x, mouse_y):
    closest_node = None
    min_distance = float('inf')  # Initialize with infinity

    for node in nodes:
        distance = math.hypot(node.x - mouse_x, node.y - mouse_y)
        if distance < min_distance and node != nodes[-1]:
            min_distance = distance
            closest_node = node

    return closest_node

# Function to check if the player has crossed a line using ray-casting
def has_crossed_line(player_x, player_y, polygon):
    count = 0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i - 1]
        if (y1 > player_y) != (y2 > player_y) and player_x < (x2 - x1) * (player_y - y1) / (y2 - y1) + x1:
            count += 1
    return count % 2 == 1

# Game loop
running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #screen.fill((40, 45, 40))
    background_image = pygame.image.load("raycaster_background.png")
    background_image = pygame.transform.scale(background_image, (width, height))

    screen.blit(background_image, (0, 0)) 

    polygon_points = [(node.x, node.y) for node in nodes]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                node = n.Node(mouse_x, mouse_y)
                nodes.append(node)
            elif event.button == 3:
                nodes.remove(nodes[-1])

    keys = pygame.key.get_pressed()

    # Update position based on keys
    if keys[pygame.K_s]:
        new_y = y - speed * math.sin(angle)
        new_x = x - speed * math.cos(angle)
        for i, node in enumerate(nodes):
            if i == len(nodes) - 1:
                nodes[i].render(screen)
                next_node = nodes[0]
            else:
                next_node = nodes[i + 1]
            if has_crossed_line(new_x, new_y, polygon_points):
                y = new_y
                x = new_x

    elif keys[pygame.K_w]:
        new_y = y + speed * math.sin(angle)
        new_x = x + speed * math.cos(angle)
        for i, node in enumerate(nodes):
            if i == len(nodes) - 1:
                next_node = nodes[0]
            else:
                next_node = nodes[i + 1]
            if has_crossed_line(new_x, new_y, polygon_points):
                y = new_y
                x = new_x

    rayangle = fov
    for i in range(raycount):
        r = ray.Ray(x, y, 0)
        #print(angle)
        a = 0
        if(len(nodes) > 2):
            a = angle + rayangle
            r.endpoint = (x + r.length * math.cos(a), y + r.length * math.sin(a))
            j = 0
            while has_crossed_line(r.endpoint[0], r.endpoint[1], polygon_points):
                j += 1
                if (j > raylength):
                    r.endpoint = (x, y)
                    break
                else:
                    r.length += 3
                    r.endpoint = (x + r.length * math.cos(a), y + r.length * math.sin(a))
            else:
                for k in range(3):
                    if not has_crossed_line(r.endpoint[0], r.endpoint[1], polygon_points):
                        r.length -= 1
                        r.endpoint = (x + r.length * math.cos(a), y + r.length * math.sin(a))
        rectheight = height - r.length * math.cos(rayangle)
        r.render_rect(screen, (width / raycount) * (raycount - (i + 1)), (height / 2) - (rectheight / 2), (width / raycount + 1), rectheight)
        r.render(screen)
        rayangle -= (fov * 2) / raycount


    if keys[pygame.K_a]:
        angle -= angle_speed

    if keys[pygame.K_d]:
        angle += angle_speed

    for i, node in enumerate(nodes):
        # node.render(screen)
        if i == len(nodes) - 1:
            next_node = nodes[0]
        else:
            next_node = nodes[i + 1]
        pygame.draw.line(screen, (85, 0, 110), (node.x, node.y), (next_node.x, next_node.y), 2)
        #node.render(screen)

    # Draw the sphere with updated position and angle
    sphere_center = (int(x), int(y))
    pygame.draw.circle(screen, player_color, sphere_center, player_radius)

    # Draw a line representing the angle of movement
    line_length = 20
    line_end = (
        int(x + line_length * math.cos(angle)),
        int(y + line_length * math.sin(angle))
    )
    pygame.draw.line(screen, (0, 0, 255), sphere_center, line_end, 2)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
