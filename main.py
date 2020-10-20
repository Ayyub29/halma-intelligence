import pygame
import time
import math
from papan import cellboard, papan, startstate

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

                if pygame.Rect(board.okayhitbox).collidepoint(event.pos): #Okay hitbox
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
                        print(halma.win(board))
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
