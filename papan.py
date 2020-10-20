import pygame
import time
import math

pygame.init()
# Memulai pygame

win = pygame.display.set_mode((1280,720)) # window dari pygamenya, ukurannya 1280x720 pixel

pygame.display.set_caption("Let's Play Halma!") # Judul gamenya

class cellboard(object):
    # Kelas untuk si petak+bidaknya
    bidak1 = [pygame.image.load("design/cellboard.png").convert(), pygame.image.load("design/dark-piece-cellboard.png"), pygame.image.load("design/invalid-move-light.png"), pygame.image.load("design/dark-piece-cellboard-1.png"), pygame.image.load("invalid-move-light.png")]
    # bidak1 untuk meload gambar dari assets, outputnya array of image
    # 0 untuk petak kosong, 1 untuk petak+bidak merah, 2 untuk petak+bidak merah yang diklik, 3 untuk petak+bidak kuning, 4 untuk petak+bidak kuning yang diklik

    def __init__(self,x,y,size):
        self.x = x # posisi x
        self.y = y # posisi y
        self.size = size
        self.status = 0 # 0 untuk petak kosong, 1 untuk petak+bidak merah, 2 untuk petak+bidak merah yang diklik, 3 untuk petak+bidak kuning, 4 untuk petak+bidak kuning yang diklik
        self.camp = 0 # 0 camp, 1 camp merah, 2 camp kuning
        self.clicked = 0 # dia lagi diklik atau ngga
        self.isStart = 0 # dia lagi mulai game atau ngga
        self.owner = 2 # 0 punya merah, 1 punya kuning, 2 ga punya siapa2
        self.hitbox = ((262 + self.x * int(55 * (8/self.size))), (130 + self.y * int(58 * (8/self.size))), int(53 * (8/self.size)), int(56 * (8/self.size))) #area yang bisa diklik

    def setStatus(self,status):
        self.status = status # 0 = kosong; 1,2,3,4 = ada isi

    def draw(self, win): # buat gambar
        if (self.isStart == 0 or self.clicked == 1):
            size = int(50 * (8/self.size))
            bidak1 = pygame.transform.scale(self.bidak1[self.status], (size,size))
            panjang = 262
            lebar = 130
            colsize = 55
            rowsize = 58
            win.blit(bidak1, ((262 + self.x * int(55 * (8/self.size))), 130 + (self.y * int(58 * (8/self.size)))))
            self.isStart = 0
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

