import pygame
import time
import math
from papan import cellboard, papan, startstate

pygame.init()
# Memulai pygame

win = pygame.display.set_mode((1280,720)) # window dari pygamenya, ukurannya 1280x720 pixel

<<<<<<< Updated upstream
pygame.display.set_caption("Let's Play Halma!") # Judul gamenya
=======
pygame.display.set_caption("Bacod Adit") # Judul gamenya

class cellboard(object):
    # Kelas untuk si petak+bidaknya
    bidak1 = [pygame.image.load('cellboard-kosong.png').convert(), pygame.image.load('cellboard-bidak1.png'), pygame.image.load('cellboard-bidak1-move.png'), pygame.image.load('cellboard-bidak2.png'), pygame.image.load('cellboard-bidak2-move.png')]
    # bidak1 untuk meload gambar dari assets, outputnya array of image
    # 0 untuk petak kosong, 1 untuk petak+bidak merah, 2 untuk petak+bidak merah yang diklik, 3 untuk petak+bidak kuning, 4 untuk petak+bidak kuning yang diklik
    
    def __init__(self,x,y):
        self.x = x # posisi x
        self.y = y # posisi y
        self.status = 0 # 0 untuk petak kosong, 1 untuk petak+bidak merah, 2 untuk petak+bidak merah yang diklik, 3 untuk petak+bidak kuning, 4 untuk petak+bidak kuning yang diklik
        self.camp = 0 # 0 camp, 1 camp merah, 2 camp kuning
        self.clicked = 0 # dia lagi diklik atau ngga 
        self.isStart = 0 # dia lagi mulai game atau ngga
        self.owner = 2 # 0 punya merah, 1 punya kuning, 2 ga punya siapa2
        self.hitbox = ((262 + self.x * 55), (130 + self.y * 58), 53, 56) #area yang bisa diklik

    def setStatus(self,status):
        self.status = status # 0 = kosong; 1,2,3,4 = ada isi
    
    def draw(self, win): # buat gambar
        if (self.isStart == 0 or self.clicked == 1):
            bidak1 = pygame.transform.scale(self.bidak1[self.status], (50, 50))
            panjang = 262
            lebar = 130
            colsize = 55
            rowsize = 58
            win.blit(bidak1, ((panjang + self.x * colsize), lebar + (self.y * rowsize)))
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

    def __init__(self,x,y):
        self.isi = [[]*x for i in range(y)] # matriks cellboardnya
        self.x = x #ukuran papan x
        self.y = y #ukuran papan y
        self.okayhitbox = (1020, 280, 241, 60) 
        self.quithitbox = (1020, 380, 241, 60)
        self.turn = 0 # 0 player 1, 1 player 2
        #self.isStart = 1
        #self.turnChanged = 0

        # buat ngeload isinya
        for i in range(self.x):
            for j in range(self.y):
                self.isi[i].append(cellboard(i,j)) #append ke self.isi
                if (i + j <= (x-5)): #ngeassign si merah
                    self.isi[i][j].camp = 1
                    self.isi[i][j].status = 1
                    self.isi[i][j].owner = 0
                if ((((x-1)*2)-(i+j)) <= 3): # ngeassign si kuning
                    self.isi[i][j].camp = 2
                    self.isi[i][j].status = 3
                    self.isi[i][j].owner = 1

    def changeturn(self): #ganti turn
        if self.turn == 1:
            self.turn = 0
        else:
            self.turn = 1

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
        play1 = pygame.transform.scale(self.play1[self.turn], (126, 46))
        win.blit(play1, (842, 670))

        #ngeprint player1
        play2 = pygame.transform.scale(self.play2[self.turn], (126, 46))
        win.blit(play2, (10, 10))

        #ngeprint okay button
        win.blit(self.okbut, (1020, 280))
        #pygame.draw.rect(win, (255,0,0), self.okayhitbox,2)

        #ngeprint quit button
        win.blit(self.quitbut, (1020, 380))
        #pygame.draw.rect(win, (255,0,0), self.quithitbox,2)

