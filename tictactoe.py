import random
import os


def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    '''
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')

print('A bunch of garbage so we can garble up the screen...')
clear()

# Same effect, less characters...


def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    '''
    os.system('cls||echo -e \\\\033c')


def draw_board(xo_list: list):
    print(f' {xo_list[6]} | {xo_list[7]} | {xo_list[8]} ')
    print('---|---|---')
    print(f' {xo_list[3]} | {xo_list[4]} | {xo_list[5]} ')
    print('---|---|---')
    print(f' {xo_list[0]} | {xo_list[1]} | {xo_list[2]} \n\n')


def choice_figure():
    figure = input('Вы выбираете "X" или "O"?  ').upper()
    while figure not in 'X O 0 Х О'.split():  # Допускаем ввод с латинской и русской раскладки и ноль
        figure = input('Необходимо ввсети "Х" или "О"!\nПопробуйте еще раз:  ').upper()
    else:
        if figure == 'Х': # Проверка на русский ввод
            return 'X'
        elif figure == 'О':
            return 'O'
    return figure


def who_starts():
    figure = choice_figure()
    if random.choice(['X', 'O']) == figure:
        gamer = 'человек'
        if figure == 'X':
            order = [figure, 'O']
        else:
            order = [figure, 'X']
    else:
        gamer = 'компьютер'
        if figure == 'X':
            order = ['O', figure]
        else:
            order = ['X', figure]
    print('Начинает', end='')
    print('.', end='')
    print('.', end='')
    print('.', end='')
    print(gamer)
    return order, gamer


def is_win(li: list, mo)->bool:
    return (li[6] == mo and li[7] == mo and li[8] == mo or  # Верхний ряд
            li[3] == mo and li[4] == mo and li[5] == mo or  # Средний ряд
            li[0] == mo and li[1] == mo and li[2] == mo or  # Нижний ряд
            li[6] == mo and li[3] == mo and li[0] == mo or  # Левый столбец
            li[7] == mo and li[4] == mo and li[1] == mo or  # Средний столбец
            li[8] == mo and li[5] == mo and li[2] == mo or  # Правый столбец
            li[6] == mo and li[4] == mo and li[2] == mo or  # Диагональ
            li[8] == mo and li[4] == mo and li[0] == mo)  # Диагональ


def is_empty(li, mo):
    return li[mo] == ' '


def set_player_move(li):
    while True:
        mo = input('Ваш ход: ')
        if mo not in '1 2 3 4 5 6 7 8 9'.split():
            print('Введенное значение должно быть в диапазоне 1-9. \n попробуйте еще раз!')
            continue
        elif not is_empty(li, int(mo) - 1):
            print('Клетка занята! Такой ход не допустим! Попробуйте еще раз!')
            continue
        else:
            break
    return int(mo)-1


def change_player(pl):
    return 'X' if pl == 'O' else 'O'


def is_can_win(li: list, letter: str):
    for i in range(0, 9):
        copy = li.copy()  # Make copy of game field
        copy[i] = letter
        if is_win(copy, letter) and is_empty(li, i):
            return i
    letter_men = change_player(letter)
    for i in range(0, 9):  # Is can win men if he'll do next step
        copy = li.copy()
        copy[i] = letter_men
        if is_win(copy, letter_men) and is_empty(li, i):
            return i
    for i in random.choice('0 2 6 8'.split()):
        if li[int(i)] == ' ':
            return int(i)
    if li[4] == ' ':
        return 4
    for i in '1 3 5 7'.split():
        if li[int(i)] == ' ':
            return int(i)
    print(f'{letter} is not argument')
    return 0


def is_repeat():
    return input('\n\nХотите сыграть еше раз?\n\nВведите "Да" для продолжения или "Enter" для выхода.  ').lower() in 'yes ya y да д'.split()


if __name__ == "__main__":
    play = True
    chel = 'человек'
    comp = 'компьютер'
    while play:
        clear()
        board = [" " for x in range(9)]
        move, gamers = who_starts()
        player = move[0]
        draw_board(board)
        if gamers == comp:
            input('Для продолжения нажмите "Enter"')
        while True:
            if gamers == chel:
                num_move = set_player_move(board)
                board[num_move] = player
                clear()
            else:
                num_move = is_can_win(board, player)
                board[num_move] = player
                clear()
            draw_board(board)
            if is_win(board, player):
                print(f'Победил {gamers}')
                break
            if ' ' not in board:
                print('Ничья. Победила дружба!')
                break
            if gamers == chel:
                gamers = comp
            else:
                gamers = chel
            player = change_player(player)

        play = is_repeat()
