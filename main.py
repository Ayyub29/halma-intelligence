import pygame
import random
import time
import math
from papan import cellboard, papan, startstate
import copy

pygame.init()
# Memulai pygame

win = pygame.display.set_mode((1280,720)) # window dari pygamenya, ukurannya 1280x720 pixel

pygame.display.set_caption("Let's Play Halma!") # Judul gamenya

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

def possibleMove(papan, pion):
    allmove = []
    sedangLoncat = False
    for i in range(papan.x):
        for j in range(papan.x):
            if not ((pion.camp == 0 and papan.isi[i][j].camp == pion.owner+1) or (pion.camp != 0 and papan.isi[i][j].camp == 0 and pion.owner+1 != pion.camp)): #Ini biar dia gabisa keluar dari camp musuh kalo udah nyampe
                if cekTetangga(papan.isi[i][j].x,papan.isi[i][j].y,pion.x,pion.y) and papan.isi[i][j].status == 0:
                    allmove.append(papan.isi[i][j])
                if cekTetangga(papan.isi[i][j].x,papan.isi[i][j].y,pion.x,pion.y) and (papan.isi[i][j].status == 1 or papan.isi[i][j].status == 3):
                    a = pion.x - 2*i if (pion.x -2*i > 0) else 2*i- pion.x
                    b = pion.y - 2*j if (pion.y -2*j > 0) else 2*j- pion.y
                    c = math.floor((a + pion.x)/2)
                    d = math.floor((b + pion.y)/2)

                    if (a >= 0 and a < 8 and b >= 0 and b < 8) and (c == i and d == j):
                        if (papan.isi[a][b].status == 0):
                            #print(c,d,i,j)
                            #print(a,b)
                            piece = papan.isi[a][b]
                            allmove.append(papan.isi[a][b])
                            sedangLoncat = True

    adayangbisadiloncat = False
    while sedangLoncat:
        for k in range(papan.x):
            for l in range(papan.x):
                if cekTetangga(papan.isi[k][l].x,papan.isi[k][l].y,piece.x,piece.y) and papan.isi[k][l].status == 0:
                    adayangbisadiloncat = False
                if cekTetangga(papan.isi[k][l].x,papan.isi[k][l].y,piece.x,piece.y) and (papan.isi[k][l].status == 1 or papan.isi[k][l].status == 3):
                    a = piece.x - 2*k if (piece.x -2*k > 0) else 2*k- piece.x
                    b = piece.y - 2*l if (piece.y -2*l > 0) else 2*l- piece.y
                    c = math.floor((a + piece.x)/2)
                    d = math.floor((b + piece.y)/2)

                    if (a >= 0 and a < 8 and b >= 0 and b < 8) and (c == k and d == l):
                        if (papan.isi[a][b].status == 0 and not (piece.x == papan.isi[a][b].x and piece.y == papan.isi[a][b].y)):
                            #print(c,d,i,j)
                            #print(a,b)
                            piece = papan.isi[a][b]
                            allmove.append(papan.isi[a][b])
                            adayangbisadiloncat = True
        if adayangbisadiloncat == False:
            sedangLoncat = False

    return allmove

def maxValue(board, player, depth, alpha, beta):
    if (depth == 0):
        return fungsiObjektif(board)

    pion = []
    for i in range (len(board.isi)):
        for j in range (len(board.isi[i])):
            #Pion bot
            if (board.isi[i][j].owner == player-1):
                pion.append(board.isi[i][j])

    allMove = []
    allPapan = []
    for bidak in pion:
        for move in (possibleMove(board, bidak)):
            papanTemp = copy.deepcopy(board)
            papanTemp.isi[bidak.x][bidak.y].status = 0
            papanTemp.isi[bidak.x][bidak.y].owner = 2
            papanTemp.isi[move.x][move.y] = copy.deepcopy(move)
            allPapan.append(papanTemp)

    bestValue = -(math.inf)
    # bestPapan = papan()
    for boards in allPapan:
        val = minValue(boards, abs(player-1), depth-1, alpha, beta)
        if (val > bestValue):
            bestValue = val
            beta = min(beta, val)
        if (bestValue <= alpha):
            return bestValue
        alpha = max(alpha, val)
        # bestPapan = boards
    return bestValue

def minValue(board, player, depth, alpha, beta):
    if (depth == 0):
        return fungsiObjektif(board)

    pion = []
    for i in range (len(board.isi)):
        for j in range (len(board.isi[i])):
            #Pion bot
            if (board.isi[i][j].owner == player-1):
                pion.append(board.isi[i][j])

    allPapan = []
    for bidak in pion:
        for move in (possibleMove(board, bidak)):
            papanTemp = copy.deepcopy(board)
            papanTemp.isi[bidak.x][bidak.y].status = 0
            papanTemp.isi[bidak.x][bidak.y].owner = 2
            papanTemp.isi[move.x][move.y] = copy.deepcopy(move)
            allPapan.append(papanTemp)

    worstValue = math.inf
    for boards in allPapan:
        val = maxValue(boards, abs(player-1), depth-1,alpha, beta)
        if (val < worstValue):
            worstValue = val
        if (worstValue >= beta):
            return worstValue
        alpha = max(alpha, val)

    return worstValue


