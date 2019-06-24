import pygame
import object
import random
import sys
import pyautogui

"""皆為整數"""
screenWidth = 1400
screenlength = 800
sightOpen = False
fps = 50
centerX = 1000
centerY = 500
sensitivityClose = 1
sensitivityOpen = 4
magnification = 4

"""產生標靶"""
def initCircleObject():
    global sightOpen
    global fps
    global magnification
    if sightOpen:
        r = random.randrange(10*magnification, 20*magnification)
        r1 = int(r/2)
        r2 = int(r1/2)
        x = random.randrange(r+100*magnification, screenWidth-r-100*magnification)
        y = random.randrange(r+50*magnification, screenlength-r-50*magnification)
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
    return object.Circle((x, y), r, r1, r2, xs, ys, 3*fps)

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
    screen = pygame.display.set_mode((screenWidth,screenlength))
    pygame.display.set_caption("test")
    smallfont = pygame.font.Font(None, 24)
    font = pygame.font.Font(None, 36)
    bigfont = pygame.font.Font(None, 108)
    pyGameOver = bigfont.render("Game Over", True, (255, 0, 0))
    pyGameStart1 = bigfont.render("Press \"space\" to start", True, (122, 122, 0))
    pyGameStart2 = bigfont.render("Press \"esc\" to end game", True, (122,122, 0))
    pyGameStart3 = bigfont.render("Press \"r\" to restart", True, (122, 122, 0))
    """420"""
    sightImage = pygame.image.load("./image/sight.png")
    """3000"""
    sniperSightImage = pygame.image.load("./image/sniper_sight2_black2_3000.png")
    s = 0
    score = 0
    failtimes = 0
    clock = pygame.time.Clock()
    times = 0
    missTarget = 0
    start = False
    while True:
        clock.tick(10)
        screen.fill((255,255,255))
        screen.blit(pyGameStart1, (250, 300))
        screen.blit(pyGameStart2, (250, 380))
        screen.blit(pyGameStart3, (250, 460))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        if start == True:
            break
        pygame.display.flip()
    """游標遮蔽"""
    pygame.mouse.set_visible(False)
    positionX = pyautogui.position()[0]
    positionY = pyautogui.position()[1]
    while True:
        clock.tick(fps)
        pyautogui.moveTo(centerX, centerY)
        pyautogui.PAUSE = fps/1000
        times += 1
        s = times//fps
        mousePosition = pyautogui.position()
        x = int(mousePosition[0])
        y = int(mousePosition[1])
        distanceX = x - centerX
        distanceY = y - centerY


        """開鏡設定"""
        if pygame.mouse.get_pressed()[2] and sightOpen == False:
            print(1)
            sightOpen = True
            screenWidth *= magnification
            screenlength *= magnification
            for i in objects:
                i.sightOpenMode(positionX, positionY, magnification)
        """關鏡設定"""
        if pygame.mouse.get_pressed()[2] == False and sightOpen == True:
            print(0)
            sightOpen = False
            screenWidth /= magnification
            screenlength /= magnification
            for i in objects:
                i.sightCloseMode(positionX, positionY, magnification)
        screen.fill((255,255,255))
        for i in objects:
            """物件存活時間檢測"""
            i.t -= 1
            if i.t == 0:
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
                pygame.draw.circle(screen, (100,100,100), (i.x, i.y), i.r)
                pygame.draw.circle(screen, (150,100,100), (i.x, i.y), i.r1)
                pygame.draw.circle(screen, (255,100,100), (i.x, i.y), i.r2)
                """物件離開範圍"""
                if i.outofscreen(screenWidth, screenlength) and sightOpen == False:
                    objects.remove(i)
                    missTarget += 1
        if sightOpen:
            positionX += distanceX * sensitivityOpen
            positionY += distanceY * sensitivityOpen
        else:
            positionX += distanceX * sensitivityClose
            positionY += distanceY * sensitivityClose
        """使用者輸入設定"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    main()
                    screenWidth = 1400
                    screenlength = 800
                if event.key == pygame.K_s:
                    s = 20
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                hitAnyTargets = False
                for i in objects:
                    a = i.onRange(positionX, positionY)
                    if a:
                        score += a
                        hitAnyTargets = True
                        objects.remove(i)
                if hitAnyTargets == False:
                    failtimes += 1

        """每一秒產生"""
        if times % fps == 0 and s<=9:
            objects.append(initCircleObject())
        """每一偵產生"""
        pyscore = font.render("Score: " + str(score), True, (0, 0, 0))
        pyfailtimes = font.render("Failtimes: " + str(failtimes), True, (0,0,0) )
        pymissTarget = font.render("MissTargets:" + str(missTarget), True, (0,0,0))
        pytime = smallfont.render(str(s), True, (255, 0, 0))
        screen.blit(pyscore, (0,0))
        screen.blit(pyfailtimes, (0,30))
        screen.blit(pymissTarget, (0,60))
        screen.blit(pytime, (screenWidth-50, 0))
        if sightOpen:
            screen.blit(sniperSightImage, (positionX-1500,positionY-1500))
        else:
            screen.blit(sightImage, (positionX-210,positionY-210))

        pygame.display.flip()
        """time over"""
        if s >= 10:
            print(score)
            print(failtimes)
            print(missTarget)
            pygame.mouse.set_visible(True)
            break
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
                    screenWidth = 1400
                    screenlength = 800


if __name__ == "__main__":
    main()
