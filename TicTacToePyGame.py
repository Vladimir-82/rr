import pygame
import tictactoe

# Color
WHITE = (255, 255, 255)
BLUE = (102, 153, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Field
HEIGHT_WINDOW = 310
WIDTH_WINDOW = 310
# Cell
HEIGHT_CELL = 90
WIDTH_CELL = 90
MERGE = 10  # Merge between cells


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = MERGE + self.col * (MERGE + HEIGHT_CELL)
        self.y = MERGE + self.row * (MERGE + WIDTH_CELL)


def is_cursor_in_cell(row, col):
    x, y = pygame.mouse.get_pos()
    cell_x = MERGE + col * (MERGE + HEIGHT_CELL)
    cell_y = MERGE + row * (MERGE + WIDTH_CELL)
    return cell_x < x < (cell_x + WIDTH_CELL) and cell_y < y < (cell_y + HEIGHT_CELL)


class Field:
    def __init__(self):
        pygame.init()
        self.gameScreen = pygame.display.set_mode([HEIGHT_WINDOW, WIDTH_WINDOW])  # Начальное положение окна
        pygame.display.set_caption("Tic Tac Toe")
        self.display_clear()

    def display_clear(self):
        self.gameScreen.fill(BLACK)
        pygame.display.flip()

    def draw_cell(self, x, y, color):
        pygame.draw.rect(self.gameScreen, color,
                         (x, y, WIDTH_CELL, HEIGHT_CELL))

    def draw_free_cell(self, row, col):
        cell = Cell(row, col)
        self.draw_cell(cell.x, cell.y, WHITE)

    def draw_cross_cell(self, row, col):
        cell = Cell(row, col)
        self.draw_cell(cell.x, cell.y, YELLOW)
        pygame.draw.line(self.gameScreen, BLACK, [cell.x + 10, cell.y + 10],
                         [cell.x + WIDTH_CELL - 10, cell.y + WIDTH_CELL - 10], 10)
        pygame.draw.line(self.gameScreen, BLACK, [cell.x + WIDTH_CELL - 10, cell.y + 10],
                         [cell.x + 10, cell.y + WIDTH_CELL - 10], 10)

    def draw_circle_cell(self, row, col):
        cell = Cell(row, col)
        self.draw_cell(cell.x, cell.y, RED)
        pygame.draw.circle(self.gameScreen, BLACK,
                           (cell.x + WIDTH_CELL / 2, cell.y + WIDTH_CELL / 2), WIDTH_CELL / 2 - 5, 7)

    def draw_text_cell(self, row, col, text='Text', x=0, y=0):
        cell = Cell(row, col)
        self.draw_cell(cell.x, cell.y, GREEN)
        # if x and y not entered, than parameters depends coordinate cell
        self.print_text(text, cell.x + 5 if x == 0 else x, cell.y + 20 if y == 0 else y)

    def draw_playing_field(self, field):
        for i in range(3):
            for j in range(3):
                if field[i + j + i * 2] == ' ':
                    self.draw_free_cell(j, i)
                elif field[i + j + i * 2] == 'X':
                    self.draw_cross_cell(j, i)
                elif field[i + j + i * 2] == 'O':
                    self.draw_circle_cell(j, i)
                else:
                    print(f'Field {field} is not draw')
                    pygame.quit()  # Exception

    def print_text(self, text, x, y, height=30, color=RED):
        font = pygame.font.Font('comic.ttf', height)
        text_surface = font.render(text, True, color)
        self.gameScreen.blit(text_surface, dest=(x, y))

    # Menu of choice game figure
    def choice_figure_draw(self):
        self.print_text('Choice figure:', 60, 40, color=BLUE)
        self.draw_circle_cell(1, 0)
        self.draw_cross_cell(1, 2)
        self.print_text('or', 130, 110, color=GREEN, height=50)

    # Event of choice game figure
    def choice_figure(self):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_cursor_in_cell(1, 0):
                    self.display_clear()
                    pygame.display.update()
                    return 'O', False, True  # figure, figure_flag, who_start_flag
                elif is_cursor_in_cell(1, 2):
                    self.display_clear()
                    pygame.display.update()
                    return 'X', False, True
        return '', True, False

    # Menu of choice who start
    def who_start_first_draw(self):
        self.print_text('Who start first?', 40, 30, color=WHITE)
        self.draw_text_cell(1, 0, 'Man', x=25, y=130)
        self.draw_text_cell(1, 2, 'Comp', x=220)
        self.print_text('or', 130, 110, height=50, color=BLUE)

    # Event of choice who start
    def who_start_first(self):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_cursor_in_cell(1, 0):
                    self.display_clear()
                    return 'human', False, True  # gamer, who_start_flag, main_game_flag
                elif is_cursor_in_cell(1, 2):
                    self.display_clear()
                    return 'computer', False, True
        return '', True, False

    # Menu of return game
    def end_game_draw(self, win):
        self.print_text(f'Winn {win}', 50, 30)
        self.print_text('Do you want', 70, 80)
        self.print_text('play again?', 80, 110)
        self.draw_text_cell(2, 1, 'Yes', x=130, y=230)

    # Event of return game
    def end_game(self, li):  # li - list of game field
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_cursor_in_cell(2, 1):
                    self.display_clear()
                    # end_game_flag, main_game_flag, new clear list of game field
                    return False, True, [" " for x in range(9)]
        return True, False, li

    # Checking who is the winner
    def winner(self, board, figure, gamer):
        if tictactoe.is_win(board, figure):
            self.display_clear()
            return gamer, False, True  # winner, main_game_flag, figure_flag
        if ' ' not in board:
            self.display_clear()
            return 'friendship', False, True
        return '', True, False


def change_player(player):
    player = 'human' if player == 'computer' else 'computer'
    return player


if __name__ == '__main__':
    # Flags
    figure = ''
    gamer = ''
    win = ''
    figure_flag = True
    who_start_flag = False
    main_game_flag = False
    end_game_flag = False
    run_game_flag = True

    board = [" " for x in range(9)]  # Create game field
    game = Field()  # Create object of game field

    while run_game_flag:
        # Draws
        if figure_flag:
            game.choice_figure_draw()
        if who_start_flag:
            game.who_start_first_draw()
        if main_game_flag:
            game.draw_playing_field(board)
            if gamer == 'computer':
                num_move = tictactoe.is_can_win(board, figure)
                board[num_move] = figure
                win, main_game_flag, end_game_flag = game.winner(board, figure, gamer)
                figure = tictactoe.change_player(figure)
                gamer = 'human'
        if end_game_flag:
            game.end_game_draw(win)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game_flag = False
            if figure_flag:
                figure, figure_flag, who_start_flag = game.choice_figure()
                continue
            if who_start_flag:
                gamer, who_start_flag, main_game_flag = game.who_start_first()
                if gamer == 'computer':
                    figure = tictactoe.change_player(figure)
                continue
            if main_game_flag:
                if gamer == 'human':
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            x, y = pygame.mouse.get_pos()
                            row = (x - MERGE) // (MERGE + HEIGHT_CELL)
                            col = (y - MERGE) // (MERGE + WIDTH_CELL)
                            if tictactoe.is_empty(board, row + col + row * 2):
                                board[row + col + row * 2] = figure
                                win, main_game_flag, end_game_flag = game.winner(board, figure, gamer)
                                figure = tictactoe.change_player(figure)
                                gamer = 'computer'
            if end_game_flag:
                end_game_flag, figure_flag, board = game.end_game(board)
        pygame.display.update()
    pygame.quit()
