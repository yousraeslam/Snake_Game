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

def show_score(score):
    value = font.render("Score: " + str(score), True, white)
    screen.blit(value, [10, 10])

def game():
    global time_counter

    while True:
        game_close = False

        x = width / 2
        y = height / 2

        dx = 0
        dy = 0

        snake_list = []
        length = 1

        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10
        foody = round(random.randrange(0, height - snake_block) / 10.0) * 10

        while not game_close:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -snake_block
                        dy = 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = snake_block
                        dy = 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dy = -snake_block
                        dx = 0
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dy = snake_block
                        dx = 0

            x += dx
            y += dy

            if x >= width or x < 0 or y >= height or y < 0:
                if gameover_sound:
                    gameover_sound.play()
                break

            screen.fill(black)

            pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

            snake_head = [x, y]
            snake_list.append(snake_head)

            if len(snake_list) > length:
                del snake_list[0]

            for block in snake_list[:-1]:
                if block == snake_head:
                    if gameover_sound:
                        gameover_sound.play()
                    game_close = True

            draw_snake(snake_block, snake_list, dx, dy)
            show_score(length - 1)

            pygame.display.update()

            if x == foodx and y == foody:
                if eat_sound:
                    eat_sound.play()
                foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10
                foody = round(random.randrange(0, height - snake_block) / 10.0) * 10
                length += 1

            time_counter += 0.2
            clock.tick(snake_speed)

        screen.fill(black)
        msg = font.render("Game Over! Press C to play again or Q to quit", True, red)
        screen.blit(msg, [40, height / 2])
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        waiting = False

game()



# py snake.py