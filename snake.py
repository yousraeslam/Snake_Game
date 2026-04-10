import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 200, 0)
red = (255, 0, 0)
black = (0, 0, 0)

# Settings
snake_block = 10
snake_speed = 15

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

# Sounds (safe load)
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
    gameover_sound = pygame.mixer.Sound("gameover.wav")
except:
    eat_sound = None
    gameover_sound = None

time_counter = 0

def draw_snake(block, snake_list, dx, dy):
    global time_counter

    for i, x in enumerate(snake_list):

        if i != len(snake_list) - 1:
            pygame.draw.rect(screen, green, [x[0], x[1], block, block])

        else:
            # Head animation
            scale = 1 + 0.2 * math.sin(time_counter)
            size = int(block * scale)

            hx = x[0] - (size - block)//2
            hy = x[1] - (size - block)//2

            pygame.draw.rect(screen, dark_green, [hx, hy, size, size])

            # Direction-based eyes + tongue
            if dx > 0:  # right
                eyes = [(x[0]+6, x[1]+2), (x[0]+6, x[1]+6)]
                tongue_start = (x[0]+block, x[1]+block//2)
                tongue_dir = (1, 0)

            elif dx < 0:  # left
                eyes = [(x[0]+2, x[1]+2), (x[0]+2, x[1]+6)]
                tongue_start = (x[0], x[1]+block//2)
                tongue_dir = (-1, 0)

            elif dy > 0:  # down
                eyes = [(x[0]+2, x[1]+6), (x[0]+6, x[1]+6)]
                tongue_start = (x[0]+block//2, x[1]+block)
                tongue_dir = (0, 1)

            else:  # up
                eyes = [(x[0]+2, x[1]+2), (x[0]+6, x[1]+2)]
                tongue_start = (x[0]+block//2, x[1])
                tongue_dir = (0, -1)

            # Draw eyes
            for ex, ey in eyes:
                pygame.draw.rect(screen, white, [ex, ey, 2, 2])

            # Tongue animation
            flick = int(4 + 2 * math.sin(time_counter * 3))

            tx = tongue_start[0] + tongue_dir[0] * flick
            ty = tongue_start[1] + tongue_dir[1] * flick

            pygame.draw.line(screen, red, tongue_start, (tx, ty), 2)

            # Fork tongue
            if tongue_dir[0] != 0:
                pygame.draw.line(screen, red, (tx, ty), (tx, ty-2), 1)
                pygame.draw.line(screen, red, (tx, ty), (tx, ty+2), 1)
            else:
                pygame.draw.line(screen, red, (tx, ty), (tx-2, ty), 1)
                pygame.draw.line(screen, red, (tx, ty), (tx+2, ty), 1)

