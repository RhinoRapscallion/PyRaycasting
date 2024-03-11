from random import shuffle, randrange, choice
import numpy as np

def maze(width, height, wall_width):
    cells = ['' for x in range(width * height)]
    
    go = True
    selected = 0 #randrange(0, len(cells))
    cells[selected] = 'c'
    neighbors = []

    while go:
        if selected % width > 0:          neighbors.append([selected - 1, selected, 'e'])
        if selected % width < height - 1: neighbors.append([selected + 1, selected, 'w'])
        if selected / width > 1:          neighbors.append([selected - height, selected, 's'])
        if selected / width < height - 1: neighbors.append([selected + height, selected, 'n'])

        shuffle(neighbors)

        while True:
            if cells[neighbors[0][0]] == '':
                selected = neighbors[0][0]
                oDir = ''
                if neighbors[0][2] == 'n': oDir = 's'
                if neighbors[0][2] == 's': oDir = 'n'
                if neighbors[0][2] == 'w': oDir = 'e'
                if neighbors[0][2] == 'e': oDir = 'w'

                cells[neighbors[0][0]] = cells[neighbors[0][0]] + neighbors[0][2]
                cells[neighbors[0][1]] = cells[neighbors[0][1]] + oDir
                neighbors.pop(0)
                break
            else:
                neighbors.pop(0)
            
            if len(neighbors) < 1:
                go = False
                break
    
    walls = []
    for index, cell in enumerate(cells):
        x1 = (index % width) * wall_width
        y1 = int(index / width) * wall_width
        x2 = x1 + wall_width
        y2 = y1 + wall_width
        color = (128, 128, 255)

        if not 'n' in  cell and not index == 0:
            if not [x1, y1, x2, y1, color] in walls:
                walls.append([x1, y1, x2, y1, color])

        if not 'e' in cell:
            if not [x2, y1, x2, y2, color] in walls:
                walls.append([x2, y1, x2, y2, color])

        if not 's' in cell and not index == len(cells) - 1:
            if not [x1, y2, x2, y2, color] in walls:
                walls.append([x1, y2, x2, y2, color])

        if not 'w' in cell:
            if not [x1, y1, x1, y2, color] in walls:
                walls.append([x1, y1, x1, y2, color])

    combine = True
    nwalls = walls
    while combine:
        combine = False
        for wall in walls:
            for cwall in walls:
                if wall == cwall: continue

                if [wall[2], wall[3]] == [cwall[0], cwall[1]]:
                    if wall[0] == wall[2] and cwall[0] == cwall[2]:
                        nwalls.append([wall[0], wall[1], cwall[2], cwall[3], wall[4]])
                        walls.remove(wall)
                        walls.remove(cwall)
                        combine=True

                    if wall[1] == wall[3] and cwall[1] == cwall[3]:
                        nwalls.append([wall[0], wall[1], cwall[2], cwall[3], wall[4]])
                        walls.remove(wall)
                        walls.remove(cwall)
                        combine=True
        walls = nwalls
    return walls
    
#print(maze(4, 4, 0))