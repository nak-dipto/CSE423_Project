from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, radians, pi
import random
# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
PI = pi
paused = False
game_over = False
game_won = False
shooter_x = WINDOW_WIDTH// 2
shooter_y = 50
shooter_width = 15
shooter_height = 10
comets = []
sun={"x": WINDOW_WIDTH//2, "y": WINDOW_HEIGHT//2, "color": (1.0, 1.0, 0.0), 'size' : 23}
# Planet properties
g_speed = 0
stars=[[random.randint(0, WINDOW_HEIGHT),random.randint(0, WINDOW_HEIGHT)] for i in range(50)]
planets = [
    {"distance": 35, "size": 6, "speed": 0.8, "angle": random.randint(0, 360), "color": (0.7, 0.7, 0.7)},  # Mercury
    {"distance": 60, "size": 8, "speed": 0.6, "angle": random.randint(0, 360), "color": (1.0, 0.9, 0.6)},  # Venus
    {"distance": 90, "size": 12, "speed": 0.3, "angle": random.randint(0, 360), "color": (0.1, 0.3, 0.7)},  # Earth
    {"distance": 120, "size": 10, "speed": 0.2, "angle": random.randint(0, 360), "color": (0.8, 0.3, 0.2)},  # Mars
    {"distance": 180, "size": 18, "speed": 0.1, "angle": random.randint(0, 360), "color": (0.9, 0.8, 0.7)},  # Jupiter
    {"distance": 240, "size": 15, "speed": 0.07, "angle": random.randint(0, 360), "color": (1.0, 0.9, 0.5)},  # Saturn
    {"distance": 300, "size": 12, "speed": 0.05, "angle": random.randint(0, 360), "color": (0.6, 0.8, 0.9)},  # Uranus
    {"distance": 360, "size": 12, "speed": 0.03, "angle": random.randint(0, 360), "color": (0.2, 0.4, 0.8)},  # Neptune
]

play_box = {
    'width': 20,
    'height': 20,
    'up': (390, 795),
    'down': (390, 775),
    'right': (410, 785),
    'color': (0, 1, 0),
}
pause_box = {
    'width': 20,
    'height': 20,
    'up1': (395, 795),
    'down1': (395, 775),
    'up2': (405, 795),
    'down2': (405, 775),
    'color': (1, 0.75, 0),
}


def MPC(r, color, center):
    x = 0
    y = r
    d = 1 - r
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x = x + 1
        else:
            d = d + 2 * x - 2 * y + 5
            x = x + 1
            y = y - 1
        Circlepoints(x, y, color, center)

def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    else:
        if dx > 0 and dy > 0:
            zone = 1
        elif dx <= 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy <= 0:
            zone = 6
    return zone

def Circlepoints(x, y, color, center):
    draw_points(x+center[0], y+center[1], color)
    draw_points(-x+center[0], y+center[1], color)
    draw_points(x+center[0], -y+center[1], color)
    draw_points(-x+center[0], -y+center[1], color)
    draw_points(y+center[0], x+center[1], color)
    draw_points(-y+center[0], x+center[1], color)
    draw_points(y+center[0], -x+center[1], color)
    draw_points(-y+center[0], -x+center[1], color)

def ConverttoZoneZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def ConvertfromZoneZero(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def MLA(x1, y1, x2, y2, color, control=False):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConverttoZoneZero(x1, y1, zone)
    x2, y2 = ConverttoZoneZero(x2, y2, zone)
    if x1>x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dNE = 2 * (dy - dx)
    dE = 2 * dy
    x = x1
    y = y1
    while x <= x2:
        draw_points(*ConvertfromZoneZero(x, y, zone), color)
        x += 1
        if d < 0:
            d += dE
        else:
            d += dNE
            y += 1

def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_shooter():
    glColor3f(0,0,0.9)
    glBegin(GL_POINTS)
    for x in range(shooter_x - shooter_width // 2, shooter_x + shooter_width // 2):
        for y in range(shooter_y, shooter_y + shooter_height):
            glVertex2f(x, y)
    glEnd()

def check_shooter_comet_collision():
    """Check if the shooter collides with any comet."""
    global game_over
    for comet in comets:
        dx = shooter_x - comet.x
        dy = shooter_y - comet.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance <= comet.size + shooter_width // 2:
            game_over = True
            break

def check_shooter_sun_collision():
    """Check if the shooter reaches the sun."""
    global game_won
    # Sun is at the center (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    sun_x = sun['x']
    sun_y = sun['y']
    dx = shooter_x - sun_x
    dy = shooter_y - sun_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance <= sun['size'] + shooter_width // 2:
        game_won = True

def draw_button():
    global paused
    if not paused:
        # PAUSE
        MLA(*pause_box['up1'],*pause_box['down1'], pause_box['color'],True)
        MLA(*pause_box['up2'],*pause_box['down2'], pause_box['color'],True)
    else:
        # PLAY
        MLA(*play_box['right'],*play_box['up'], play_box['color'],True)
        MLA(*play_box['right'],*play_box['down'], play_box['color'],True)
        MLA(*play_box['up'],*play_box['down'], play_box['color'],True)

def draw_orbit():
    for planet in planets:
        # Draw the orbit
        MPC(planet["distance"], (.5,.5,.5), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

class Comet:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        angle = random.uniform(0, 2 * pi)
        self.speed_x = random.uniform(5, 10) * cos(angle)  # Faster speed
        self.speed_y = random.uniform(5, 10) * sin(angle)
        self.size = random.randint(1, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        glColor3f(1.0, 0.0, 0.0)  # Red for comet
        draw_filled_circle(self.x, self.y, self.size, (1.0, 0.0, 0.0))  # Draw filled comet

def draw_filled_circle(x, y, r, color):
    """Draw a filled circle using MPC."""
    for radius in range(int(r), 0, -1):  # Cast r to integer
        MPC(radius, color, (x, y))

def update_comets():
    """Update the positions of comets and check for collisions."""
    global comets, planets

    comets_to_remove = []  # List of comets to remove after collisions
    planets_to_remove = []  # List of planets to remove after being hit twice

    for comet in comets:
        comet.x += comet.speed_x  # Update comet's x position
        comet.y += comet.speed_y  # Update comet's y position

        # Check for collisions with planets
        for planet in planets:
            planet_x = planet['x']
            planet_y = planet['y']

            dx = comet.x - planet_x
            dy = comet.y - planet_y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance <= planet["size"]:  # Collision detected
                # Shrink the planet and increase hit count
                if "hit_count" not in planet:
                    planet["hit_count"] = 0  # Initialize hit count
                planet["hit_count"] += 1
                # planet["size"] *= 0.8  # Shrink the planet by 20%
                planet["size"] = round(planet["size"]* 0.9)  # Shrink the planet by 20%

                # Mark the comet for removal
                if comet not in comets_to_remove:
                    comets_to_remove.append(comet)

                # Destroy the planet if hit twice
                if planet["hit_count"] >= 4 and planet not in planets_to_remove:
                    planets_to_remove.append(planet)
    # Remove marked comets and planets
    for comet in comets_to_remove:
        comets.remove(comet)
    for planet in planets_to_remove:
        planets.remove(planet)

def draw_comets():
    for comet in comets:
        comet.move()
        comet.draw()

def check_shooter_planet_collision():
    """Check if the shooter collides with any comet."""
    global game_over
    for planet in planets:
        dx = shooter_x - planet['x']
        dy = shooter_y - planet['y']
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance <= planet['size'] + shooter_width // 2:
            game_over = True
            break        

def draw_planets():
    # Draw the Sun
    for i in range(sun['size']):
        MPC(i, (1.0, 1.0, 0.0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    # Draw planets and their orbits
    for planet in planets:
        # Calculate planet position
        planet["angle"] += planet["speed"]
        if planet["angle"] > 360:
            planet["angle"] -= 360

        rad_angle = radians(planet["angle"])
        planet_x = WINDOW_WIDTH // 2 + planet["distance"] * cos(rad_angle)
        planet_y = WINDOW_HEIGHT // 2 + planet["distance"] * sin(rad_angle)
        planet['x']=planet_x
        planet['y']=planet_y
        # Draw the planet
        for i in range(0, planet["size"]):
            MPC(i, planet['color'], (planet_x, planet_y))
        # MPC(planet['size'], planet['color'], (planet_x, planet_y))

def draw_stars():
    draw_points(50,50,(1,1,1))
    for i in stars:
        draw_points(*i,(1,1,1))

def reset_game():
    global planets, shooter_x, shooter_y, paused, shooter_width, shooter_height,g_speed,sun,comets,game_over,game_won
    shooter_x = WINDOW_WIDTH // 2
    shooter_y = 50
    comets = []
    # Planet properties
    g_speed = 0
    planets = [
        {"distance": 35, "size": 6, "speed": 0.8, "angle": random.randint(0, 360), "color": (0.7, 0.7, 0.7)},  # Mercury
        {"distance": 60, "size": 8, "speed": 0.6, "angle": random.randint(0, 360), "color": (1.0, 0.9, 0.6)},  # Venus
        {"distance": 90, "size": 12, "speed": 0.3, "angle": random.randint(0, 360), "color": (0.1, 0.3, 0.7)},  # Earth
        {"distance": 120, "size": 10, "speed": 0.2, "angle": random.randint(0, 360), "color": (0.8, 0.3, 0.2)},  # Mars
        {"distance": 180, "size": 18, "speed": 0.1, "angle": random.randint(0, 360), "color": (0.9, 0.8, 0.7)},  # Jupiter
        {"distance": 240, "size": 15, "speed": 0.07, "angle": random.randint(0, 360), "color": (1.0, 0.9, 0.5)},  # Saturn
        {"distance": 300, "size": 12, "speed": 0.05, "angle": random.randint(0, 360), "color": (0.6, 0.8, 0.9)},  # Uranus
        {"distance": 360, "size": 12, "speed": 0.03, "angle": random.randint(0, 360), "color": (0.2, 0.4, 0.8)},  # Neptune
    ]
    sun={"x": WINDOW_WIDTH//2, "y": WINDOW_HEIGHT//2, "color": (1.0, 1.0, 0.0), 'size' : 23}
    paused = False
    comets=[]
    game_over=False
    game_won=False
    # print("Resetting game...")

def draw_restart_button():
    button_x = 10
    button_y = WINDOW_HEIGHT - 15
    button_width = 20
    button_height = 20

    glColor3f(0, 1, 0)

    #rectangle background for the Restart button
    glBegin(GL_POINTS)
    for x in range(button_x - button_width // 2, button_x + button_width // 2):
        for y in range(button_y - button_height // 2, button_y + button_height // 2):
            glVertex2f(x, y)
    glEnd()

    # Draw the arrow inside the Restart button
    glColor3f(0, 0, 0)
    glBegin(GL_POINTS)
    # Arrow part
    for x in range(0, 11): #Left Side
        for y in range(-10 + x, 11 - x):
            glVertex2f(button_x - x, button_y + y)

        # Horizontal line part(Right Side)
    for x in range(1, 11):
        glVertex2f(button_x + x, button_y)
    glEnd()

def draw_exit_button():
    button_x = WINDOW_WIDTH - 10
    button_y = WINDOW_HEIGHT - 15
    button_width = 20
    button_height = 20
    glColor3f(1, 0, 0)  # Red color for the Exit button
    #rectangle for the Exit button
    glBegin(GL_POINTS)
    for x in range(button_x - button_width // 2, button_x + button_width // 2):
        for y in range(button_y - button_height // 2, button_y + button_height // 2):
            glVertex2f(x, y)
    glEnd()
    #X inside the Exit button
    glColor3f(0, 0, 0)
    glBegin(GL_POINTS)
    for i in range(-10, 11):
        glVertex2f(button_x + i, button_y + i)
        glVertex2f(button_x + i, button_y - i)
    glEnd()

def display():
    global game_over, game_won
    """Display callback for GLUT."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_stars()
    draw_orbit()
    draw_shooter()
    draw_button()
    draw_planets()
    draw_restart_button()
    draw_exit_button()
    update_comets()
    draw_comets()  # Draw comets
    check_shooter_sun_collision()
    check_shooter_comet_collision()
    check_shooter_planet_collision()
    if game_won:
        print("YOU WON")
        reset_game()
    elif game_over:
        reset_game()
        print("WOMP WOMP")
    glutSwapBuffers()

def mouseListener(button, state, x, y):
    global paused, pause_box
    button_x = 10
    button_y = WINDOW_HEIGHT - 10
    button_width = 20
    button_height = 20
    adjusted_y=800-y
    # Define the button's boundaries
    left_bound = button_x - button_width // 2
    right_bound = button_x + button_width // 2
    bottom_bound = button_y - button_height // 2
    top_bound = button_y + button_height // 2        
    exit_x = WINDOW_WIDTH - 10
    exit_y = WINDOW_HEIGHT - 15
    exit_size = 20
    if button==GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if pause_box['up1'][0] <= x <= pause_box['up2'][0] + pause_box['width']  and pause_box['down1'][1] <= 800-y <= pause_box['up2'][1] + pause_box['height']:
            if paused:
                print("Play clicked")
            else:
                print("Pause clicked")
            paused = not paused

        # Check if the click is inside the button
        elif left_bound <= x <= right_bound and bottom_bound <= adjusted_y <= top_bound:
            print("Restart button clicked!")
            reset_game()

        elif exit_x - exit_size <= x <= exit_x + exit_size and exit_y - exit_size <= adjusted_y <= exit_y + exit_size:
            glutLeaveMainLoop()
    # glutPostRedisplay()
        else:
            if not paused:
            # Spawn a comet at the mouse click position
                comet = Comet(x, 800 - y)
                comets.append(comet)
    # glutPostRedisplay()

def keyboardListener(key, x, y):
    global paused, planets, sun, shooter_x, shooter_y, game_over, game_won
    if not paused and not game_over and not game_won:  # Only allow movement if the game is not over or won
        if key == b'.':
            for i in planets:
                if i['speed'] < 4:
                    i['speed'] += 0.1
        if key == b',':
            for i in planets:
                if i['speed'] > 0.1:
                    i['speed'] -= 0.1
        if key == b'r':
            print("Resetting the game")
            reset_game()
        if key == b'a':  # Moving Left
            shooter_x = max(shooter_width // 2, shooter_x - 10)
        elif key == b'd':  # Moving right
            shooter_x = min(WINDOW_WIDTH - shooter_width // 2, shooter_x + 10)
        elif key == b'w':
            shooter_y = min(WINDOW_HEIGHT - shooter_height // 2, shooter_y + 10)
        elif key == b's':
            shooter_y = max(shooter_height // 2, shooter_y - 10)

def animate():
    if not paused and not game_over and not game_won:
        glutPostRedisplay()


def init():
    """Initialization for OpenGL."""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Interactive Solar System Game")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)

glutMainLoop()