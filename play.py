import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (159, 163, 168)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CAR_COLOR = (181, 230, 29)
TEXT_COLOR = (250, 105, 10)


pygame.init()


class Car:
    def __init__(self, x=0, y=0, dx=4, dy=0, width=30, height=30, color=RED):
        self.image = ""
        self.x = x
        self.y = y
        self. dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.color = color

    def load_image(self, img):
        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey(BLACK)

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def draw_rect(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 0)

    def check_out_of_screen(self):
        if self.x+self.width > 400 or self.x < 0:
            self.x -= self.dx


def check_collision(player_x, player_y, player_width, player_height, car_x, car_y, car_width, car_height):
    if (player_x+player_width > car_x) and (player_x < car_x+car_width) and (player_y < car_y+car_height) and (player_y+player_height > car_y):
        return True
    else:
        return False


# Set the width and height of the screen [width, height]
size = (400, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Ride the Road")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create a player car object
player = Car(175, 475, 0, 0, 70, 131, RED)
player.load_image("player.png")

collision = True

# Store the score
score = 0

# Load the fonts
font_40 = pygame.font.SysFont("Arial", 40, True, False)
font_30 = pygame.font.SysFont("Arial", 30, True, False)
text_title = font_40.render("Ride the Road", True, TEXT_COLOR)
text_ins = font_30.render("Click to Play!", True, TEXT_COLOR)


def draw_main_menu():
    screen.blit(text_title, [size[0] / 2 - 106, size[1] / 2 - 100])
    score_text = font_40.render("Score: " + str(score), True, TEXT_COLOR)
    screen.blit(score_text, [size[0] / 2 - 70, size[1] / 2 - 30])
    screen.blit(text_ins, [size[0] / 2 - 85, size[1] / 2 + 40])
    pygame.display.flip()


# Setup the enemy cars
cars = []
car_count = 2
for i in range(car_count):
    x = random.randrange(0, 340)
    car = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10), 60, 60, CAR_COLOR)
    cars.append(car)


# Setup the stripes.
stripes = []
stripe_count = 20
stripe_x = 185
stripe_y = -10
stripe_width = 20
stripe_height = 80
space = 20
for i in range(stripe_count):
    stripes.append([190, stripe_y])
    stripe_y += stripe_height + space

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Reset everything when the user starts the game.
        if collision and event.type == pygame.MOUSEBUTTONDOWN:
            collision = False
            for i in range(car_count):
                cars[i].y = random.randrange(-150, -50)
                cars[i].x = random.randrange(0, 350)
            player.x = 175
            player.dx = 0
            score = 0
            pygame.mouse.set_visible(False)

        if not collision:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 4
                elif event.key == pygame.K_LEFT:
                    player.dx = -4

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.dx = 0
                elif event.key == pygame.K_RIGHT:
                    player.dx = 0

    # --- Game logic should go here

    # --- Screen-clearing code goes here
    screen.fill(GRAY)

    # --- Drawing code should go here
    if not collision:
        # Draw the stripes
        for i in range(stripe_count):
            pygame.draw.rect(screen, WHITE, [stripes[i][0], stripes[i][1], stripe_width, stripe_height])
        # Move the stripes
        for i in range(stripe_count):
            stripes[i][1] += 3
            if stripes[i][1] > size[1]:
                stripes[i][1] = -40 - stripe_height

        player.draw_image()
        player.move_x()
        player.check_out_of_screen()

        # Check if the enemy cars move out of the screen.
        for i in range(car_count):
            cars[i].draw_rect()
            cars[i].y += cars[i].dy
            if cars[i].y > size[1]:
                score += 10
                cars[i].y = random.randrange(-150, -50)
                cars[i].x = random.randrange(0, 340)
                cars[i].dy = random.randint(4, 9)

        # Check the collision of the player with the car
        for i in range(car_count):
            if check_collision(player.x, player.y, player.width, player.height, cars[i].x, cars[i].y, cars[i].width, cars[i].height):
                collision = True
                pygame.mouse.set_visible(True)
                break

        # Draw the score.
        txt_score = font_30.render("Score: "+str(score), True, WHITE)
        screen.blit(txt_score, [15, 15])

        pygame.display.flip()
    else:
        draw_main_menu()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
