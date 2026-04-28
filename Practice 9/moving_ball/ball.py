import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
fon = (255, 255 ,255)
screen.fill(fon)
isDone = True
mainCoordX = 250
mainCoordY = 250

while isDone:
    screen.fill(fon)
    pygame.draw.circle(screen, 'Red', (mainCoordX, mainCoordY), 25)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDone = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainCoordY - 20 - 25 >= 0:
                    mainCoordY -= 20
            if event.key == pygame.K_DOWN:
                if mainCoordY + 20 + 25 <= 500:
                    mainCoordY += 20
            if event.key == pygame.K_RIGHT:
                if mainCoordX + 20 + 25 <= 500:
                    mainCoordX += 20
            if event.key == pygame.K_LEFT:
                if mainCoordX - 20 - 25 >= 0:
                    mainCoordX -= 20
