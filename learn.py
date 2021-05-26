import pygame, sys


def terminate():
    pygame.quit()
    sys.exit()


# 加载图片
board_image = pygame.image.load("board.png")
board_rect = board_image.get_rect()

# 设置窗口
window = pygame.display.set_mode((board_rect.width, board_rect.height))
pygame.display.set_caption("黑白棋")

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    window.blit(board_image, (0, 0), board_rect)
    pygame.display.update()