import pygame
import object
import random
import sys
import math

"""皆為整數"""
screenWidth = 1400
screenlength = 800
sightOpen = False
fps = 100
centerX = screenWidth//2
centerY = screenlength//2
sensitivityClose = 1
sensitivityOpen = 1
magnification = 2

"""產生標靶"""
def initCircleObject(t):
    global sightOpen
    global fps
    global magnification
    if sightOpen:
        r = random.randrange(10*magnification, 20*magnification)
        r1 = int(r/2)
        r2 = int(r1/2)
        x = random.randrange(r+100*magnification, (screenWidth-100)*magnification-r)
        y = random.randrange(r+50*magnification, (screenlength-50)*magnification-r)
        xs = random.randrange(-2*magnification, 2*magnification)
        ys = random.randrange(-2*magnification, 2*magnification)
    else:
        r = random.randrange(10, 20)
        r1 = int(r/2)
        r2 = int(r1/2)
        x = random.randrange(r+100, screenWidth-r-100)
        y = random.randrange(r+50, screenlength-r-50)
        xs = random.randrange(-2, 2)
        ys = random.randrange(-2, 2)
    return object.Circle((x, y), r, r1, r2, xs, ys, t)

def main():
    global screenWidth
    global screenlength
    global sightOpen
    global fps
    global centerX
    global centerY
    global sensitivityClose
    global sensitivityOpen
    global magnification
    pygame.init()
    objects = []
    Fonts = []
    screen = pygame.display.set_mode((screenWidth,screenlength))
    pygame.display.set_caption("test")
    smallfont = pygame.font.Font(None, 24)
    font = pygame.font.Font(None, 36)
    bigfont = pygame.font.Font(None, 108)
    pyGameOver = bigfont.render("Game Over", True, (255, 0, 0))
    pyGameStart1 = bigfont.render("Press \"space\" to start", True, (122, 122, 0))
    pyGameStart2 = bigfont.render("Press \"esc\" to end game", True, (122,122, 0))
    pyGameStart3 = bigfont.render("Press \"r\" to restart", True, (122, 122, 0))
    pyMiss = smallfont.render("miss", True, (255, 0, 0))
    pyScore = smallfont.render("score", True, (0, 255, 0))
    """420"""
    sightImage = pygame.image.load("./image/sight.png")
    """3000"""
    sniperSightImage = pygame.image.load("./image/sniper_sight2_black2_3000.png")
    s = 0
    score = 0
    failtimes = 0
    clock = pygame.time.Clock()
    missTarget = 0
    start = True
    running = True
    while start:
        clock.tick(10)
        screen.fill((255,255,255))
        screen.blit(pyGameStart1, (250, 300))
        screen.blit(pyGameStart2, (250, 380))
        screen.blit(pyGameStart3, (250, 460))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        pygame.display.flip()
    """游標遮蔽"""
    pygame.mouse.set_visible(True)
    mousePosition = pygame.mouse.get_pos()
    positionX = centerX
    positionY = centerY
    initime = pygame.time.get_ticks()/1000
    while running:
        clock.tick(fps)
        now = pygame.time.get_ticks()/1000 - initime
        mousePosition = pygame.mouse.get_pos()
        x = mousePosition[0]
        y = mousePosition[1]
        distanceX = x - centerX
        distanceY = y - centerY
        """開鏡設定"""
        if pygame.mouse.get_pressed()[2] and sightOpen == False:
            print(1)
            sightOpen = True
            for i in objects:
                i.sightOpenMode(positionX, positionY, magnification)
        """關鏡設定"""
        if pygame.mouse.get_pressed()[2] == False and sightOpen == True:
            print(0)
            sightOpen = False
            for i in objects:
                i.sightCloseMode(positionX, positionY, magnification)
        screen.fill((0,0,0))
        if sightOpen:
            pygame.draw.rect(screen, (255,255,255), (centerX-positionX*magnification, centerY-positionY*magnification, screenWidth*magnification, screenlength*magnification))
        else:
            pygame.draw.rect(screen, (255,255,255), (centerX-positionX, centerY-positionY, screenWidth, screenlength))
        for i in objects:
            """物件存活時間檢測"""
            if now - i.t >= 100:
                objects.remove(i)
                missTarget += 1
            if i != None:
                """物件隨機停或動"""
                if random.random() >= 0.02:
                    i.move()
                elif i.stop == 0:
                    i.stop = 20
                if i.stop:
                    i.stop -= 1
                pygame.draw.circle(screen, (100,100,100), (i.x-positionX+centerX, i.y-positionY+centerY), i.r)
                pygame.draw.circle(screen, (150,100,100), (i.x-positionX+centerX, i.y-positionY+centerY), i.r1)
                pygame.draw.circle(screen, (255,100,100), (i.x-positionX+centerX, i.y-positionY+centerY), i.r2)
                """物件離開範圍"""
                if (i.outofscreen(screenWidth, screenlength) and sightOpen == False):
                    objects.remove(i)
                    missTarget += 1
        if now > 1:
            if sightOpen:
                positionX += math.floor(distanceX * sensitivityOpen)
                positionY += math.floor(distanceY * sensitivityOpen)
            else:
                positionX += math.floor(distanceX * sensitivityClose)
                positionY += math.floor(distanceY * sensitivityClose)
        """使用者輸入設定"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_s:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                hitAnyTargets = False
                for i in objects:
                    a = i.onRange(positionX, positionY)
                    if a:
                        score += a
                        hitAnyTargets = True
                        objects.remove(i)
                        Fonts.append(object.Font(pyScore, centerX, centerY))
                if hitAnyTargets == False:
                    failtimes += 1
                    Fonts.append(object.Font(pyMiss, centerX, centerY))
        """每一秒產生"""
        if now - s >= 1 and now<=10:
            s += 1
            objects.append(initCircleObject(now))
        """每一偵產生"""
        pyscore = font.render("Score: " + str(score), True, (0, 0, 0))
        pyfailtimes = font.render("Failtimes: " + str(failtimes), True, (0,0,0) )
        pymissTarget = font.render("MissTargets:" + str(missTarget), True, (0,0,0))
        pytime = smallfont.render(str(now), True, (255, 0, 0))
        screen.blit(pyscore, (0,0))
        screen.blit(pyfailtimes, (0,30))
        screen.blit(pymissTarget, (0,60))
        screen.blit(pytime, (screenWidth-50, 0))
        for i in Fonts:
            if i != None:
                screen.blit(i.font, (i.x, i.y))
                i.move()
                if i.t <= 0:
                    Fonts.remove(i)
        pygame.mouse.set_pos(centerX, centerY)
        if sightOpen:
            screen.blit(sniperSightImage, (centerX-1500,centerY-1500))
        else:
            screen.blit(sightImage, (centerX-210,centerY-210))
        pygame.display.flip()
        """time over"""
        if now >= 12:
            print(score)
            print(failtimes)
            print(missTarget)
            pygame.mouse.set_visible(True)
            running = False
    while True:
        clock.tick(1)
        screen.fill((255,255,255))
        screen.blit(pyscore, (0,0))
        screen.blit(pyfailtimes, (0,30))
        screen.blit(pymissTarget, (0,60))
        screen.blit(pyGameOver, (380, 350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    main()


if __name__ == "__main__":
    main()
