import pygame
import math

pygame.init()

# Set window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horizontal Throw Simulation")

# Setting ground parameter
GROUND = 50
GROUND = HEIGHT - GROUND  # Y coordinates are inverted

# Color presets
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 153, 51)
BROWN = (89, 45, 0)

# Set up the font
font = pygame.font.Font(None, 16)


class Body:
    # Constants
    G = 9.81

    def __init__(self, x, y, radius, color, mass, x_vel, y_vel):
        # Initial coordinates
        self.x = x
        self.y = y

        # Color
        self.color = color

        # Physical properties
        self.radius = radius  # [m]
        self.mass = mass  # [kg]

        # Initial velocity
        self.x_vel = x_vel  # [m/s]
        self.y_vel = y_vel  # [m/s]

        self.trajectory = []

        self.time = 0

    # Draw initial body
    def draw(self):
        x = self.x
        y = self.y
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)

    # Define horizontal velocity for the body; during free fall it's 0
    def horizontal_vel(self):
        if self.is_on_ground():
            self.x_vel = 0
        return self.x_vel

    # Define vertical velocity for the body
    def vertical_vel(self):
        if self.is_on_ground():
            self.y_vel = 0
        else:
            self.y_vel += self.G * (1 / 60)

    def get_coordinates(self):
        return self.x, self.y

    def set_new_coords(self, x, y):
        self.x, self.y = (x + (1 / 60) * self.horizontal_vel(),
                          y + (1 / 60) * self.y_vel + (self.G * pow(1 / 60, 2)) / 2)
        self.vertical_vel()

    def draw_body(self, x, y):
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)

    def draw_trajectory(self):
        self.trajectory.append(self.get_coordinates())
        for i in self.trajectory:
            pygame.draw.circle(WIN, WHITE, i, 1)

    def is_on_ground(self):
        return not self.get_coordinates()[1] <= GROUND - self.radius

    def count_time(self):
        self.time += 1 / 60


# Create ground
def ground(y, color):
    rect_pos = (0, y, WIDTH, HEIGHT)
    pygame.draw.rect(WIN, color, rect_pos)


# Set background when switching frames
def reset_background():
    WIN.fill(BLACK)
    ground(GROUND, BROWN)


def main():
    run = True
    clock = pygame.time.Clock()

    ball = Body(20, 50, 5, GREEN, 1, 40, 0)
    ball_second = Body(10, 350, 8, RED, 6, 80, 0)

    while run:
        clock.tick(60)
        ball.count_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not ball.is_on_ground() or not ball_second.is_on_ground():
            reset_background()

            ball_second.set_new_coords(*ball_second.get_coordinates())
            ball_second.draw_trajectory()
            ball_second.draw_body(*ball_second.get_coordinates())

            ball.set_new_coords(*ball.get_coordinates())
            ball.draw_trajectory()
            ball.draw_body(*ball.get_coordinates())

        # Render stats
        stats = ['[Green] Horizontal velocity: ' + str(round(ball.x_vel, 2)) + ' m / s',
                 '[Green] Vertical velocity: ' + str(round(ball.y_vel, 2)) + ' m / s',
                 '[Green] Instantaneous velocity: ' +
                 str(round(math.sqrt(pow(ball.x_vel, 2) + pow(ball.y_vel, 2)), 2)) + ' m / s',
                 '[Red] Horizontal velocity: ' + str(round(ball_second.x_vel, 2)) + ' m / s',
                 '[Red] Vertical velocity: ' + str(round(ball_second.y_vel, 2)) + ' m / s',
                 '[Red] Instantaneous velocity: ' +
                 str(round(math.sqrt(pow(ball_second.x_vel, 2) + pow(ball_second.y_vel, 2)), 2)) + ' m / s',
                 'Time elapsed: ' + str(round(ball.time, 2)) + ' s']

        texts = []

        for stat in stats:
            text = font.render(stat, True, WHITE, None)

            text_rect = text.get_rect()

            texts.append((text, text_rect))

        y_text = 20

        # Loop through the texts list
        for text, text_rect in texts:
            text_rect.centerx = WIDTH - 120
            text_rect.top = y_text
            WIN.blit(text, text_rect)
            y_text += 20

        pygame.display.update()

    pygame.quit()


main()
