import pygame
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horizontal Throw Simulation")

# Setting ground parameter (after HEIGHT -)
GROUND = HEIGHT - 20

# Colors
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLACK = (0, 0, 0)

# Set up the font
font = pygame.font.Font(None, 16)

class Body:
    G = 9.81

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius # in meters
        self.color = color
        self.mass = mass # in kg

        self.trajectory = []

    # Draw initial body
    def draw(self, win):
        x = self.x
        y = self.y
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    # Define horizontal velocity for the body; during free fall it's 0
    def horizontal_vel(self):
        return 50

    # Define vertical velocity for the body
    def vertical_vel(self):
        y_vel = 0
        y_vel += self.G * (pygame.time.get_ticks() / 1000)

        return y_vel

    def get_coordinates(self):
        x, y = (self.horizontal_vel() * (pygame.time.get_ticks() / 1000), self.vertical_vel() * (pygame.time.get_ticks() / 1000) * (1/2))
        return x, y

    def draw_body(self, x, y):
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)


# Create ground
def ground(y, color):
    rectPos = (0, y, WIDTH, HEIGHT)
    pygame.draw.rect(WIN, color, rectPos)

# Set background when switching frames
def reset_background():
    WIN.fill(BLACK)
    ground(GROUND, RED)

def main():
    run = True
    clock = pygame.time.Clock()

    ball = Body(20, 400, 5, WHITE, 1)



    while run:
        clock.tick(60)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        text_y = str(round(ball.vertical_vel(), 2))
        text_x = str(round(ball.horizontal_vel(), 2))

        # Render the ball
        if ball.get_coordinates()[1] <= GROUND - ball.radius:
            reset_background()
            ball.draw_body(*ball.get_coordinates())
        else:
            text_y = str(0)
            text_x = str(0)

        # Render the velocity
        textVer = font.render('Vertical velocity: ' + text_y + ' m / s', True, WHITE, BLACK)
        textHor = font.render('Horizontal velocity: ' + text_x + ' m / s', True, WHITE, BLACK)
        textVer_rect = textVer.get_rect()
        textHor_rect = textHor.get_rect()
        textVer_rect.center = (WIDTH - 100, 20)
        textHor_rect.center = (WIDTH - 100, 40)


        # Draw text
        WIN.blit(textVer, textVer_rect)
        WIN.blit(textHor, textHor_rect)

        pygame.display.update()

    pygame.quit()

main()
