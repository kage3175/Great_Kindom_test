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

### Pygame 관련 전역변수들
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
port_num = 0
fpsClock = pygame.time.Clock()

clusters_black = []
clusters_white = []
clusters_neutral = []
clusters_black_house = []
clusters_white_house = []
clusters_blank = []

is_host = 0

serverSock = socket(AF_INET, SOCK_STREAM)
clientSock = socket(AF_INET, SOCK_STREAM)
sender = ''
receiver = ''
connectionSock = None

def send(sock):
    while True:
        sendData = input(">>>")
        sock.send(sendData.encode('utf-8'))

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print("상대방:", recvData.decode('utf-8'))

def main_game():
    global connectionSock, receiver, sender
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
                msg = str(position[0]) + " " + str(position[1])
                connectionSock.send(msg.encode('utf-8'))
                print(position)
        screen.fill((255,255,255))
        screen.blit(imgBoard, (52,49))
        '''screen.blit(imgBlackStone, imgBlackStone_RectObj)
        screen.blit(imgWhiteStone, imgWhiteStone_RectObj)'''
        for i in range(9):
            screen.blit(imgBlackStone, (round(LEFT_TOP[0]+GAP[0]*(i-1)), round(LEFT_TOP[1]+GAP[1]*(i-1))))
        pygame.display.flip()


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
    global clientSock, sender, receiver
    ip_address = entry_ip.get()
    port = int(entry_port.get())
    print('x')
    clientSock.connect((ip_address, port))
    sender = threading.Thread(target = send, args = (clientSock, ))
    receiver = threading.Thread(target = receive, args = (clientSock, ))

    sender.start()
    receiver.start()
    window.destroy()
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
    global sender
    global receiver
    global connectionSock
    port_num = int(entry.get())
    print(port_num)
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port_num))
    serverSock.listen(1)
    window.destroy()
    my_ip = gethostbyname(gethostname())
    stop_event = threading.Event()
    tk_thread = threading.Thread(target = waiting_window, args=(port_num, my_ip, stop_event))
    tk_thread.start()
    connectionSock, addr = serverSock.accept()
    print(3)
    time.sleep(0.1)
    stop_event.set()
    is_host = 0
    sender = threading.Thread(target = send, args = (connectionSock, ))
    receiver = threading.Thread(target = receive, args = (connectionSock, ))
    sender.start()
    receiver.start()
    print(4)
    main_game()

def backto_start_window(window):
    window.destroy()
    start_window()

def test(window, entry):
    port = entry.get()
    window.destroy()
    print(port)

start_window()