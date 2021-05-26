# coding: UTF-8
import copy
import pygame
import sys
from pygame.locals import *

FPS = 40
CELLWIDTH = 50
CELLHEIGHT = 50
PIECEWIDTH = 47
PIECEHEIGHT = 47
BOARDX = 35
BOARDY = 35
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# 退出程序
def terminate():
    pygame.quit()
    sys.exit()


# 初始化
pygame.init()
main_clock = pygame.time.Clock()
basic_font = pygame.font.SysFont("simsunnsimsun", 38)


# 加载图片
board_image = pygame.image.load("./图片/棋盘.png")
board_rect = board_image.get_rect()
black_image = pygame.image.load("./图片/黑子.png")
black_rect = black_image.get_rect()
white_image = pygame.image.load("./图片/白子.png")
white_rect = white_image.get_rect()

black_hint = pygame.image.load("./图片/黑子_提示.png")
black_hint_rect = black_hint.get_rect()
white_hint = pygame.image.load("./图片/白子_提示.png")
white_hint_rect = white_hint.get_rect()

# 设置窗口
window_surface = pygame.display.set_mode((board_rect.width, board_rect.height))
pygame.display.set_caption("黑白棋")


class Player:
    sign = ""
    hint = True

    def __init__(self, sign, hint=True):
        super().__init__()
        self.sign = sign
        self.hint = hint

    def action(self, board):
        # 先判断是否有子可落，如果无法落子，跳过回合
        if len(board.get_all_valid_moves(self.sign)) == 0:
            print("本回合%s无子可落，跳过回合" % (self.sign))
            return False

        # 提示可以落子的点
        if self.hint == True:
            board.draw_hints(self.sign)

        # 反复落子，直至位置有效
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == MOUSEBUTTONDOWN:
                    # 落子
                    if event.button == 1:
                        x_mouse, y_mouse = pygame.mouse.get_pos()
                        col = (x_mouse - BOARDX) // CELLWIDTH
                        row = (y_mouse - BOARDY) // CELLHEIGHT
                        if board.move_in_chess(self.sign, row, col) == True:
                            # 画图
                            board.draw_board_picture()
                            return True
                    # 开关提示
                    if event.button == 2:
                        if self.hint == True:
                            self.hint = False
                            board.draw_board_picture()
                        else:
                            self.hint = True
                            board.draw_hints(self.sign)

                    # 让AI帮你下
                    if event.button == 3:
                        self.ai(board)
                        return True

    def ai(self, board):
        valid_moves = board.get_all_valid_moves(self.sign)

        # 用ai代替人下棋
        best_move = [-1, -1]
        best_score = 0
        for x, y in valid_moves:
            if board.is_corner(x, y):
                board.move_in_chess(self.sign, x, y)
                board.draw_board_picture()
                return True

            score = len(board.valid_move(self.sign, x, y))
            if score > best_score:
                best_score = score
                best_move = [x, y]

        x, y = best_move
        board.move_in_chess(self.sign, x, y)
        board.draw_board_picture()


class Computer:
    sign = ""

    def __init__(self, sign):
        super().__init__()
        self.sign = sign

    def action(self, board):
        valid_moves = board.get_all_valid_moves(self.sign)
        if len(valid_moves) == 0:
            print("本回合%s无子可落，跳过回合" % (self.sign))
            return False

        # 鼠标点一下过后，再行动
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    best_move = [-1, -1]
                    best_score = 0
                    for x, y in valid_moves:
                        if board.is_corner(x, y):
                            board.move_in_chess(self.sign, x, y)
                            board.draw_board_picture()
                            return True

                        score = len(board.valid_move(self.sign, x, y))
                        if score > best_score:
                            best_score = score
                            best_move = [x, y]

                    x, y = best_move
                    board.move_in_chess(self.sign, x, y)
                    board.draw_board_picture()
                    return True


