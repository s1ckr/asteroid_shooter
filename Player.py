import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite, sprite_boost, creation_time=0, W=1000, H=800):
        super().__init__()
        self.original_image = sprite
        self.original_image_boost = sprite_boost
        self.current_image = sprite
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.center = (W // 2, H // 2)
        self.speed = 1
        self.decelerationSpeed = 0.05
        self.turningSpeed = 2
        self.angle = 90
        self.angleRad = math.radians(self.angle)
        self.velocity = 0
        self.lives = 3
        self.score = 0
        self.asteroids_shot = 0
        self.is_alive = True

    def accelerate(self):
        if self.velocity < 3:
            self.velocity += self.speed

    def turnRight(self):
        self.angle -= self.turningSpeed
        self.angle %= 360
        self.rotate_image()
        self.angleRad = math.radians(self.angle)


    def turnLeft(self):
        self.angle += self.turningSpeed
        self.angle %= 360
        self.rotate_image()
        self.angleRad = math.radians(self.angle)

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.current_image, (self.angle + 270)%360)
        self.rect = self.image.get_rect(center=self.rect.center)

    def switch_image_to_boosted(self, to_boosted=False):
        if to_boosted:
            self.current_image = self.original_image_boost
            self.rotate_image()
        else:
            self.current_image = self.original_image
            self.rotate_image()


    def update(self):
        if self.velocity > 0:
            self.velocity -= self.decelerationSpeed
        self.rect.x += self.velocity * math.cos(self.angleRad)
        self.rect.y -= self.velocity * math.sin(self.angleRad)
