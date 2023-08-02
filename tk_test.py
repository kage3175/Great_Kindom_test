from tkinter import *

def opponent_leaved():
    window = Tk()
    window.title('Opponent Leaved')
    frm=Frame(window, width=298, height=120, bg='gray79')
    frm.pack()
    text1 = Label(window, text = "Opponent leaved the game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text1.place(x = 15, y = 10)
    text2 = Label(window, text = "Press Confirm Button to quit the game.",bg='gray79', fg='black', font=('Helvetica', 12))
    text2.place(x = 15, y = 35)
    select_OFF = Button(window, text = "    Confirm    ", bg = 'snow', height = 1, width = 20, font=('Helvetica', 14), command = quit)
    select_OFF.place(x = 30, y = 71)
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
    
def wait_accept():
    window = Tk()
    window.title('You lose')
    frm=Frame(window, width=298, height=90, bg='gray79')
    frm.pack()
    text1 = Label(window, text = "Waiting for Opponent's response...",bg='gray79', fg='black', font=('Helvetica', 12))
    text1.place(x = 15, y = 30)
    window.mainloop()
    
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
    

'''window = Tk()
window.title('Result')
frm=Frame(window, width=140, height=190, bg='gray89')
frm=Frame(window, width=340, height=250, bg='black')
frm.pack()
text_black = Label(window, text='Black house: ' + '10', bg='gray89', fg='black', font=('Helvetica', 12))
text_black.place(x= 12, y= 10)
text_white = Label(window, text='White house: ' + '4', bg='gray89', fg='black', font=('Helvetica', 12))
text_white.place(x= 12, y= 35)
text_whowin = Label(window, text='Black wins!', bg='gray89', fg='black', font=('Helvetica', 15))
text_whowin.place(x=12, y= 70)
select_host = Button(window, text = "    Accept    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
select_host.place(x = 10, y = 50)
select_client = Button(window, text = "    Refuse    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
select_client.place(x = 182, y = 50)
select_OK = Button(window, text = "    Confirm    ", height = 1, width = 10, font=('Helvetica', 14), command = quit)
select_OK.place(x = 11, y = 120)
window.mainloop()'''

notice_not_valid_point()