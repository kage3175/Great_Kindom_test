import pygame, sys
from pygame.locals import *

LEFT_TOP = [124, 121]
SPACE = [54.8,55]

pygame.init()
screen=pygame.display.set_mode((800,720))
pygame.display.set_caption('Great Kingdom')

fps=10 #프레임이 높을 필요가 없기 때문에 프레임은 10으로 설정하였다. 낮은 사양의 컴퓨터에서는 이를 5 정도로 낮춰서 사용해도 문제가 없다.
fpsClock=pygame.time.Clock()

imgBoard = pygame.image.load('./img/board.png')
imgBlackStone = pygame.image.load('./img/black_stone.png')
imgWhiteStone = pygame.image.load('./img/white_stone.png')
lst_imgBlackStone = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN and event.button==1:
            position=pygame.mouse.get_pos()
            print(position)
    screen.fill((255,255,255))
    screen.blit(imgBoard, (52,49))
    '''screen.blit(imgBlackStone, imgBlackStone_RectObj)
    screen.blit(imgWhiteStone, imgWhiteStone_RectObj)'''
    '''for i in range(9):
        screen.blit(imgBlackStone, (round(LEFT_TOP[0]+SPACE[0]*(i-1)), round(LEFT_TOP[1]+SPACE[1]*(i-1))))'''
    pygame.display.flip()