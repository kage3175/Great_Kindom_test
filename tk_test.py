from tkinter import *

window = Tk()
window.title('Result')
frm=Frame(window, width=140, height=190, bg='gray89')
'''frm=Frame(window, width=340, height=250, bg='black')'''
frm.pack()
text_black = Label(window, text='Black house: ' + '10', bg='gray89', fg='black', font=('Helvetica', 12))
text_black.place(x= 12, y= 10)
text_white = Label(window, text='White house: ' + '4', bg='gray89', fg='black', font=('Helvetica', 12))
text_white.place(x= 12, y= 35)
text_whowin = Label(window, text='Black wins!', bg='gray89', fg='black', font=('Helvetica', 15))
text_whowin.place(x=12, y= 70)
'''select_host = Button(window, text = "    Accept    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
select_host.place(x = 10, y = 50)
select_client = Button(window, text = "    Refuse    ", height = 2, width = 13, font=('Helvetica', 14), command = quit)
select_client.place(x = 182, y = 50)'''
select_OK = Button(window, text = "    Confirm    ", height = 1, width = 10, font=('Helvetica', 14), command = quit)
select_OK.place(x = 11, y = 120)
window.mainloop()