class startstate(object):
    #setting permainan

    #ngeload gambar
    col1but = pygame.image.load('radio-red.png')
    col2but = pygame.image.load('radio-yellow.png')
    col2but = pygame.transform.scale(col2but, (145, 24))
    col1but = pygame.transform.scale(col1but, (90, 24))
    rad1but = [pygame.image.load('radio-8.png'), pygame.image.load('radio-8-clicked.png')]
    rad2but = [pygame.image.load('radio-10.png'), pygame.image.load('radio-10-clicked.png')]
    rad3but = [pygame.image.load('radio-16.png'), pygame.image.load('radio-16-clicked.png')]

    def __init__(self):
        #state dalam permainannya
        self.row = 0      #0 Null, 4 8x8 row, 2 10x10 row, 3 16x16 row
        self.player1 = 0  #0 human, 1 AI-Minimax, 2 AI-Minimax + Local search -> color auto red
        self.player2 = 0  #0 human, 1 AI-Minimax, 2 AI-Minimax + Local search -> color auto yellow
        self.rad1hitbox = (490, 387, 65, 30)
        self.rad2hitbox = (590, 387, 75, 30)
        self.rad3hitbox = (700, 387, 75, 30)
        
    def setrow(self,row):
        self.row = row

    def setplayer1(self,player1):
        self.player1 = player1 
    
    def setplayer2(self,player2):
        self.player2 = player2

    def draw(self,win):
        rad1but = pygame.transform.scale(self.rad1but[((3-self.row) // 2) * self.row], (60, 24))
        rad2but = pygame.transform.scale(self.rad2but[ (1 - (self.row % 2)) * (self.row // 2)], (60, 24))
        rad3but = pygame.transform.scale(self.rad3but[self.row // 3], (60, 24))
        win.blit(rad2but, (600, 390))
        #pygame.draw.rect(win, (255,0,0), self.rad2hitbox,2)
        win.blit(rad1but, (500, 390))
        #pygame.draw.rect(win, (255,0,0), self.rad1hitbox,2)
        win.blit(rad3but, (710, 390))
        #pygame.draw.rect(win, (255,0,0), self.rad3hitbox,2)

        #print(((3-self.row) // 2) * self.row, (1 - (self.row % 2)) * (self.row // 2), self.row // 3)
        #win.blit(self.col1but, (680, 500))      
        #win.blit(self.col2but, (475, 500))

    def size(self):
        if (self.row == 4):
            return 8
        elif (self.row == 2):
            return 10
        elif (self.row == 3):
            return 16
        else:
            return 0

###############################################################################################################################################################################################################################################################################################
# ^^^ dia namanya shafa ^^^ #
class point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
>>>>>>> Stashed changes

def redrawGameWindow():
    #buat ngedraw game window
    win.blit(bg, (0,0))
    if start:
        halma.draw(win)
    if not start:
        board.draw(win)
        board.drawtime(win)
    pygame.display.update()

def cekTetangga(x,y,a,b):
    # buat cek tetangga?
    return (x-a == 1 and y-b == 1) or (a-x == 1 and y-b == 1) or (x-a == 1 and b-y == 1) or (a-x == 1 and b-y == 1) or (x-a == 0 and y-b == 1) or (x-a == 1 and y-b == 0) or (x-a == 0 and b-y == 1) or (a-x == 1 and y-b == 0)

<<<<<<< Updated upstream
=======
objectiveValue8 = [[0,15,30,30,35,35,35,35], [15, 35, 40, 45, 45, 45, 45, 45], [30, 40, 55, 55, 55, 55, 55, 55], [30, 45, 55, 65, 65, 65, 65, 65], [35, 45, 55, 65, 75, 75, 75, 85], [35, 45, 55, 65, 75, 75, 75, 85], [35, 45, 55, 65, 75, 90, 95, 95], [35, 45, 55, 65, 85, 90, 95, 100]]
objectiveValue10 = [[0,15,20,25,30,35,35,35,35,35], [15,25,30,35,40,40,40,40,40,40], [20,30,35,45,45,45,45,45,45,45], [25,35,45,55,55,55,55,55,55,55], [30,40,45,55,65,65,65,65,65,65], [35,40,45,55,65,70,70,70,70,80], [35,40,45,55,65,70,80,80,85,85], [35,40,45,55,65,70,80,85,90,90], [35,40,45,55,65,70,85,90,95,95], [35,40,45,55,65,80,85,90,95,100]]
objectiveValue16 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

def fungsiObjektif(x,y,size):
    if (size == 8):
        global objectiveValue8
        return objectiveValue8[x][y]
    elif (size == 10):
        global objectiveValue10
        return objectiveValue10[x][y]
    else:
        global objectiveValue16
        return objectiveValue16[x][y]
        
def possibleMove(papan, pioneer):
    allMove = [] 
    for i in range ((pioneer.x)-1, (pioneer.x)+1)
        for j in range ((pioneer.y)-1, (pioneer.y)+1)
            if (cekTetangga(pioneer.x,pioneer.y,i,j) and (pioneer.x != i and pioneer.y=j) and i >= 0 and i <= papan.x and j>=0 and j<= papan.y):
                if (papan.isi[i][j].status == 0)
                    papanTemp = copy.deepcopy(papan)
                    papanTemp.isi[pioneer.x][pioneer.y].status = 0
                    lastPiece = board.isi[i][j]

    sedangLoncat = False #buat tau dia loncat atau ngga
    pioneer

    return allMove

def minimax(papan, player, depth, size, score):
    result = checkWinner()
    if (result != null):
        score = scores[result]
        return score

    pion = []
    for i in range (len(papan.isi)):
        for j in range (len(papan.isi[i])):
            #Pion bot
            if (papan.isi[i][j].owner == player):
                pion.append(papan.isi[i][j])

    gerakYangMungkin = []
    for pioneer in pion:
        for i in range (len(papan.isi)):
            for j in range (len(papan.isi[i])):
                if papan.isi[]
                    gerakYangMungkin.append()

            
def min(papan, player, depth, size):


def max(papan, player, depth, size):
    if (depth == 3):
        return fungsiObjektif(x,y,papan.)
    min


def bestMove(papan, player):
    #papan berkelas startstate
    #color: 0 merah, 1 kuning
    bestScore = -999
    score = minimax(papan, player, 0, false, papan.size())
        if (score > bestScore):
            bestScore = score
            bestX = pion.x
            bestY = pion.y

    #Pindahin pake x dan y

    #ganti turn
    
                    

>>>>>>> Stashed changes
# MAIN

halma = startstate() # memulai permainan

run = True #gamenya masih jalan?
start = True #dia lagi lagi di page mana? kalo true berarti di page awal, kalo false berarti di page permainan
hasSetRow = False
hasSetColor = False

bg1 = [pygame.image.load("design/Landing-page-bg.png"), pygame.image.load("design/Game-2.png")]
bg = pygame.transform.scale(bg1[0], (1280, 720))
win.blit(bg, (0,0))
#buat ngeload background

curPiece = [] #array cellboard yang lagi diklik
countLoop = 1 #buat menghitung
sedangLoncat = False #buat tau dia loncat atau ngga

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

##### ALGORITMA UTAMA ######
while run:

    if start: #kalau dia lagi di page 1
        for event in pygame.event.get(): # menangkap apa saja yang terjadi dipagenya
            if event.type == pygame.MOUSEBUTTONDOWN: # jika sedang menklik
            # Set the x, y postions of the mouse click
                x, y = event.pos # posisi dari klikannya
                if pygame.Rect(halma.rad1hitbox).collidepoint(event.pos): #kalo misal rad1hitbox lagi diklik
                    halma.setrow(1)  #set rownya = 1 -> ukuran papan 8x8
                    ukuranPapan = 8
                    hasSetRow = True
                if pygame.Rect(halma.rad2hitbox).collidepoint(event.pos):
                    halma.setrow(2) #set rownya = 2 -> ukuran papan 10x10
                    ukuranPapan = 10
                    hasSetRow = True
                if pygame.Rect(halma.rad3hitbox).collidepoint(event.pos):
                    halma.setrow(3) #set rownya = 3 -> ukuran papan 10x10
                    ukuranPapan = 16
                    hasSetRow = True
                if pygame.Rect(halma.col1hitbox).collidepoint(event.pos): #kalo misal rad1hitbox lagi diklik
                    halma.setcolor(1)
                    hasSetColor = True
                if pygame.Rect(halma.col2hitbox).collidepoint(event.pos):
                    halma.setcolor(2)
                    hasSetColor = True
            if hasSetColor and hasSetRow: #kalo udah ngesetting
                if event.type == pygame.KEYDOWN: #kalau dia mencet sesuatu
                    if event.key == pygame.K_SPACE: #kalau dia mencet space
                        start = False #biar bisa pindah page
                        bg = pygame.transform.scale(bg1[1], (1280, 720))
                        win.blit(bg, (0,0))
                        # ngeserve background page selanjutnya
                        board = papan(ukuranPapan,ukuranPapan,halma.color)
            if event.type == pygame.QUIT: #buat quit
                run = False
    else:
        if board.time == 0:
            #ngeback semua yang udah terjadi
            for kotak in curPiece:
                kotak.clicked = 0
                if kotak == firstPiece:
                    kotak.setStatus(kotak.status-1)
                else:
                    kotak.setStatus(kotak.status-((firstPiece.owner+1)*2))
            curPiece.clear()
            lastX, lastY = -1, -1
            countLoop = 1
            sedangLoncat = False
            board.changeturn()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                board.settime(board.time-1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(board.quithitbox).collidepoint(event.pos):
                    #ngeback semua yang udah terjadi
                    for kotak in curPiece:
                        kotak.clicked = 0
                        if kotak == firstPiece:
                            kotak.setStatus(kotak.status-1)
                        else:
                            kotak.setStatus(kotak.status-((firstPiece.owner+1)*2))
                    curPiece.clear()
                    lastX, lastY = -1, -1
                    countLoop = 1
                    sedangLoncat = False
<<<<<<< Updated upstream

                if pygame.Rect(board.okayhitbox).collidepoint(event.pos):
=======
                if pygame.Rect(board.okayhitbox).collidepoint(event.pos): #Okay hitbox
>>>>>>> Stashed changes
                    if (len(curPiece) > 1): #intinya minimal ada 2 cellboard yang lagi diklik
                        #dia ngubah turn dia mengubah lastclicked jadi bidak yang ada isinya, sisanya jadi bidak kosong, terus ngereset curPiece, lastX,lastY, dan sedang loncat
                        board.changeturn()
                        for kotak in curPiece:
                            kotak.clicked = 0
                            if kotak == lastPiece:
                                kotak.setStatus(kotak.status - 1)
                            else:
                                kotak.setStatus(0)
                        curPiece.clear()
                        lastX, lastY = -1, -1
                        countLoop = 1
                        sedangLoncat = False
                        print(board.objective(halma))
                    """
                    else:
                        board.changeturn()
                        for kotak in curPiece:
                            kotak.setStatus(kotak.status - 1)
                            kotak.clicked = 0
                        curPiece.clear()
                        lastX, lastY = -1, -1
                        countLoop = 1
                        sedangLoncat = False
                    """
                for i in range(ukuranPapan):
                    for j in range(ukuranPapan):
                        if pygame.Rect(board.isi[i][j].hitbox).collidepoint(event.pos): #kalo misal cellboard i,j lagi diklik
                            if not curPiece: #belum ada yang diklik
                                if (board.isi[i][j].owner == board.turn-1) and ((board.isi[i][j].status == 1) or (board.isi[i][j].status == 3)): #jika dia klik board punya dia dan statusnya 1 atau 3
                                    board.isi[i][j].clicked = 1 #board itu lagi diklik
                                    lastX, lastY = i, j #last index yang gw klik
                                    board.isi[i][j].setStatus(board.isi[i][j].status+1) #ngubah status dari bidak ada isi ke lagi diklik
                                    curPiece.append(board.isi[i][j]) #masukin si cellboardnya ke curpiece
                                    firstPiece = board.isi[i][j] #cellboard pertama yang lagi diklik
                            else: #kalo udah ada yang diklik
                                if (firstPiece.owner == board.turn-1 and countLoop > 0 and board.isi[i][j].status == 0): #jika turnnya turn dia, countLoopnya masih ada dan yang diklik kosong
                                    a = math.floor((i + lastX)/2) #bidak musuh
                                    b = math.floor((j + lastY)/2)
                                    c = (i + lastX)/2
                                    d = (j + lastY)/2
                                    #print(lastX,lastY,a,b,c,d)

                                    if not ((firstPiece.camp == 0 and board.isi[i][j].camp == firstPiece.owner+1) or (firstPiece.camp != 0 and board.isi[i][j].camp == 0 and firstPiece.owner+1 != firstPiece.camp)): #Ini biar dia gabisa keluar dari camp musuh kalo udah nyampe
                                        if (cekTetangga(a,b,lastX,lastY) and cekTetangga(i,j,a,b) and (c.is_integer() and d.is_integer() > 0) and (((board.isi[a][b].status == 1) or (board.isi[a][b].status == 3)) and ((board.isi[lastX][lastY].status == 4) or (board.isi[lastX][lastY].status == 2)))):
                                            #intinya dia pengen loncat
                                            sedangLoncat = True
                                            board.isi[i][j].setStatus(board.isi[i][j].status+((firstPiece.owner+1)*2))
                                            curPiece.append(board.isi[i][j])
                                            lastX, lastY = i, j
                                            board.isi[i][j].clicked = 1
                                            board.isi[i][j].owner = firstPiece.owner
                                            lastPiece = board.isi[i][j]

                                        if (sedangLoncat == False and cekTetangga(i,j,lastX,lastY)):
                                            #intinya dia pengen gerak ke sekitar
                                            countLoop -= 1
                                            board.isi[i][j].setStatus(board.isi[i][j].status+((firstPiece.owner+1)*2))
                                            curPiece.append(board.isi[i][j])
                                            lastX, lastY = i, j
                                            board.isi[i][j].clicked = 1
                                            board.isi[i][j].owner = firstPiece.owner
                                            lastPiece = board.isi[i][j]

            if event.type == pygame.QUIT:
                run = False

    redrawGameWindow() #menggambar ulang window


pygame.quit()
