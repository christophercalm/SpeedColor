"""
Game that tests the ability to detect differences in colors
Christopher Calmes
"""

import pygame
import random
import pickle

pygame.init()

# dimensions
_display_width = 900
_game_width = _display_width - 300
_display_height = 600
_margin = 5

# colors
_black = (0, 0, 0)
_white = (255, 255, 255)

# initialize fonts
large_text = pygame.font.Font("res/fonts/PressStart2P.ttf", 60)
small_text = pygame.font.Font("res/fonts/PressStart2P.ttf", 25)
score_text = pygame.font.Font("res/fonts/PressStart2P.ttf", 20)

# pygame init things
game_display = pygame.display.set_mode((_display_width, _display_height))
pygame.display.set_caption("Speed Color")
clock = pygame.time.Clock()
frame_rate = 60


def random_color():
    """
    Makes a random color
    :return: Color tuple
    """
    r = lambda: random.randint(0, 255)
    return r(), r(), r()


def change_color(color, difficulty):
    """
    Makes a color that one shade lighter than the inputted color
    :param color: input color
    :param difficulty: the value that the color calculation depends on
    :return: Returns a tuple that can be used as a color
    """
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
    """
    Returns random square
    :param rows:
    :return: integer
    """
    return random.randint(0, rows - 1)


def get_rect(x, y, rows, cols):
    """
    Handles mouse clicking

    :param x: mouse x position
    :param y: mouse y position
    :param rows: rows in matrix
    :param cols: columns in game matrix
    :return: coordinates of the clicked game square
    """
    block_size = (_game_width - rows * _margin) / cols
    posX = x // (block_size + _margin)
    posY = y // (block_size + _margin)
    return posX, posY


# return 2-D list with one 1
def make_grid(rows: int, cols: int) -> list:
    newgrid = [[0 for x in range(rows)] for y in range(cols)]
    newgrid[random_square(rows)][random_square(rows)] = 1  # this square will be a different color
    return newgrid


# return text object to render
def text_objects(text, font, color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()


# get list position with 1
def different_color_pos(grid):
    for j in range(len(grid)):
        for k in range(len(grid[j])):
            if grid[j][k] == 1:
                return j, k


# return level to base grid on
def get_level(num_clicked):
    if num_clicked <= 5:
        return 1
    elif num_clicked > 5 and num_clicked < 8:
        return 2
    elif 8 <= num_clicked < 11:
        return 3
    elif 11 <= num_clicked < 14:
        return 4
    elif 14 <= num_clicked < 17:
        return 5
    elif 17 <= num_clicked < 20:
        return 6
    elif 20 <= num_clicked < 30:
        return 7
    elif 30 <= num_clicked < 40:
        return 8
    elif num_clicked >= 40:
        return 9


# draws time left as a rectangle
def draw_time(time_left, time_allowed, grid_color, background_color):
    time_left_height = (time_allowed - (time_allowed - time_left)) * 100
    reset_rect = (_display_width * (7 / 9), (_display_height - _margin), 110, -(_display_width - _display_height))
    time_left_rect = (_display_width * (7 / 9), (_display_height - _margin), 110, -time_left_height)

    # draw blank rectangle before redrawing time
    pygame.draw.rect(game_display, background_color, reset_rect)
    pygame.display.update(reset_rect)

    pygame.draw.rect(game_display, grid_color, time_left_rect)
    pygame.display.update(time_left_rect)


# renders board with high score, score, and numbre clicked
def draw_board(rows, cols, difficulty, grid, score, high_score, num_clicked, grid_color, background_color):
    width = ((_game_width - rows * _margin) + _margin) / rows
    height = ((_game_width - rows * _margin) + _margin) / cols
    game_display.fill(background_color)
    color = grid_color

    # high score
    high_score_surf, high_score_rect = text_objects("Top: " + str((int(high_score))), small_text, _white)
    high_score_rect.center = ((_display_width * (7.5 / 9)), (_display_height * (1 / 7)))

    # score
    score_surf, score_rect = text_objects("Score: " + str((int(score))), score_text, _white)
    score_rect.center = ((_display_width * (7.5 / 9)), (_display_height * (1 / 7)) + 60)

    # clicked
    num_clicked_surf, num_clicked_rect = text_objects("Tiles: " + str(num_clicked), score_text, _white)
    num_clicked_rect.center = ((_display_width * (7.5 / 9)), (_display_height * (1 / 7)) + 90)

    game_display.blit(high_score_surf, high_score_rect)
    game_display.blit(score_surf, score_rect)
    game_display.blit(num_clicked_surf, num_clicked_rect)

    for row in range(rows):
        for col in range(cols):
            rect = (row * (width + _margin), col * (width + _margin), width, height)
            if grid[row][col] == 0:  # normally draw
                pygame.draw.rect(game_display, color, rect)
            elif grid[row][col] == 1:  # square that is different
                pygame.draw.rect(game_display, (change_color(color, difficulty)), rect)


# displays intro
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

        game_display.fill(random_color())  # change color every second

        text_surf, text_rect = text_objects("Speed Color", large_text, _black)
        text_rect.center = ((_display_width / 2), (_display_height / 2))
        game_display.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("Press ENTER to continue", small_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) + 50))

        game_display.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(1)