def minimax(board, player, depth):
    # result = checkWinner()
    # if (result != null):
    #     return result

    pion = []
    for i in range (len(board.isi)):
        for j in range (len(board.isi[i])):
            # Pion bot
            if (board.isi[i][j].owner == player-1):
                pion.append(board.isi[i][j])

    allMove = []
    allPapan = []
    t = 10
    for bidak in pion:
        for move in (possibleMove(board, bidak)):
            if (t > 0):
                print(move.x,move.y)
                papanTemp = copy.deepcopy(board)
                pionTemp = copy.deepcopy(move)
                papanTemp.isi[pionTemp.x][pionTemp.y].status = bidak.status
                papanTemp.isi[pionTemp.x][pionTemp.y].owner = bidak.owner
                papanTemp.isi[bidak.x][bidak.y].status = 0
                papanTemp.isi[bidak.x][bidak.y].owner = 2
                allPapan.append(papanTemp)
                t -= 1

    bestValue = -(math.inf)
    bestPapan = papan(board.x,board.y,board.turn,board.mode)
    for boards in allPapan:
        val = minValue(boards, player, depth-1, -(math.inf), math.inf)
        if (val > bestValue):
            bestValue = val
            bestPapan = boards

    return bestPapan

objectiveValue8 = [[10,5,5,5,5,5,0,0], [10, 30, 30, 20, 20, 15, 10, 10], [10, 30, 35, 30, 25, 15, 20, 10], [10, 25, 45, 65, 65, 45, 25, 10], [10, 25, 65, 75, 75, 75, 75, 100], [10, 45, 55, 65, 75, 75, 105, 105], [10, 45, 55, 65, 75, 100, 105, 110], [10, 45, 55, 65, 105, 110, 115, 120]]
objectiveValue10 = [[10,10,5,5,5,5,0,0,0,0], [10,30,30,25,25,15,15,10,10,0], [10,35,45,35,35,35,25,15,15,0], [10,35,55,55,65,75,65,55,35,15], [15,35,55,65,75,85,85,75,55,20], [15,40,45,55,65,70,70,70,70,105], [15,40,45,55,65,70,80,80,105,110], [20,40,45,55,65,70,80,105,110,115], [20,40,45,55,65,70,105,110,115,120], [25,40,45,55,65,105,110,115,120,125]]
objectiveValue16 = [[15,15,10,10,10,10,5,5,5,5,5,5,0,0,0,0], [15,25,25,20,20,15,15,15,15,10,10,10,5,5,0], [5,15,30,27,25,25,25,22,20,20,15,15,15,10,10,10], [5,10,25,35,27,25,25,25,25,20,20,15,15,10,10,10], [10,10,15,15,20,30,35,30,25,25,20,20,15,15,15,15], [10,15,20,25,25,25,35,45,40,35,30,25,20,20,15,15], [10,15,20,20,25,30,35,35,45,35,30,25,25,20,20,15], [15,20,20,25,30,30,45,50,55,45,45,40,40,40,35,105], [15,20,20,25,25,25,35,35,35,55,45,45,45,40,105,110], [20,25,25,30,35,35,40,45,50,55,55,55,55,105,110,115], [20,25,25,30,35,35,45,50,55,60,65,65,65,105,110,115], [20,30,30,30,35,45,50,55,65,65,70,70,105,110,115,120], [20,35,35,40,45,50,50,55,65,65,70,105,110,115,120,125], [15,35,35,45,50,55,55,65,75,75,105,110,115,120,125,130], [20,30,40,50,60,65,75,75,105,110,115,120,125,130,135,135], [15,25,35,45,55,65,65,85,105,110,115,120,125,130,135,140]

for i in range(8):
    for j in range(8):
        print(objectiveValue8[i][j],end="")
    print()

def cellObjektif(board,i,j):
    if board.x == 8:
        return objectiveValue8[i][j]
    elif board.x == 10:
        return objectiveValue10[i][j]
    else:
        return objectiveValue16[i][j]


def fungsiObjektif(board):
    n = board.x

    mySum = 0
    enemySum = 0
    for i in range(n):
        for j in range(n):

            #cek pake status dari si cellboard (apakah dia ada bidak atau ga)
            if board.isi[i][j].status == 1  or board.isi[i][j].status == 3:
                #if 2*self.isi[i][j].status - 1 == state.color:
                if board.isi[i][j].status == (board.turn+1)/2:
                    #Jumlahin score player 1
                    mySum = mySum + cellObjektif(board,i,j)
                else:

                    #Jumlahin score player 2
                    enemySum = enemySum + cellObjektif(board, i, j)

    return mySum - enemySum

def localMinimax(board, player, depth):
    # result = checkWinner()
    # if (result != null):
    #     return result

    pion = []
    for i in range (len(board.isi)):
        for j in range (len(board.isi[i])):
            # Pion bot
            if (board.isi[i][j].owner == player-1):
                pion.append(board.isi[i][j])

    allPapan = []
    for bidak in pion:
        for move in (possibleMove(board, bidak)):
            print(move.x,move.y)
            papanTemp = copy.deepcopy(board)
            pionTemp = copy.deepcopy(move)
            papanTemp.isi[pionTemp.x][pionTemp.y].status = bidak.status
            papanTemp.isi[pionTemp.x][pionTemp.y].owner = bidak.owner
            papanTemp.isi[bidak.x][bidak.y].status = 0
            papanTemp.isi[bidak.x][bidak.y].owner = 2
            allPapan.append(papanTemp)

    successorBoard = board
    loop = True
    while loop:
        neighbor = random.choice(allPapan)
        if fungsiObjektif(successorBoard) > fungsiObjektif(neighbor):
            loop = False
            return successorBoard

            successorBoard = neighbor
# MAIN

halma = startstate() # memulai permainan

run = True #gamenya masih jalan?
start = True #dia lagi lagi di page mana? kalo true berarti di page awal, kalo false berarti di page permainan
hasSetRow = False
hasSetColor = False
hasSetMode = False

bg1 = [pygame.image.load('bgstart1.png'), pygame.image.load('bggame.png')]
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
                if pygame.Rect(halma.mod1hitbox).collidepoint(event.pos): #kalo misal rad1hitbox lagi diklik
                    halma.setmode(1)  #set rownya = 1 -> ukuran papan 8x8
                    hasSetMode = True
                if pygame.Rect(halma.mod2hitbox).collidepoint(event.pos):
                    halma.setmode(2) #set rownya = 2 -> ukuran papan 10x10
                    hasSetMode = True
                if pygame.Rect(halma.mod3hitbox).collidepoint(event.pos):
                    halma.setmode(3) #set rownya = 3 -> ukuran papan 10x10
                    hasSetMode = True
                if pygame.Rect(halma.col1hitbox).collidepoint(event.pos): #kalo misal rad1hitbox lagi diklik
                    halma.setcolor(1)  #set rownya = 1 -> ukuran papan 8x8
                    hasSetColor = True
                if pygame.Rect(halma.col2hitbox).collidepoint(event.pos):
                    halma.setcolor(2) #set rownya = 2 -> ukuran papan 10x10
                    hasSetColor = True
            if hasSetColor and hasSetRow and hasSetMode: #kalo udah ngesetting
                if event.type == pygame.KEYDOWN: #kalau dia mencet sesuatu
                    if event.key == pygame.K_SPACE: #kalau dia mencet space
                        start = False #biar bisa pindah page
                        bg = pygame.transform.scale(bg1[1], (1280, 720))
                        win.blit(bg, (0,0))
                        # ngeserve background page selanjutnya
                        board = papan(ukuranPapan,ukuranPapan,halma.color,halma.mode)
    else:
        if board.turn == 1 and (board.mode == 1 or board.mode == 2): #and (board.mode == 1 or board.mode == 2) and board.player1 == 1:
            for event in pygame.event.get():
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

                    if pygame.Rect(board.okayhitbox).collidepoint(event.pos):
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
                            #print(board.objective(halma))
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
                                        allmove = possibleMove(board,firstPiece)
                                        for pion in allmove:
                                            print(pion.x,pion.y)
                                else: #kalo udah ada yang diklik

                                    if (firstPiece.owner == board.turn-1 and countLoop > 0 and board.isi[i][j].status == 0): #jika turnnya turn dia, countLoopnya masih ada dan yang diklik kosong
                                        a = math.floor((i + lastX)/2) #bidak musuh
                                        b = math.floor((j + lastY)/2)
                                        c = (i + lastX)/2
                                        d = (j + lastY)/2
                                        #print(lastX,lastY,a,b,c,d)
                                        if not ((firstPiece.camp == 0 and board.isi[i][j].camp == firstPiece.owner+1) or (firstPiece.camp != 0 and board.isi[i][j].camp == 0 and firstPiece.owner+1 != firstPiece.camp)): #Ini biar dia gabisa keluar dari camp musuh kalo udah nyampe
                                            if (cekTetangga(a,b,lastX,lastY) and cekTetangga(i,j,a,b) and (c.is_integer() and d.is_integer()) and (((board.isi[a][b].status == 1) or (board.isi[a][b].status == 3)) and ((board.isi[lastX][lastY].status == 4) or (board.isi[lastX][lastY].status == 2)))):
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
        if board.turn == 2:# and (board.mode == 3 or board.mode == 2): #and (board.mode == 3 or board.mode == 2) and board.player == 2:#(board.mode == 1 or board.mode == 3) and ((board.player1 == 2 and board.turn == 1) or (board.player2 == 2 and board.turn == 2)):
            board = minimax(board,board.turn,1)
            board.changeturn()

    if event.type == pygame.QUIT:
        run = False

    redrawGameWindow() #menggambar ulang window


pygame.quit()
