"""
Game that tests the ability to detect differences in colors
Christopher Calmes
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

large_text = pygame.font.Font("res/fonts/PressStart2P.ttf", 60)
small_text = pygame.font.Font("res/fonts/PressStart2P.ttf", 25)
score_text = pygame.font.Font("res/fonts/PressStart2P.ttf", 20)

gameDisplay = pygame.display.set_mode((_display_width, _display_height))
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


# get list position with 1
def different_color_pos(grid):
    for j in range(len(grid)):
        for k in range(len(grid[j])):
            if grid[j][k] == 1:
                return j, k


def draw_time(time_left, time_allowed, grid_color, background_color):
    time_left_height = (time_allowed - (time_allowed - time_left)) * 100
    reset_rect = (_display_width * (7.25 / 9), (_display_height - _margin), 90, -(_display_width - _display_height))
    time_left_rect = (_display_width * (7.25 / 9), (_display_height - _margin), 90, -time_left_height)

    # draw blank rectangle before redrawing time
    pygame.draw.rect(gameDisplay, background_color, reset_rect)
    pygame.display.update(reset_rect)

    pygame.draw.rect(gameDisplay, grid_color, time_left_rect)
    # gameDisplay.blit(time_left_surf, time_left_rect)
    pygame.display.update(time_left_rect)


def draw_board(rows, cols, difficulty, grid, score, num_clicked, grid_color, background_color):
    width = ((_game_width - rows * _margin) + _margin) / rows
    height = ((_game_width - rows * _margin) + _margin) / cols
    gameDisplay.fill(background_color)
    color = grid_color

    # score
    score_surf, score_rect = text_objects("Score: " + str((int(score))), score_text, _white)
    score_rect.center = ((_display_width * (7.5 / 9)), (_display_height * (1 / 7)))

    # clicked
    num_clicked_surf, num_clicked_rect = text_objects("Tiles: " + str(num_clicked), score_text, _white)
    num_clicked_rect.center = ((_display_width * (7.5 / 9)), (_display_height * (1 / 7)) + 30)

    gameDisplay.blit(score_surf, score_rect)
    gameDisplay.blit(num_clicked_surf, num_clicked_rect)

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

        text_surf, text_rect = text_objects("Speed Color", large_text, _black)
        text_rect.center = ((_display_width / 2), (_display_height / 2))
        gameDisplay.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("Press ENTER to continue", small_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) + 50))

        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(1)


def game_over(score):
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
                if event.key == pygame.K_s:
                    end_screen = False
                    high_scores()

        gameDisplay.fill(random_color())  # change color every second

        text_surf, text_rect = text_objects("Game Over :(", large_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) - 70))
        gameDisplay.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("You scored: " + str((int(score))), small_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2)))
        gameDisplay.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects("Press (ENTER) to continue", small_text, _black)
        text_rect.center = ((_display_width / 2), ((_display_height / 2) + 50))
        gameDisplay.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(1)

def game_loop():

    # initial values
    rows = 2  # start with 2x2 matrix
    cols = 2
    difficulty = 35  # value pixels change by
    maxrows = 10
    score = 0
    clicked = 0
    gamegrid = make_grid(rows, cols)  # initial game grid

    frames = 0  # frames since last loop
    time_allowed = 2.5
    seconds_left = time_allowed

    grid_color = random_color()
    background_color = random_color()
    draw_board(rows, cols, difficulty, gamegrid, score, clicked, grid_color, background_color)
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
                print(str(posgridx) + "," + str(posgridy))
                if (posgridx, posgridy) == different_color_pos(gamegrid):  # if correct square clicked
                    clicked_correct = True
                    # debug this
                else:
                    game_over(score)

        # only update the time left if it is greater than 0
        if seconds_left > 0:
            seconds_left = time_allowed - (frames / frame_rate)
        else:
            game_over(score)

        # continuously update the time on the screen
        draw_time(seconds_left, time_allowed, grid_color, background_color)
        pygame.display.update()

        # move the game forward if they get the right square
        if clicked_correct:
            if rows < maxrows:
                rows += 1
                cols += 1
            difficulty -= .5
            score += 10 + 10 * (seconds_left / time_allowed)
            clicked += 1
            frames = 0
            seconds_left = time_allowed


            # update game board
            gamegrid = make_grid(rows, cols)
            grid_color = random_color()
            background_color = random_color()
            draw_board(rows, cols, difficulty, gamegrid, score, clicked, grid_color, background_color)
            draw_time(seconds_left, time_allowed, grid_color, background_color)
            pygame.display.update()

            clicked_correct = False  # reset click

        frames += 1
        clock.tick(frame_rate)


game_intro()
