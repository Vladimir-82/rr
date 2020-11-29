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
MERGE = 10
FPS = 60
fpsClock = pygame.time.Clock()


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
                    print('это не возможно')
                    pygame.quit()  # Роняем приложение

    def print_text(self, text, x, y, height=30, color=RED):
        font = pygame.font.Font('comic.ttf', height)
        text_surface = font.render(text, True, color)
        self.gameScreen.blit(text_surface, dest=(x, y))

    def start_screen(self):
        self.print_text('Choice figure:', 60, 40, color=BLUE)
        self.draw_circle_cell(1, 0)
        self.draw_cross_cell(1, 2)
        self.print_text('or', 130, 110, color=GREEN, height=50)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_cursor_in_cell(1, 0):
                    self.display_clear()
                    return 'O', False
                elif is_cursor_in_cell(1, 2):
                    self.display_clear()
                    return 'X', False
        return '', True

    def who_start_first(self):
        self.print_text('Who start first?', 40, 30, color=WHITE)
        self.draw_text_cell(1, 0, 'Man', x=25, y=130)
        self.draw_text_cell(1, 2, 'Comp', x=220)  # Проверить
        self.print_text('or', 130, 110, height=50, color=BLUE)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_cursor_in_cell(1, 0):
                    self.display_clear()
                    return 'man', False, False
                elif is_cursor_in_cell(1, 2):
                    self.display_clear()
                    return 'computer', False, False
        return '', True, True

    def end_game(self, win, li):
        self.print_text(f'Winn {win}', 50, 30)
        self.print_text('Do you want', 70, 80)
        self.print_text('play again?', 80, 110)
        self.draw_text_cell(2, 1, 'Yes', x=130, y=230)  # Проверить
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_cursor_in_cell(2, 1):
                    self.display_clear()
                    return True, True, False, True, True, [" " for x in range(9)]  # Сделать функцию "Поднять флаги"
        return False, False, True, False, False, li

    def winner(self, board, figure, gamer):
        if tictactoe.is_win(board, figure):
            self.display_clear()
            return gamer, True
        if ' ' not in board:
            self.display_clear()
            return 'friendship', True
        return '', False


if __name__ == '__main__':
    board = [" " for x in range(9)]
    # Flags
    figure = ''
    gamer = ''
    win = ''
    start_menu = True  # флаг выхода из стартового меню
    choice_figure = True  # флаг выхода из меню выбора фигур
    choice_who_start = True  # флаг выхода из меню выбора кто начинает
    main_game = True
    end_game_flag = False
    # Цикл игры
    runGame = True  # флаг выхода из цикла игры

    game = Field()

    while runGame:
        fpsClock.tick(FPS)
        # Отслеживание события: "закрыть окно"
        for event in pygame.event.get():

            if event.type == pygame.QUIT: runGame = False

            if start_menu:
                if choice_figure:
                    figure, choice_figure = game.start_screen()
                elif choice_who_start:
                    gamer, choice_who_start, start_menu = game.who_start_first()
                    if gamer == 'computer':
                        figure = tictactoe.change_player(figure)
                else:
                    continue
            elif main_game:
                game.draw_playing_field(board)

                if gamer == 'man':
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            x, y = pygame.mouse.get_pos()
                            row = (x - MERGE) // (MERGE + HEIGHT_CELL)
                            col = (y - MERGE) // (MERGE + WIDTH_CELL)
                            if tictactoe.is_empty(board, row + col + row * 2):
                                board[row + col + row * 2] = figure
                                win, end_game_flag = game.winner(board, figure, gamer)
                                figure = tictactoe.change_player(figure)
                                gamer = 'computer'
                elif gamer == 'computer':
                    num_move = tictactoe.is_can_win(board, figure)
                    board[num_move] = figure
                    win, end_game_flag = game.winner(board, figure, gamer)
                    figure = tictactoe.change_player(figure)
                    gamer = 'man'
            if end_game_flag:
                start_menu, main_game, end_game_flag, choice_figure, choice_who_start, board = game.end_game(win, board)
        pygame.display.update()

    # Выход из игры:
    pygame.quit()
