from tkinter import *
from tkinter import messagebox
import numpy as np
import random
class Minesweeper:
    
    def __init__(self,tk):
        self.master = tk
        self.master.geometry('270x270')
        self.master.title("Hello, Mine!")
        self.start()
    def on_menu_9_9(self):
        self.row = 9
        self.col = 9
        self.master.geometry('270x270')
        self.drawWindow(self.row, self.col)
    def on_menu_16_16(self):
        self.row = 16
        self.col = 16
        self.master.geometry('480x480')
        self.drawWindow(self.row,self.col)
    def on_menu_16_30(self):
        self.row = 30
        self.col = 16
        self.master.geometry('900x480')
        self.drawWindow(self.row, self.col)
    def start(self):
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="9*9",command = self.on_menu_9_9)
        self.filemenu.add_command(label="16*16",command = self.on_menu_16_16)
        self.filemenu.add_command(label="16*30",command = self.on_menu_16_30)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit",command = self.master.destroy)

        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.master.config(menu=self.menubar)
    
    def drawWindow(self,row, col):
        self.count = 0
        self.a = row
        self.b = col
        self.pattern = np.arange(row*col*3).reshape(row,col,3)
        self.button = [[0] * self.row for _ in range(self.col)]
        self.alist = []
        self.blist = []
        self.mineCount = 0
        for i in range(0,row):
            for j in range(0,col):
                self.pattern[i][j][1] = 0
                self.pattern[i][j][0] = 0
                self.pattern[i][j][2] = 0
        if(col==9):
            self.mineCount = 10
            for i in range(self.mineCount):
                self.r1 = random.randint(0,8)
                self.r2 = random.randint(0,8)
                while [self.r1,self.r2] in self.alist:
                    self.r1 = random.randint(0,8)
                    self.r2 = random.randint(0,8)
                self.alist.append([self.r1,self.r2])
            
                
        if(col==16):
            self.mineCount = 40
            for i in range(self.mineCount):
                self.r1 = random.randint(0,15)
                self.r2 = random.randint(0,15)
                while [self.r1,self.r2] in self.alist:
                    self.r1 = random.randint(0,15)
                    self.r2 = random.randint(0,15)
                self.alist.append([self.r1,self.r2])
        if(col==30):
            self.mineCount = 99
            for i in range(self.mineCount):
                
                self.r1 = random.randint(0,15)
                self.r2 = random.randint(0,29)
                while [self.r1,self.r2] in self.alist:
                    self.r1 = random.randint(0,15)
                    self.r2 = random.randint(0,29)
                self.alist.append([self.r1,self.r2])
        for i in self.alist:
            self.pattern[i[0]][i[1]][1] = 1
        for x in range(0, row):
            for y in range(0,col):
                if(self.pattern[x][y][1] == 1):
                    try:
                        if(x-1>=0):
                            self.pattern[x-1][y][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(x-1>=0 and y-1>=0):
                            self.pattern[x-1][y-1][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(x-1>=0 and y+1<=col):
                            self.pattern[x-1][y+1][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(y+1<=col):
                            self.pattern[x][y+1][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(y-1>=0):
                            self.pattern[x][y-1][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(x+1<=row):
                            self.pattern[x+1][y][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(x+1<=row and y-1>=0):
                            self.pattern[x+1][y-1][0]+=1
                    except IndexError:
                        pass
                    try:
                        if(x+1<=row and y+1<=col):
                            self.pattern[x+1][y+1][0]+=1
                    except IndexError:
                        pass
                self.button[y][x] = Button(self.master, text=" ",height = 2,width = 3,command = lambda _x=y, _y=x : self.click(_x,_y))
                self.button[y][x].place(x=(x)*30,y=(y)*30)
                self.button[y][x].bind("<Button-3>",self.rightClick(x,y))
                
    def rightClick(self,row,col):
        return lambda Button: self.onRightClick(self.button[col][row],row,col)
    def onRightClick(self, b, row, col):
        if(b['text'] == 'X'):
            b['text'] = ' '
            self.count-=1
            self.pattern[col][row][2] = 0
        else:
            b['text'] = 'X'
            self.count+=1
            self.pattern[col][row][2] = 1
        if(self.count==self.mineCount):
            for x in range(0, self.a):
                for y in range(0,self.b):
                    if(self.pattern[x][y][1] == 1 and self.pattern[x][y][2]==1):
                        self.count-=1
                        
                    else:
                        continue
            if(self.count==0):
                messagebox.showinfo("Win","You Win")
                self.master.destroy()
            else:
                messagebox.showinfo("Failed","You lose")
                self.master.destroy()
    def click(self,row,col):
        if(self.pattern[row][col][1] == 1):
            self.button[row][col]['text'] = 'B'
            messagebox.showinfo("Bomb","Bommmmmmmmmmb")
            self.master.destroy()
        else:
            if(self.pattern[row][col][0] <=1 and self.pattern[row][col][1] == 0):
                self.search(row,col)
            else:
                self.button[row][col]['text'] = self.pattern[row][col][0]
                self.pattern[row][col][1] = 2
    def search(self,row,col):
        if(self.pattern[row][col][1]<=1 and self.pattern[row][col][0]!=0):
            self.button[row][col]['text'] = self.pattern[row][col][0]
            self.pattern[row][col][1] = 2
            return
        elif(self.pattern[row][col][1]==1):
            return
        elif(self.pattern[row][col][1]==2):
            return
        elif(self.pattern[row][col][0]<=1 and self.pattern[row][col][1]!=2):
            self.button[row][col]['text'] = self.pattern[row][col][0]
            self.pattern[row][col][1] = 2
            try:
                if(col-1>=0):
                    self.search(row,col-1)
            except IndexError:
                pass
            try:
                if(col+1<=self.b):
                    self.search(row,col+1)
            except IndexError:
                pass
            try:
                if(row+1<=self.a and col-1>=0):
                    self.search(row+1,col-1)
            except IndexError:
                pass
            try:
                if(row+1<=self.a and col+1<=self.b):
                    self.search(row+1,col+1)
            except IndexError:
                pass
            try:
                if(row+1<=self.a):
                    self.search(row+1,col)
            except IndexError:
                pass
            try:
                if(row-1>=0 and col-1>=0):
                    self.search(row-1,col-1)
            except IndexError:
                pass
            try:
                if(row-1>=0):
                    self.search(row-1,col)
            except IndexError:
                pass
            try:
                if(row-1>=0 and col+1<=self.b):
                    self.search(row-1,col+1)
            except IndexError:
                pass
        else:
            
            return
def main():
    window = Tk()
    window.title("Hello, Mine!")
    minesweeper = Minesweeper(window)
    window.mainloop()
                
if __name__=="__main__":
    main()