# function that handles rendering game over screen and saving high score
def game_over(game_over_score, game_over_high_score):
    if game_over_score > game_over_high_score:
        game_over_high_score = game_over_score

    # save high scores
    with open('dat/score.dat', 'wb') as scores:
        pickle.dump(game_over_high_score, scores)

    end_screen = True

    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    end_screen = False
                    game_loop()

        game_display.fill(random_color())  # change color every second

        text_surf, text_rect = text_objects("Game Over :(", large_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) - 70))
        game_display.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("You scored: " + str((int(game_over_score))), small_text, _black)
        text_rect.center = ((_display_width / 2), (_display_height / 2))
        game_display.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("Press (ENTER) to continue", small_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) + 50))
        game_display.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(1)


# main loop
def game_loop():
    # initial values
    rows = 2  # start with 2x2 matrix
    cols = 2
    difficulty = 35  # value pixels change by
    score = 0
    clicked = 0
    level = 0
    game_grid = make_grid(rows, cols)  # initial game grid

    try:
        with open('dat/score.dat', 'rb') as scores:
            high_score = pickle.load(scores)
    except FileNotFoundError:
        high_score = 0

    frames = 0  # frames since last loop
    time_allowed = 2.75
    seconds_left = time_allowed

    grid_color = random_color()
    background_color = random_color()
    draw_board(rows, cols, difficulty, game_grid, score, high_score, clicked, grid_color, background_color)
    draw_time(seconds_left, time_allowed, grid_color, background_color)

    pygame.display.update()
    done = False
    clicked_correct = False

    while not done:

        for event in pygame.event.get():  # get all events
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()

            # change grid size if press return
            if event.type == pygame.MOUSEBUTTONDOWN:  # clicking on squares
                posx, posy = pygame.mouse.get_pos()
                posgridx, posgridy, = get_rect(posx, posy, rows, cols)
                if (posgridx, posgridy) == different_color_pos(game_grid):  # if correct square clicked
                    clicked_correct = True
                else:
                    game_over(score, high_score)

        # only update the time left if it is greater than 0
        if seconds_left > 0:
            seconds_left = time_allowed - (frames / frame_rate)
        else:
            game_over(score, high_score)

        # continuously update the time on the screen
        draw_time(seconds_left, time_allowed, grid_color, background_color)
        pygame.display.update()

        # move the game forward if they get the right square
        if clicked_correct:
            cur_level = level
            level = get_level(clicked)
            if level > cur_level:
                cols += 1
                rows += 1
                difficulty -= 2.5
            # increase difficulty every click after max level
            if level > 9:
                difficulty -= .5
            score += int(20 + 20 * (seconds_left / time_allowed))
            clicked += 1
            frames = 0
            seconds_left = time_allowed

            # update game board
            game_grid = make_grid(rows, cols)
            grid_color = random_color()
            background_color = random_color()
            draw_board(rows, cols, difficulty, game_grid, score, high_score, clicked, grid_color, background_color)
            draw_time(seconds_left, time_allowed, grid_color, background_color)
            pygame.display.update()

            clicked_correct = False  # reset click

        frames += 1
        clock.tick(frame_rate)


game_intro()
