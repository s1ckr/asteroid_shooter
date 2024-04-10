import pygame
import random
import math



class Asteroid(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, W=1000, H=800):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, W)
        self.rect.y = random.randint(0, H)
        while math.sqrt(math.pow(x - self.rect.x, 2) + math.pow(y - self.rect.y, 2)) < 250:
            self.rect.x = random.randint(0, W)
            self.rect.y = random.randint(0, H)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)

        while abs(self.speed_x) + abs(self.speed_y) < 1.5 or abs(self.speed_x) + abs(self.speed_y) > 4.5:
            self.speed_x = random.uniform(-3, 3)
            self.speed_y = random.uniform(-3, 3)


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y