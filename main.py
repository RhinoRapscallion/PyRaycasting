import numpy as np
import pygame
from player import player
from mazeGenerater import maze

RESOLUTION = (800, 600)
pygame.init()

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
playing = True

player = player(250, 100, 0, int(RESOLUTION[0]/10), 6000, fov = 60, speed = 20)

control = [0, 0]

#walls = [
#    [100, 100, 100, 5000, (0, 255, 0)],
#    [100, 5000, 5000, 5000, (255, 0, 0)],
#    [5000, 5000, 5000, 100, (0, 255, 0)],
#    [5000, 100, 100, 100, (0, 0, 255)],
#    [500, 100, 500, 500, (0, 255, 255)],
#    [3000, 3000, 5000, 3000, (0, 255, 255)]
#]

walls = maze(10, 10, 500)
print(len(walls))

delta = RESOLUTION[0] / len(player.rays)

while playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                control[0] = -player.speed
            
            if event.key == pygame.K_DOWN:
                control[0] = player.speed
            
            if event.key == pygame.K_RIGHT:
                control[1] = 5
            
            if event.key == pygame.K_LEFT:
                control[1] = -5
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and control[0] < 0:
                control[0] = 0
            
            if event.key == pygame.K_DOWN and control[0] > 0:
                control[0] = 0
            
            if event.key == pygame.K_RIGHT and control[1] > 0:
                control[1] = 0
            
            if event.key == pygame.K_LEFT and control[1] < 0:
                control[1] = 0

    player.transform(control[0], control[1])
    player.colisionDisplace(walls, 10)

    screen.fill((0, 0, 0))

    raycast = enumerate(player.wallCatch(walls))
    for count, catch in raycast:
        height = RESOLUTION[1] / ((catch[0] * np.cos(np.radians(-player.fov/2 + (count * player.fov/player.n))))) * (5000 / 6)
        
        pygame.draw.rect(screen, np.multiply(catch[1], 1 - (catch[0] / player.fog)), ((count * delta), RESOLUTION[1]/2 - height/2, delta, height))
    
    #for wall in walls:
    #    pygame.draw.line(screen, wall[4], (wall[0], wall[1]),(wall[2], wall[3]), 5)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()