class papan(object):
    # kumpulan cellboard
    okbut =  pygame.image.load('okbut.png')
    okbut = pygame.transform.scale(okbut, (241, 60))
    quitbut =  pygame.image.load('quitbut.png')
    quitbut = pygame.transform.scale(quitbut, (241, 60))
    play1 =  [pygame.image.load('player-one-turn.png'), pygame.image.load('player-one.png')]
    play2 =  [pygame.image.load('player-two.png'), pygame.image.load('player-two-turn.png')]

    def __init__(self,x,y,color):
        self.isi = [[]*x for i in range(y)] # matriks cellboardnya
        self.x = x #ukuran papan x
        self.y = y #ukuran papan y
        self.okayhitbox = (1020, 280, 241, 60)
        self.quithitbox = (1020, 380, 241, 60)
        self.turn = color # 0 player 1, 1 player 2
        self.time = 100
        #self.isStart = 1
        #self.turnChanged = 0

        # buat ngeload isinya
        i = 0
        j = 0
        for i in range(self.x):
            for j in range(self.y):
                self.isi[i].append(cellboard(i,j,self.x)) #append ke self.isi
                if (x != 16):
                    if color == 1:
                        if (i + j <= (x/2-1)): #ngeassign si merah
                            self.isi[i][j].camp = 1
                            self.isi[i][j].status = 1
                            self.isi[i][j].owner = 0
                        if ((((x-1)*2)-(i+j)) <= (x/2-1)): # ngeassign si kuning
                            self.isi[i][j].camp = 2
                            self.isi[i][j].status = 3
                            self.isi[i][j].owner = 1
                    else:
                        if ((((x-1)*2)-(i+j)) <= (x/2-1)): #ngeassign si merah
                            self.isi[i][j].camp = 1
                            self.isi[i][j].status = 1
                            self.isi[i][j].owner = 0
                        if (i + j <= (x/2-1)): # ngeassign si kuning
                            self.isi[i][j].camp = 2
                            self.isi[i][j].status = 3
                            self.isi[i][j].owner = 1
                else:
                    if color == 1:
                        if (i + j <= (12/2-1) and not(i == 5 or j == 5)): #ngeassign si merah
                            self.isi[i][j].camp = 1
                            self.isi[i][j].status = 1
                            self.isi[i][j].owner = 0
                        if ((((x-1)*2)-(i+j)) <= (12/2-1) and not(i == 10 or j == 10)): # ngeassign si kuning
                            self.isi[i][j].camp = 2
                            self.isi[i][j].status = 3
                            self.isi[i][j].owner = 1
                    else:
                        if ((((x-1)*2)-(i+j)) <= (12/2-1) and not(i == 10 or j == 10)): #ngeassign si merah
                            self.isi[i][j].camp = 1
                            self.isi[i][j].status = 1
                            self.isi[i][j].owner = 0
                        if (i + j <= (12/2-1) and not(i == 5 or j == 5)): # ngeassign si kuning
                            self.isi[i][j].camp = 2
                            self.isi[i][j].status = 3
                            self.isi[i][j].owner = 1

    def changeturn(self): #ganti turn
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        self.settime(100)

    def settime(self,time):
        self.time = time

    def drawtime(self,win):
        font = pygame.font.SysFont('Consolas', 30)
        mins, secs = divmod(self.time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        text = font.render('Time: ' + str(timer), 1, (250, 183, 50))
        win.blit(text, (1050, 65))
        pygame.display.update()

    def draw(self, win): # ngedraw papan (okay button, player turn, quit button sama cellboard)
        #x = 262
        #y = 130
        #colsize = 55
        #rowsize = 58

        #ngeloop buat ngeprint cellboard
        for i in range(self.x):
            for j in range(self.y):
                self.isi[i][j].draw(win)

        #ngeprint player1
        play1 = pygame.transform.scale(self.play1[self.turn-1], (126, 46))
        win.blit(play1, (842, 670))

        #ngeprint player1
        play2 = pygame.transform.scale(self.play2[self.turn-1], (126, 46))
        win.blit(play2, (10, 10))

        #ngeprint okay button
        win.blit(self.okbut, (1020, 280))
        #pygame.draw.rect(win, (255,0,0), self.okayhitbox,2)

        #ngeprint quit button
        win.blit(self.quitbut, (1020, 380))
        #pygame.draw.rect(win, (255,0,0), self.quithitbox,2)

    #Objective Function
    def objective(self, state):
        n = self.x

        mySum = 0
        enemySum = 0
        for i in range(n):
            for j in range(n):

                #cek pake status dari si cellboard (apakah dia ada bidak atau ga)
                if self.isi[i][j].status == 1  or self.isi[i][j].status == 3:

                    #ini rumusnya gara-gara ayyub ga konsisten hehe
                    if 2*self.isi[i][j].status - 1 == state.color:

                        #Jumlahin score player 1
                        mySum = mySum + i + j
                    else:

                        #Jumlahin score player 2
                        enemySum = enemySum + (n-i-1) + (n-j-1)

        return mySum - enemySum

class startstate(object):
    #setting permainan

    #ngeload gambar
    col1but = [pygame.image.load('radio-red.png'),pygame.image.load('radio-red-clicked.png')]
    col2but = [pygame.image.load('radio-yellow.png'),pygame.image.load('radio-yellow-clicked.png')]

    rad1but = [pygame.image.load('radio-8.png'), pygame.image.load('radio-8-clicked.png')]
    rad2but = [pygame.image.load('radio-10.png'), pygame.image.load('radio-10-clicked.png')]
    rad3but = [pygame.image.load('radio-16.png'), pygame.image.load('radio-16-clicked.png')]

    def __init__(self):
        #state dalam permainannya
        self.row = 0      #0 Null, 8 8x8 row, 10 10x10 row, 16 16x16 row
        self.player1 = 0  #0 human, 1 AI-Minimax, 2 AI-Minimax + Local search -> color auto red
        self.player2 = 0  #0 human, 1 AI-Minimax, 2 AI-Minimax + Local search -> color auto yellow
        self.color = 0 # 0 kosong, 1 merah, 2 kuning
        self.rad1hitbox = (490, 387, 65, 30)
        self.rad2hitbox = (590, 387, 75, 30)
        self.rad3hitbox = (700, 387, 75, 30)
        self.col1hitbox = (680, 500, 90, 24)
        self.col2hitbox = (475, 500, 145, 24)

    def setrow(self,row):
        self.row = row

    def setcolor(self,col):
        self.color = col

    def setplayer1(self,player1):
        self.player1 = player1

    def setplayer2(self,player2):
        self.player2 = player2

    def draw(self,win):
        rad1but = pygame.transform.scale(self.rad1but[((3-self.row) // 2) * self.row], (60, 24))
        rad2but = pygame.transform.scale(self.rad2but[ (1 - (self.row % 2)) * (self.row // 2)], (60, 24))
        rad3but = pygame.transform.scale(self.rad3but[self.row // 3], (60, 24))
        col2but = pygame.transform.scale(self.col2but[(1 - (self.color % 2)) * (self.color // 2)], (145, 24))
        col1but = pygame.transform.scale(self.col1but[((3-self.color) // 2) * self.color], (90, 24))
        #print(self.row, ((3-self.row) // 2) * self.row, (1 - (self.row % 2)) * (self.row // 2), self.row // 3 )
        win.blit(rad2but, (600, 390))
        #pygame.draw.rect(win, (255,0,0), self.rad2hitbox,2)
        win.blit(rad1but, (500, 390))
        #pygame.draw.rect(win, (255,0,0), self.rad1hitbox,2)
        win.blit(rad3but, (710, 390))
        #pygame.draw.rect(win, (255,0,0), self.rad3hitbox,2)
        #pygame.draw.rect(win, (255,0,0), self.col1hitbox,2)
        #pygame.draw.rect(win, (255,0,0), self.col2hitbox,2)

        #print(((3-self.row) // 2) * self.row, (1 - (self.row % 2)) * (self.row // 2), self.row // 3)
        win.blit(col1but, (680, 500))
        win.blit(col2but, (475, 500))