class Board:
    array = []
    size = 0

    def __init__(self, size, array=None):
        super().__init__()
        self.size = size
        if array != None:
            self.array = copy.deepcopy(array)
        else:
            for x in range(size):
                self.array.append([" "] * 8)
            self.reset_board()

    def draw_scores(self):
        scores = self.get_scores()

        output_str = "游戏结束 " + str(scores["X"]) + ":" + str(scores["O"]) + " "

        xscore = int(scores["X"])
        oscore = int(scores["O"])
        if xscore > oscore:
            output_str += "黑棋胜"
        elif xscore < oscore:
            output_str += "白棋胜"
        else:
            output_str += "平局"

        print(output_str)

        text = basic_font.render(output_str, True, WHITE, BLACK)
        textRect = text.get_rect()

        textRect.centerx = window_surface.get_rect().centerx
        textRect.centery = window_surface.get_rect().centery

        window_surface.blit(text, textRect)

        # 显示
        pygame.display.update()
        main_clock.tick(FPS)

    def draw_hints(self, sign):
        valid_moves = self.get_all_valid_moves(sign)
        # 直接画提示的子就可以，前面已经画好其它了
        for x, y in valid_moves:
            rect_location = pygame.Rect(
                BOARDX + y * CELLWIDTH + 2,
                BOARDY + x * CELLHEIGHT + 2,
                PIECEWIDTH,
                PIECEHEIGHT,
            )
            if sign == "X":
                window_surface.blit(black_hint, rect_location, black_hint_rect)
            elif sign == "O":
                window_surface.blit(white_hint, rect_location, white_hint_rect)

        # 更新画面
        pygame.display.update()
        main_clock.tick(FPS)

    def draw_board_picture(self):
        # 先画画板，再画棋子
        window_surface.blit(board_image, (0, 0), board_rect)

        for x in range(8):
            for y in range(8):
                rect_location = pygame.Rect(
                    BOARDX + y * CELLWIDTH + 2,
                    BOARDY + x * CELLHEIGHT + 2,
                    PIECEWIDTH,
                    PIECEHEIGHT,
                )
                if self.array[x][y] == "X":
                    window_surface.blit(black_image, rect_location, black_rect)
                elif self.array[x][y] == "O":
                    window_surface.blit(white_image, rect_location, white_rect)

        # 更新画面
        pygame.display.update()
        main_clock.tick(FPS)

    def reset_board(self):
        # 复原游戏面板
        size = self.size
        for x in range(size):
            for y in range(size):
                self.array[x][y] = " "
        mid = int(size / 2) - 1
        self.array[mid][mid] = "X"
        self.array[mid][mid + 1] = "O"
        self.array[mid + 1][mid] = "O"
        self.array[mid + 1][mid + 1] = "X"

    def is_corner(self, x, y):
        return x % 7 == 0 and y % 7 == 0

    def on_board(self, x, y):
        if x in range(self.size) and y in range(self.size):
            return True
        else:
            return False

    def valid_move(self, sign, x_start, y_start):
        # 是否可以移动
        # 如果可移动返回需要翻转的棋子位置，否则返回false

        if (
            self.on_board(x_start, y_start) == False
            or self.array[x_start][y_start] != " "
        ):
            return False

        o_sign = "X" if sign == "O" else "O"

        directions = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1],
        ]

        flip_sites = []
        has_answer = False
        for x_direc, y_direc in directions:
            x, y = x_start, y_start
            x += x_direc
            y += y_direc

            # 确保第一个棋子必须是对手的棋子，先取出一个棋子
            # 不能出界，不能为空，不能是自己棋子
            # 不在界内或者在界内但不是对手棋子，直接进入下一个循环
            if self.on_board(x, y) == False or self.array[x][y] != o_sign:
                continue

            while True:
                # 第一个已经判断，从第二个开始
                if self.array[x][y] == o_sign:
                    x += x_direc
                    y += y_direc
                if self.on_board(x, y) == False or self.array[x][y] == " ":
                    break
                if self.array[x][y] == sign:
                    has_answer = True
                    while True:
                        x -= x_direc
                        y -= y_direc
                        flip_sites.append([x, y])
                        if x == x_start and y == y_start:
                            break
                    break

        if has_answer:
            return flip_sites
        else:
            return False

    def get_all_valid_moves(self, sign):
        valid_moves = []
        for x in range(self.size):
            for y in range(self.size):
                moveable = self.valid_move(sign, x, y)
                if moveable != False:
                    valid_moves.append([x, y])
        return valid_moves

    def show_all_valid_moves(self, sign):
        copy_board = Board(self.size, self.array)
        for x, y in copy_board.get_all_valid_moves(sign):
            copy_board.array[x][y] = "."
        copy_board.draw_board()

    def get_scores(self):
        xscore = 0
        oscore = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.array[x][y] == "X":
                    xscore += 1
                if self.array[x][y] == "O":
                    oscore += 1
        return {"X": xscore, "O": oscore}

    def move_in_chess(self, sign, x, y):
        marks = self.valid_move(sign, x, y)
        if marks != False:
            for i, j in marks:
                self.array[i][j] = sign
            return True
        else:
            return False


class Game:

    player1 = Player("X")
    player2 = Player("O")

    def __init__(self, size=4):
        super().__init__()
        self.game_board = Board(size)

    def mouse_game_start(self):
        # 主循环
        self.game_board.draw_board_picture()
        while True:
            action1 = self.player1.action(self.game_board)
            action2 = self.player2.action(self.game_board)
            if action1 == False and action2 == False:
                print("游戏结束")
                self.game_board.draw_scores()
                break

        # 只有按退出才能结束
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()


def main():
    mouse_game = Game(8)
    mouse_game.mouse_game_start()


if __name__ == "__main__":
    main()