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
imgNeutral = pygame.image.load('./img/neutral.png')
imgResignButton = pygame.image.load('./img/resign_button.png')
imgCountRequestButton = pygame.image.load('./img/counting_request_button.png')
fontObj = pygame.font.Font(None, 50)
text_my = 'balck'
textSurfaceObj1 = fontObj.render(text_my, True, (0,0,0))
textRectObj1=textSurfaceObj1.get_rect()
textRectObj1.center =(680,76)
lst_imgBlackStone = []
text_my = 'white'

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
    screen.blit(imgResignButton, (95, 600))
    screen.blit(imgCountRequestButton, (350, 600))
    screen.blit(textSurfaceObj1, textRectObj1)
    pygame.display.flip()