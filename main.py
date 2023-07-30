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

def main_game(window):
    window.destroy()
    pygame.init()
    screen = pygame.display.set_mode((350, 500))
    pygame.display.set_caption("Great_Kindom_test")

    while 1:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type==QUIT : # Q랑 같은 역할이다. 나도 왜 이걸 따로 만들었는지 기억이 가물가물... 아... 0.1 버전 때는 버그 때문에 이거 안 먹어서 Q를 따로 만든거였어용ㅎㅎ 지금은 잘 먹음
                pygame.quit()
                sys.exit()
        pygame.display.flip()

def start_window():
    window=Tk()
    window.title('Host/Client 설정')
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
    new_window.title('호스트 설정')
    frm=Frame(new_window, width=345, height=250, bg='gray50')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    l1=Label(new_window, text='포트 넘버(4자리)를 설정해주세요.', bg='gray50', fg='white', font=('Helvetica', 15))
    l1.place(x=30, y=15)
    entry=Entry(new_window, width = 5, font = ('Helvetica', 20))
    entry.place(x=130, y=50)
    button_port = Button(new_window, text = "    입력 완료    ", height = 2, width = 40, command = lambda: waiting_for_access(new_window, entry))
    button_port.place(x=30, y=100)
    button_back = Button(new_window, text = "    Host/Client 세팅으로 돌아가기    ", height = 2, width = 40, command = lambda: backto_start_window(new_window))
    button_back.place(x=30, y=150)
    new_window.mainloop()

def client_setting_window(window):
    window.destroy()
    new_window=Tk()
    new_window.title('호스트 설정')
    frm=Frame(new_window, width=400, height=200, bg='gray50')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    l1=Label(new_window, text='접속할 상대의 IP 주소와 포트넘버를 입력해주세요.', bg='gray50', fg='white', font=('Helvetica', 13))
    l1.place(x=15, y=15)
    l2=Label(new_window, text='IP 주소', bg='gray50', fg='white', font=('Helvetica', 10))
    l2.place(x=85, y=77)
    l3=Label(new_window, text='포트 넘버', bg='gray50', fg='white', font=('Helvetica', 10))
    l3.place(x=85, y=127)
    entry_ip=Entry(new_window, width = 10, font = ('Helvetica', 18))
    entry_ip.place(x=160, y=70)
    entry_port=Entry(new_window, width = 10, font = ('Helvetica', 18))
    entry_port.place(x=160, y=120)
    new_window.mainloop()

def waiting_for_access(window, entry):
    port_num = entry.get()
    window.destroy()
    my_ip = gethostbyname(gethostname())
    new_window=Tk()
    new_window.title('호스트 대기중')
    frm=Frame(new_window, width=345, height=150, bg='white')
    '''frm=Frame(window, width=340, height=250, bg='black')'''
    frm.pack()
    test_text = port_num
    l1=Label(new_window, text='상대방의 접속을 대기중입니다...', fg='black', font = ('Helvetica', 10))
    l1.place(x=10, y=10)
    l2=Label(new_window, text='IP Address: ' + my_ip, fg='black', font = ('Helvetica', 10))
    l2.place(x=10, y=50)
    l3=Label(new_window, text='Port Number: ' + test_text, fg='black', font = ('Helvetica', 10))
    l3.place(x=10, y=70)
    new_window.mainloop()

def backto_start_window(window):
    window.destroy()
    start_window()

def test(window, entry):
    port = entry.get()
    window.destroy()
    print(port)

start_window()