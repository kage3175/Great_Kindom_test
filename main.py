import pygame
from pygame.locals import *
from socket import *
import threading
import time
from tkinter import*
import random
import sys

# 실제 플레이에 사용되는 보드는 9x9
# 1은 흑돌, 2는 백돌, 3은 중립돌

### Great Kingdom 관련 전역변수들
BOARD_SIZE = 9
THECROSS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BLANK = 0
BLACKSTONE = 1
WHITESTONE = 2
NEUTRAL = 3
LEFT_TOP = [124, 121]
GAP = [54.8,55]
LEFT_GRID = [93, 89]
GAP_GRID = [55.625, 55.75]
OMAKE = 3

### Pygame 관련 전역변수들
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
POS_CATCH = 20
port_num = 0
fpsClock = pygame.time.Clock()

clusters_black = []
clusters_white = []
clusters_neutral = []
clusters_black_house = []
clusters_white_house = []
clusters_blank = []
board = [[0 for i in range(BOARD_SIZE+2)] for j in range(BOARD_SIZE+2)]
mark_cluster = [[True for i in range(BOARD_SIZE+3)] for j in range(BOARD_SIZE+2)]

is_host = True
running = True

serverSock = socket(AF_INET, SOCK_STREAM)
clientSock = socket(AF_INET, SOCK_STREAM)
connectionSock = None
content = None
accept_count = True

imgBoard = pygame.image.load('./img/board.png')
imgBlackStone = pygame.image.load('./img/black_stone.png')
imgWhiteStone = pygame.image.load('./img/white_stone.png')
imgNeutral = pygame.image.load('./img/neutral.png')
imgResignButton = pygame.image.load('./img/resign_button.png')
imgCountRequestButton = pygame.image.load('./img/counting_request_button.png')

def clear_board():
    global board
    for i in range(BOARD_SIZE+2):
        for j in range(BOARD_SIZE+2):
            board[i][j] = 0
    board[int(BOARD_SIZE/2)+1][int(BOARD_SIZE/2)+1] = 3
    for i in range(BOARD_SIZE+2):
        board[0][i]=3
        board[BOARD_SIZE+1][i]=3
        board[i][0]=3
        board[i][BOARD_SIZE+1]=3

