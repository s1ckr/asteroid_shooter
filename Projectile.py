import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, sprite, pos_x, pos_y, angle, W=1000, H=800):
        super().__init__()
        self.W = W
        self.H = H
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.speed = 5
        self.angle = angle
        self.change_x = self.speed * math.cos(math.radians(self.angle))
        self.change_y = -self.speed * math.sin(math.radians(self.angle))
        self.rotate_image()

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.image, (self.angle + 270)%360)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.center[0] < 0 or self.rect.center[0] > self.W or self.rect.center[1] < 0 or self.rect.center[1] > self.H:
            self.kill()