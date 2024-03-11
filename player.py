import numpy as np
from utils import crossProduct

class player():
    def __init__(self, x, y, zrot, n, r, fov = 90, speed = 10):
        self.pos = [x, y]
        self.zrot = 0
        self.n = n
        self.r = r
        self.fog = self.r
        self.fov = fov
        self.speed = speed
        self.s = []
        self.resetRays()
    
    def resetRays(self):
        self.rays=[]
        for i in range(1, self.n+1):
            rayx = (self.r * np.cos(np.radians((self.fov/2 + self.zrot) - (i * self.fov/self.n)+(self.fov/self.n/2))))
            rayy = (self.r * np.sin(np.radians((self.fov/2 + self.zrot) - (i * self.fov/self.n)+(self.fov/self.n/2))))


            self.rays.append([rayx, rayy])
        
    def transform(self, distance, rot):
        self.zrot = (self.zrot - rot) % 360

        self.pos[0] += np.cos(np.radians(self.zrot)) * distance
        self.pos[1] += np.sin(np.radians(self.zrot)) * distance

        self.resetRays()

    def rayCatch(self, W1, W2):
        scalars = []
        for ray in self.rays:
            p = self.pos
            q = W1

            s = [ray[0], ray[1]]
            r = [W1[0] - W2[0], W1[1] - W2[1]]

            if crossProduct(r, s) == 0:
                continue

            t = crossProduct(np.subtract(q, p), s) / crossProduct(r, s)
            u = crossProduct(np.subtract(p, q), r) / crossProduct(s, r)

            if 0 <= t and t <= 1 and 0 <= u and u <= 1:
                scalars.append(u * self.r)
            else:
                scalars.append(self.r)
        
        return scalars
    
    def wallCatch(self, walls, colisionRadius = 20):

        scalars = [(self.r, (0, 0, 0)) for x in self.rays]
        for count, wall in enumerate(walls):

            newScalars = self.rayCatch((wall[0], wall[1]), (wall[2], wall[3]))

            for index, scalar in enumerate(scalars):
                if scalar[0] > newScalars[index]:
                    scalars[index] = (newScalars[index], wall[4])

        return scalars
    
    def colisionDisplace(self, walls, radius):
        for wall in walls:
            if wall[1] == wall[3]:
                if abs(self.pos[1] - wall[1]) < radius:
                    if (self.pos[0] > wall[0] and self.pos[0] < wall[2]) or (self.pos[0] < wall[0] and self.pos[0] > wall[3]):
                        self.pos[1] += (-1 if self.pos[1] < wall[1] else 1) * abs(radius - abs(self.pos[1] - self.wall[1]))
                
            if wall[0] == wall[2]:
                if abs(self.pos[0] - wall[0]) < radius:
                    if (self.pos[1] > wall[1] and self.pos[1] < wall[3]) or (self.pos[1] < wall[1] and self.pos[1] > wall[3]):
                        self.pos[0] += (-1 if self.pos[0] < wall[0] else 1) * abs(radius - abs(self.pos[0] - self.wall[0]))