def opponent_leaved():
    window = Tk()
    window.title('Opponent Leaved')
    frm=Frame(window, width=298, height=125, bg='gray79')
    frm.pack()
    text1 = Label(window, text = "Opponent leaved the game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text1.place(x = 15, y = 10)
    text2 = Label(window, text = "Press Confirm Button to quit the game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text2.place(x = 15, y = 40)
    select_OFF = Button(window, text = "    Confirm    ", bg = 'snow', height = 1, width = 20, font=('Helvetica', 14), command = quit)
    select_OFF.place(x = 30, y = 76)
    window.mainloop()

def you_win(win_code):
    window = Tk()
    window.title('You win!')
    frm=Frame(window, width=298, height=126, bg='gray79')
    frm.pack()
    if win_code == 'c':
        text1 = Label(window, text = "You won by capturing Opponent's stone!",bg='gray79', fg='black', font=('Helvetica', 12))
        text1.place(x = 15, y = 10)
    elif win_code == 'r':
        text1 = Label(window, text = "Opponent resigned.",bg='gray79', fg='black', font=('Helvetica', 12))
        text1.place(x = 15, y = 10)
    text2 = Label(window, text = "Press Confirm Button to quit the game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text2.place(x = 15, y = 40)
    select_OFF = Button(window, text = "    Confirm    ", bg = 'snow', height = 1, width = 20, font=('Helvetica', 14), command = quit)
    select_OFF.place(x = 30, y = 76)
    window.mainloop()

def receive(sock):
    global content
    while True:
        recvData = sock.recv(1024)
        line = recvData.decode('utf-8')
        words = list(line.split())
        if words[0] == 'q' or words[0] == 'Q':
            msg = 'Q 1'
            sock.send(msg.encode('utf-8'))
            content = 'Q 1'
            return
        elif words[0] == 's':
            msg = 's'
            sock.send(msg.encode('utf-8'))
            return
        else:
            content = line

def opponent_win(lose_code):
    window = Tk()
    window.title('You lose')
    frm=Frame(window, width=298, height=126, bg='gray79')
    frm.pack()
    if lose_code == 'r':
        text1 = Label(window, text = "You Resigned.",bg='gray79', fg='black', font=('Helvetica', 12))
        text1.place(x = 15, y = 10)
    elif lose_code == 'c':
        text1 = Label(window, text = "Opponent captured your stone.",bg='gray79', fg='black', font=('Helvetica', 12))
        text1.place(x = 15, y = 10)
    text2 = Label(window, text = "Press Confirm Button to quit the game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text2.place(x = 15, y = 40)
    select_OFF = Button(window, text = "    Confirm    ", bg = 'snow', height = 1, width = 20, font=('Helvetica', 14), command = quit)
    select_OFF.place(x = 30, y = 76)
    window.mainloop()

def request_counting(): #작업해야하는거
    global accept_count
    accept_count = False
    window = Tk()
    window.title('Opponent\'s request for counting')
    frm=Frame(window, width=345, height=130, bg='gray50')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    text_notice = Label(window, text='Opponent requested for the counting', bg='gray50', fg='white', font=('Helvetica', 14))
    text_notice.place(x= 12, y= 10)
    select_host = Button(window, text = "    Accept    ", height = 2, width = 13, font=('Helvetica', 14), command = lambda: accept_counting(window))
    select_host.place(x = 10, y = 50)
    select_client = Button(window, text = "    Refuse    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
    select_client.place(x = 182, y = 50)
    window.mainloop()

def accept_counting(win):
    win.destroy()
    accept_count = True

def wait_accept():
    window = Tk()
    window.title('You lose')
    frm=Frame(window, width=298, height=90, bg='gray79')
    frm.pack()
    text1 = Label(window, text = "Waiting for Opponent's response...",bg='gray79', fg='black', font=('Helvetica', 12))
    text1.place(x = 15, y = 30)
    if content != None:
        window.destroy()
        return
    window.mainloop()

def counting_house():
    global clusters_white_house, clusters_black_house
    cnt_white, cnt_black = 0, 0
    for cluster in clusters_white_house:
        for house in cluster:
            cnt_white+=1
    for cluster in clusters_black_house:
        for house in cluster:
            cnt_black+=1
    return cnt_black, cnt_white

def winneris(blackhouse, whitehouse):
    window = Tk()
    window.title('Result')
    frm=Frame(window, width=140, height=190, bg='gray89')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    text_black = Label(window, text='Black house: ' + str(blackhouse), bg='gray89', fg='black', font=('Helvetica', 12))
    text_black.place(x= 12, y= 10)
    text_white = Label(window, text='White house: ' + str(whitehouse), bg='gray89', fg='black', font=('Helvetica', 12))
    text_white.place(x= 12, y= 35)
    if blackhouse >= whitehouse + 3:
        text_whowin = Label(window, text='Black wins!', bg='gray89', fg='black', font=('Helvetica', 15))
    else:
        text_whowin = Label(window, text='White wins!', bg='gray89', fg='black', font=('Helvetica', 15))
    text_whowin.place(x=12, y= 70)
    '''select_host = Button(window, text = "    Accept    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
    select_host.place(x = 10, y = 50)
    select_client = Button(window, text = "    Refuse    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
    select_client.place(x = 182, y = 50)'''
    select_OK = Button(window, text = "    Confirm    ", height = 1, width = 10, font=('Helvetica', 14), command = quit)
    select_OK.place(x = 11, y = 120)
    window.mainloop()

def is_caught(blackorwhite):
    global clusters_black, clusters_white
    caught = True
    flag = False
    if blackorwhite == 1:
        for cluster in clusters_black:
            caught = True
            for (x, y) in cluster:
                for k in range(4):
                    newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                    if board[newx][newy] == 0:
                        caught = False
                        flag = True
                        break
            if flag:
                break
            if caught:
                clusters_black.remove(cluster)
                clusters_blank.append(cluster)
                return True
    else:
        for cluster in clusters_white:
            caught = True
            for (x, y) in cluster:
                for k in range(4):
                    newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                    if board[newx][newy] == 0:
                        caught = False
                        flag = True
                        break
                if flag:
                    break
            if caught:
                clusters_white.remove(cluster)
                clusters_blank.append(cluster)
                return True
    return False

def send_quit_msg():
    global connectionSock
    msg = 'Q I quit the game'
    connectionSock.send(msg.encode('utf-8'))

def check_valid_pos(i, j, turn, not_valid_house): # 작업 끝
    global clusters_black, clusters_black_house, clusters_white, clusters_white_house, clusters_neutral, clusters_blank
    make_cluster(1, BOARD_SIZE+1)
    if board[i][j] != 0:
        print('not blank')
        return False
    else:
        if turn >= 4:
            if not_valid_house == 1: #상대방 돌이 흑이면, 내가 둔 곳이 흑 집 클러스터 내부인지 확인
                for cluster in clusters_black_house:
                    if (i, j) in cluster:
                        print('black house')
                        return False
            else:
                for cluster in clusters_white_house:
                    if (i, j) in cluster:
                        print('white house')
                        return False
    return True

def close_socket(is_host):
    global serverSock, clientSock
    if is_host:
        serverSock.close()
    else:
        clientSock.close()
        
def notice_not_valid_point():
    window = Tk()
    window.title('You lose')
    frm=Frame(window, width=298, height=126, bg='gray79')
    frm.pack()
    text1 = Label(window, text = "You can\'t put your stone there.",bg='gray79', fg='black', font=('Helvetica', 12))
    text1.place(x = 15, y = 10)
    text2 = Label(window, text = "Press Confirm Button to return to game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text2.place(x = 15, y = 40)
    select_OFF = Button(window, text = "    Confirm    ", bg = 'snow', height = 1, width = 20, font=('Helvetica', 14), command = quit)
    select_OFF.place(x = 30, y = 76)
    window.mainloop()
        
def send_signals(line):
    global connectionSock
    connectionSock.send(line.encode('utf-8'))

def main_game():
    global connectionSock, is_host, running, content, board, mark_cluster
    global imgBoard, imgBlackStone, imgWhiteStone, imgNeutral, imgResignButton, imgCountRequestButton, fontObj
    pygame.init()
    my_stone = 1
    running = True
    screen=pygame.display.set_mode((800,720))
    pygame.display.set_caption('Great Kingdom')

    fontObj = pygame.font.Font(None, 50)
    
    if is_host:
        if random.random() > 0.5:
            whose_black = False
            my_stone = 2
            op_stone = 1
            textSurfaceObj1 = fontObj.render('White', True, (0,0,0))
            msg = 'w white'
        else:
            whose_black = True
            my_stone = 1
            op_stone = 2
            textSurfaceObj1 = fontObj.render('Black', True, (0,0,0))
            msg = 'w black'
        connectionSock.send(msg.encode('utf-8'))
    else:
        recvData = connectionSock.recv(1024)
        if recvData.decode('utf-8') == 'w black':
            my_stone = 2
            op_stone = 1
            textSurfaceObj1 = fontObj.render('White', True, (0,0,0))
        else:
            my_stone = 1
            op_stone = 2
            textSurfaceObj1 = fontObj.render('Black', True, (0,0,0))

    textRectObj1=textSurfaceObj1.get_rect()
    textRectObj1.center =(680,76)
    lst_text = [(textSurfaceObj1, textRectObj1)]

    turn = 1
    receiver = threading.Thread(target=receive, args = (connectionSock,))
    receiver.start()
    content = None

    clear_board()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                send_quit_msg()
                close_socket()
                sys.exit()
            elif event.type==MOUSEBUTTONDOWN and event.button==1:
                position = pygame.mouse.get_pos()
                posx, posy = int(position[0]), int(position[1])
                if (posx >= (LEFT_GRID[0] - POS_CATCH) and posx <= 558) and (posy >= (LEFT_GRID[1] - POS_CATCH) and posy <= 555): # 판 위를 클릭한 경우
                    if turn % 2 == my_stone % 2: # 내 턴인 경우
                        for i in range(9):
                            for j in range(9):
                                if (posx >= (round(LEFT_GRID[0]+GAP_GRID[0]*i) - POS_CATCH) and posx <= (round(LEFT_GRID[0]+GAP_GRID[0]*i) + POS_CATCH)) and (posy >= (round(LEFT_GRID[1]+GAP_GRID[1]*j) - POS_CATCH) and posy <= (round(LEFT_GRID[1]+GAP_GRID[1]*j) + POS_CATCH)): #i, j의 인식 범위를 누른 경우
                                    if check_valid_pos(i+1, j+1, turn, op_stone):
                                        board[i+1][j+1] = my_stone
                                        msg = 'c ' + str(i+1) + " " +str(j+1)
                                        connectionSock.send(msg.encode('utf-8'))
                                        if is_caught(op_stone): #내가 둔 돌로 인해 상대방이 잡힌 경우, 게임이 끝나는 경우
                                            blit_screen()
                                            pygame.display.flip()
                                            send_signals('s')
                                            you_win('c')
                                            close_socket()
                                            pygame.quit()
                                            sys.exit()
                                        turn += 1
                                    else:
                                        print('blank: ', clusters_blank)
                                        print('black: ', clusters_black_house)
                                        print('white: ', clusters_white_house)
                                        notice_not_valid_point()
                    else:
                        continue
                if (posx >= 97 and posx <= 283) and (posy >= 603 and posy <= 696): # 기권하기 버튼을 누른 경우, 게임이 끝나는 경우
                    msg = 'r I resign'
                    connectionSock.send(msg.encode('utf-8'))
                    time.sleep(0.1)
                    send_signals('s')
                    opponent_win('r')
                    pygame.quit()
                    close_socket()
                    sys.exit()
                if (posx >= 353 and posx <= 540) and (posy >= 603 and posy <= 696): # 계가하기 버튼을 누른 경우
                    msg = 'h I want Counting'
                    connectionSock.send(msg.encode('utf-8'))
                    wait_accept()
                    if content[0] == 'a' or content[0] == 'A': #상대가 수락한 경우, 게임이 끝나는 경우
                        black_house, white_house = counting_house()
                        send_signals('s')
                        winneris(black_house, white_house)
                        pygame.quit()
                        close_socket()
                        sys.exit()
                    else: 
                        continue
        blit_screen(screen, lst_text)
        pygame.display.flip()
        if content != None: # 상대방이 둔 수를 받는 경우
            print('opponent: ' + content)
            if turn % 2 != my_stone % 2 and (content[0] == 'c' or content[0] == 'C'):# #상대방이 좌표를 보낸 경우
                lst_words = list(content.split())
                x, y = int(lst_words[1]), int(lst_words[2])
                board[x][y] = op_stone
                print('blank: ', clusters_blank)
                print('black: ', clusters_black_house)
                print('white: ', clusters_white_house)
                if is_caught(my_stone): # 게임이 끝나는 경우
                    blit_screen()
                    pygame.display.flip()
                    send_signals('s')
                    opponent_win('c')
                    close_socket()
                    pygame.quit()
                    sys.exit()
                turn+=1
                make_cluster(1, BOARD_SIZE+1)
            elif content[0] == 'r' or content[0] == 'R': #상대방이 기권한 경우, 게임이 끝나는 경우
                send_signals('s')
                you_win('r')
                close_socket()
                pygame.quit()
                sys.exit()
            elif content[0] == 'Q' or content[0] == 'q': #상대방이 파이게임 창을 끈 경우, 게임이 끝나는 경우
                opponent_leaved()
                pygame.quit()
                close_socket()
                sys.exit()
            elif content[0] == 'h' or content[0] == 'H': #상대방이 계가를 요청한 경우
                request_counting()
                if accept_count: # 게임이 끝나는 경우
                    msg = 'a I accept your request'
                    connectionSock.send(msg.encode('utf-8'))
                    black_house, white_house = counting_house()
                    time.sleep(0.1)
                    send_signals('s')
                    winneris(black_house, white_house)
                    accept_count = False
                    pygame.quit()
                    close_socket()
                    sys.exit()
                else:
                    msg = 'n No I dont want'
                    connectionSock.send(msg.encode('utf-8'))
            content = None
            waste = pygame.mouse.get_pos()
        time.sleep(0.1)
############################################################################# End of main

def blit_screen(screen, lst_text):
    global imgBoard, imgBlackStone, imgWhiteStone, imgNeutral, imgResignButton, imgCountRequestButton
    screen.fill((255,255,255))
    screen.blit(imgBoard, (52,49))
    '''screen.blit(imgBlackStone, imgBlackStone_RectObj)
    screen.blit(imgWhiteStone, imgWhiteStone_RectObj)'''
    for i in range(9):
        for j in range(9):
            posx, posy = round(LEFT_TOP[0]+GAP[0]*(i-1)), round(LEFT_TOP[1]+GAP[1]*(j-1))
            if board[i+1][j+1] == 1:
                screen.blit(imgBlackStone, (posx, posy))
            elif board[i+1][j+1] == 2:
                screen.blit(imgWhiteStone, (posx, posy))
            elif board[i+1][j+1] == 3:
                screen.blit(imgNeutral, (posx, posy))
    screen.blit(imgResignButton, (95, 600))
    screen.blit(imgCountRequestButton, (350, 600))
    for textObj in lst_text:
        screen.blit(textObj[0], textObj[1])

def make_cluster(start, end):
    global clusters_black, clusters_black_house, clusters_white, clusters_white_house, clusters_neutral, clusters_blank, board, mark_cluster
    clusters_black = []
    clusters_black_house = []
    clusters_white = []
    clusters_white_house = []
    clusters_blank = []
    clusters_neutral = []
    for i in range(start, end):
        for j in range(start, end):
            if mark_cluster[i][j]:
                temp = []
                queue = []
                queue.append((i,j))
                mark_cluster[i][j] = False
                if board[i][j] == 0:#blank에 일단 넣는다.
                    while queue:
                        (x, y) = queue.pop()
                        temp.append((x,y))
                        for k in range(4):
                            newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                            if board[newx][newy] == 0 and mark_cluster[newx][newy]:
                                queue.append((newx, newy))
                                mark_cluster[newx][newy] = False
                    clusters_blank.append(temp)
                elif board[i][j] == 1:
                    while queue:
                        (x, y) = queue.pop()
                        temp.append((x,y))
                        for k in range(4):
                            newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                            if board[newx][newy] == 1 and mark_cluster[newx][newy]:
                                queue.append((newx, newy))
                                mark_cluster[newx][newy] = False
                    clusters_black.append(temp)
                elif board[i][j] == 2:
                    while queue:
                        (x, y) = queue.pop()
                        temp.append((x,y))
                        for k in range(4):
                            newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                            if board[newx][newy] == 2 and mark_cluster[newx][newy]:
                                queue.append((newx, newy))
                                mark_cluster[newx][newy] = False
                    clusters_white.append(temp)
    flag = True
    for cluster in clusters_blank: ### check if black house
        flag = True
        for (x, y) in cluster:
            for k in range(4):
                newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                if board[newx][newy] == 2:
                    flag = False
                    break
            if not flag:
                break
        if flag:
            clusters_black_house.append(cluster)
    for cluster in clusters_black_house:
        clusters_blank.remove(cluster)
    for cluster in clusters_blank: ### check if white house
        flag = True
        for (x, y) in cluster:
            for k in range(4):
                newx, newy = x+THECROSS[k][0], y+THECROSS[k][1]
                if board[newx][newy] == 1:
                    flag = False
                    break
            if not flag:
                break
        if flag:
            clusters_white_house.append(cluster)
    for cluster in clusters_white_house:
        clusters_blank.remove(cluster)
    for i in range(start, end):
        for j in range(start, end):
            mark_cluster[i][j] = True

def start_window():
    window=Tk()
    window.title('Host/Client Selection')
    frm=Frame(window, width=345, height=150, bg='gray50')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    select_host = Button(window, text = "    HOST    ", height = 5, width = 20, command = lambda: host_setting_window(window))
    select_host.place(x = 10, y = 30)
    select_client = Button(window, text = "    CLIENT    ", height = 5, width = 20, command = lambda: client_setting_window(window))
    select_client.place(x = 190, y = 30)
    window.mainloop()

def host_setting_window(window):
    window.destroy()
    new_window=Tk()
    new_window.title('Host Settings')
    frm=Frame(new_window, width=345, height=250, bg='gray50')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    l1=Label(new_window, text='Enter a Port number (4 digits)', bg='gray50', fg='white', font=('Helvetica', 15))
    l1.place(x=30, y=15)
    entry=Entry(new_window, width = 5, font = ('Helvetica', 20))
    entry.place(x=130, y=50)
    button_port = Button(new_window, text = "    Next Step    ", height = 2, width = 40, command = lambda: waiting_for_access(new_window, entry))
    button_port.place(x=30, y=100)
    button_back = Button(new_window, text = "    Back to Host/Client Selection    ", height = 2, width = 40, command = lambda: backto_start_window(new_window))
    button_back.place(x=30, y=150)
    new_window.mainloop()

def client_setting_window(window):
    window.destroy()
    new_window=Tk()
    new_window.title('Client Settings')
    frm=Frame(new_window, width=400, height=240, bg='gray50')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    l1=Label(new_window, text='Please put the IP Address and Port Number', bg='gray50', fg='white', font=('Helvetica', 14))
    l1.place(x=12, y=15)
    l2=Label(new_window, text='IP Address:', bg='gray50', fg='white', font=('Helvetica', 12))
    l2.place(x=60, y=76)
    l3=Label(new_window, text='Port Number: ', bg='gray50', fg='white', font=('Helvetica', 12))
    l3.place(x=60, y=126)
    entry_ip=Entry(new_window, width = 10, font = ('Helvetica', 18))
    entry_ip.place(x=160, y=70)
    entry_port=Entry(new_window, width = 10, font = ('Helvetica', 18))
    entry_port.place(x=160, y=120)
    button_ok = Button(new_window, text = "    Next Step    ", height = 2, width = 30, font = ('Helvetica', 13), command = lambda: client_check_valid_ip(new_window, entry_ip, entry_port))
    button_ok.place(x=50, y=180)
    new_window.mainloop()

def client_check_valid_ip(window, entry_ip, entry_port):
    global clientSock, connectionSock, is_host
    ip_address = entry_ip.get()
    port = int(entry_port.get())
    clientSock.connect((ip_address, port))
    connectionSock = clientSock
    window.destroy()
    is_host = False
    main_game()

def waiting_window(port_num, my_ip, stop_event):
    '''def check_stop_event():
        if stop_event.is_set():
            new_window.destroy()
            return
        else:
            new_window.after(100, check_stop_event)'''
    new_window=Tk()
    new_window.title('Waiting for Client...')
    frm=Frame(new_window, width=345, height=150, bg='white')
    frm.pack()
    l1=Label(new_window, text='상대방의 접속을 대기중입니다...', fg='black', font = ('Helvetica', 10))
    l1.place(x=10, y=10)
    l2=Label(new_window, text='IP Address: ' + my_ip, fg='black', font = ('Helvetica', 10))
    l2.place(x=10, y=50)
    l3=Label(new_window, text='Port Number: ' + str(port_num), fg='black', font = ('Helvetica', 10))
    l3.place(x=10, y=70)
    while not stop_event.is_set():
        new_window.update()
        time.sleep(0.1)

    new_window.destroy()

def waiting_for_access(window, entry):
    global serverSock
    global connectionSock
    port_num = int(entry.get())
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port_num))
    serverSock.listen(1)
    window.destroy()
    my_ip = gethostbyname(gethostname())
    stop_event = threading.Event()
    tk_thread = threading.Thread(target = waiting_window, args=(port_num, my_ip, stop_event))
    tk_thread.start()
    connectionSock, addr = serverSock.accept()
    time.sleep(0.1)
    stop_event.set()
    is_host = True
    main_game()

def backto_start_window(window):
    window.destroy()
    start_window()

start_window()