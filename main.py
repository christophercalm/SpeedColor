"""
Game that tests the ability to detect differences in colors
"""

import pygame
import random

pygame.init()

# dimensions
_display_width = 900
_game_width = _display_width - 300
_display_height = 600
_margin = 5

_black = (0, 0, 0)
_white = (255, 255, 255)

gameDisplay = pygame.display.set_mode((_display_width, _display_height))
pygame.display.set_caption("Speed Color")
clock = pygame.time.Clock()
frame_rate = 60

def random_color():
    r = lambda: random.randint(0, 255)
    return r(), r(), r()


def change_color(color, difficulty):
    newcolor = [0, 0, 0]

    for c in range(len(color)):
        if color[c] - difficulty < 0:
            newcolor[c] = color[c] + difficulty
        elif color[c] + difficulty > 255:
            newcolor[c] = color[c] - difficulty
        else:
            newcolor[c] = color[c] + difficulty
    return newcolor[0], newcolor[1], newcolor[2]


def random_square(rows):
    return random.randint(0, rows - 1)


# return grid square that is clicked
def get_rect(x, y, rows, cols):
    block_size = (_game_width - rows * _margin) / cols
    posX = x // (block_size + _margin)
    posY = y // (block_size + _margin)
    return (posX, posY)

# return 2-D list with one 1
def make_grid(rows: int, cols: int) -> list:
    newgrid = [[0 for x in range(rows)] for y in range(cols)]
    newgrid[random_square(rows)][random_square(rows)] = 1  # this square will be a different color
    print(newgrid)
    return newgrid


def text_objects(text, font, color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()

#get list position with 1
def different_color_pos(grid):
    for j in range(len(grid)):
        for k in range(len(grid[j])):
            if grid[j][k] == 1:
                return j, k

def draw_time(time_left, screen_color):

    print(time_left, screen_color)
    time_left_text = pygame.font.Font('freesansbold.ttf', 30)
    time_left_surf, time_left_rect = text_objects(str("{0:.2f}".format(time_left)), time_left_text, _white)
    time_left_rect.center = ((_display_width * (7 / 9)), (_display_height * (3 / 7)))

    # draw blank rectangle before redrawing time
    pygame.draw.rect(gameDisplay, screen_color, time_left_rect)
    gameDisplay.blit(time_left_surf, time_left_rect)


def draw_board(rows, cols, difficulty, grid, score, screen_color):
    width = ((_game_width - rows * _margin) + _margin) / rows
    height = ((_game_width - rows * _margin) + _margin) / cols
    gameDisplay.fill(random_color())
    color = screen_color

    score_text = pygame.font.Font('freesansbold.ttf', 30)
    score_surf, score_rect = text_objects("Score: " + str(score), score_text, _white)
    score_rect.center = ((_display_width * (7 / 9 )), (_display_height * (1 / 7)))
    gameDisplay.blit(score_surf, score_rect)


    for row in range(rows):
        for col in range(cols):
            rect = (row * (width + _margin), col * (width + _margin), width, height)
            if grid[row][col] == 0:  # normally draw
                pygame.draw.rect(gameDisplay, color, rect)
            elif grid[row][col] == 1:  # square that is different
                pygame.draw.rect(gameDisplay, (change_color(color, difficulty)), rect)


def high_scores():
    pass


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                    game_loop()
                if event.key == pygame.K_s:
                    intro = False
                    high_scores()

        gameDisplay.fill(random_color())  # change color every second

        large_text = pygame.font.Font('freesansbold.ttf', 60)
        small_text = pygame.font.Font('freesansbold.ttf', 25)

        text_surf, text_rect = text_objects("Speed Color", large_text, _black)
        text_rect.center = ((_display_width / 2), (_display_height / 2))
        gameDisplay.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("Press ENTER to continue", small_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) + 50))

        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(1)


def game_loop():
    # initial values
    rows = 2  # start with 2x2 matrix
    cols = 2
    difficulty = 30  # value pixels change by
    maxrows = 10
    score = 0
    gamegrid = make_grid(rows, cols)  # initial game grid

    frames = 0 # frames since last loop
    seconds_left = 3.0

    screen_color = random_color()
    draw_board(rows, cols, difficulty, gamegrid, score, screen_color)
    draw_time(seconds_left, screen_color)

    pygame.display.update()
    done = False
    clicked_correct = False

    while not done:

        for event in pygame.event.get():  # get all events
            if event.type == pygame.QUIT:
                done = True

            pressed = pygame.key.get_pressed()
            # change grid size if press return

            if event.type == pygame.MOUSEBUTTONDOWN:  # clicking on squares
                posx, posy = pygame.mouse.get_pos()
                posgridx, posgridy, = get_rect(posx, posy, rows, cols)
                print(str(posgridx) + "," + str(posgridy))
                if (posgridx, posgridy) == different_color_pos(gamegrid):  # if correct square clicked
                    clicked_correct = True
                    # debug this
                else:
                    pass
                    # pygame.quit()
                    # quit()
                    # game over code
        print(frames)

        seconds_left = 3.0 - (frames / frame_rate)
        print(seconds_left)
        draw_time(seconds_left, screen_color)

        if seconds_left <= 0:
            print("Game over")

        if clicked_correct:
            if rows < maxrows:
                rows += 1
                cols += 1
            difficulty -= .5
            score += 1
            frames = 0
            seconds_left = 3

            # update game board
            gamegrid = make_grid(rows, cols)
            print(seconds_left)
            screen_color = random_color()
            draw_board(rows, cols, difficulty, gamegrid, score, screen_color)
            draw_time(seconds_left, screen_color)
            pygame.display.update()

            clicked_correct = False  # reset click


        frames += 1
        clock.tick(frame_rate)

game_intro()
