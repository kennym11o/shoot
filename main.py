import pygame
import object
import random
import sys

screenWidth = 800
screenlength = 600

def initCircleObject():
    r = random.randrange(30, 50)
    r1 = int(r/2)
    r2 = int(r1/2)
    x = random.randrange(r, screenWidth-r)
    y = random.randrange(r, screenlength-r)
    xs = random.randrange(-3, 3)
    ys = random.randrange(-3, 3)
    return object.Circle((x, y), r, r1, r2, xs, ys)

def main():
    pygame.init()
    objects = []
    screen = pygame.display.set_mode((screenWidth,screenlength))
    pygame.display.set_caption("test")
    font = pygame.font.Font(None, 36)
    cursorImage = pygame.image.load("./image/cursor2.png")
    s = 0
    score = 0
    failtimes = 0
    clock = pygame.time.Clock()
    times = 0
    missTarget = 0
    pygame.mouse.set_visible(False)
    fps = 100
    while True:
        clock.tick(fps)
        times += 1
        s = times/fps
        screen.fill((255,255,255))
        for i in objects:
            i.t -= 1
            if i.t == 0:
                objects.remove(i)
                missTarget += 1
            if i != None:
                if random.random() >= 0.02:
                    i.move()
                elif i.stop == 0:
                    i.stop = 20
                if i.stop:
                    i.stop -= 1
                pygame.draw.circle(screen, (100,100,100), i.pos, i.r)
                pygame.draw.circle(screen, (150,100,100), i.pos, i.r1)
                pygame.draw.circle(screen, (200,100,100), i.pos, i.r2)
                if i.outofscreen(screenWidth, screenlength):
                    objects.remove(i)
                    missTarget += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_SPACE:
                    hitAnyTargets = False
                    position = pygame.mouse.get_pos()
                    for i in objects:
                        a = i.onRange(position[0], position[1])
                        if a:
                            score += a
                            hitAnyTargets = True
                            objects.remove(i)
                    if hitAnyTargets == False:
                        failtimes += 1
                if event.key == pygame.K_s:
                    s = 20
            if event.type == pygame.MOUSEBUTTONDOWN:
                hitAnyTargets = False
                position = pygame.mouse.get_pos()
                for i in objects:
                    a = i.onRange(position[0], position[1])
                    if a:
                        score += a
                        hitAnyTargets = True
                        objects.remove(i)
                if hitAnyTargets == False:
                    failtimes += 1

        #每一秒產生
        if times % fps == 0:
            objects.append(initCircleObject())
        if s >= 5:
            if (times + fps/2) % 50 == 0:
                 objects.append(initCircleObject())

        pyscore = font.render("Score: " + str(score), True, (0, 0, 0))
        pyfailtimes = font.render("Failtimes: " + str(failtimes), True, (0,0,0) )
        pymissTarget = font.render("MissTargets:" + str(missTarget), True, (0,0,0))
        screen.blit(pyscore, (0,0))
        screen.blit(pyfailtimes, (0,30))
        screen.blit(pymissTarget, (0,60))
        screen.blit(cursorImage, (pygame.mouse.get_pos()[0]-50,pygame.mouse.get_pos()[1]-50))
        pygame.display.flip()
        #時間到
        if s >= 10:
            print(score)
            print(failtimes)
            print(missTarget)
            while True:
                clock.tick(1)
                screen.fill((255,255,255))
                screen.blit(pyscore, (0,0))
                screen.blit(pyfailtimes, (0,30))
                screen.blit(pymissTarget, (0,60))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()
                        if event.key == pygame.K_r:
                            main()


if __name__ == "__main__":
    main()
