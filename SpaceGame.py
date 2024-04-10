import pygame
from Player import Player
from Projectile import Projectile
from Asteroid import Asteroid

pygame.font.init()

W = 1000
H = 750
window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
BACKGROUND_COLOR = (0, 0, 0)


sprite = pygame.transform.scale(pygame.image.load('ship2.png'), (40, 70))
sprite_boost = pygame.transform.scale(pygame.image.load('ship1.png'), (40, 70))
rocket = pygame.transform.scale(pygame.image.load('rocket.png'), (10, 30))
asteroid_sprite = pygame.transform.scale(pygame.image.load('asteroid.png'), (100, 100))
bg = pygame.transform.scale(pygame.image.load('background.png'), (W, H))
go = pygame.transform.scale(pygame.image.load('game_over_2.png'), (W // 2, H // 2))
heart = pygame.transform.scale(pygame.image.load('heart.png'), (40, 40))
restart = pygame.transform.scale(pygame.image.load('restart.png'), (W // 2, H // 8))
font_small = pygame.font.Font("pixel_font.ttf", 50)
font_big = pygame.font.Font("pixel_font.ttf", 100)

asteroid_timer = pygame.time.get_ticks()
asteroid_interval = 3000

projectile_timer = pygame.time.get_ticks()
projectile_interval = 1000


pygame.display.set_caption('Астероиды')


def controls_handler(keys):
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.switch_image_to_boosted(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.switch_image_to_boosted(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spawn_rocket()


    if not game_over:
        if keys[pygame.K_UP]:
            player.accelerate()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()

def spawn_rocket():
    global projectile_timer, projectile_interval
    current_time = pygame.time.get_ticks()

    if current_time - projectile_timer > projectile_interval:
        proj = Projectile(rocket, player.rect.center[0], player.rect.center[1], player.angle)
        projectiles.add(proj)
        all_sprites.add(proj)
        projectile_timer = current_time
def spawn_asteroids():
    global asteroid_timer, asteroid_interval, player
    current_time = pygame.time.get_ticks()

    if current_time - asteroid_timer > asteroid_interval:
        asteroid = Asteroid(asteroid_sprite, player.rect.center[0], player.rect.center[1])
        asteroids.add(asteroid)
        all_sprites.add(asteroid)
        asteroid_timer = current_time

def check_toroidal():
    for obj in all_sprites:
        if obj.rect.center[0] > W:
            obj.rect.x = 0
        elif obj.rect.center[0] < 0:
            obj.rect.x = W - obj.rect.width
        if obj.rect.center[1] > H:
            obj.rect.y = 0
        elif obj.rect.center[1] < 0:
            obj.rect.y = H - obj.rect.height

def check_asteroid_hit(player, asteroids):
    global game_over
    collisions = pygame.sprite.spritecollide(player, asteroids, True)
    for _ in collisions:
        player.lives -= 1
        if player.lives <= 0:
            game_over = True

def check_rocket_hits():
    global player, projectiles, asteroids
    for proj in projectiles:
        did_hit = False
        collisions = pygame.sprite.spritecollide(proj, asteroids, True)
        for _ in collisions:
            player.asteroids_shot += 1
            did_hit = True
        if did_hit:
            proj.kill()

def render_lives():
    num = player.lives
    for i in range(num):
        window.blit(heart, (15+i*55, 15))

def count_score():
    player.score = int(20 * player.asteroids_shot + 5 * (pygame.time.get_ticks() - attempt_start_time) // 1000)

def render_score():
    text = font_small.render(f"Score: {player.score}", True, (255, 255, 255))
    window.blit(text, (W - 200, 15))


def restart_game():
    global player, asteroids, all_sprites, game_over, attempt_start_time, projectiles
    player = Player(sprite, sprite_boost, pygame.time.get_ticks())
    asteroids = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    game_over = False
    attempt_start_time = pygame.time.get_ticks()

def game_cycle():
    global player, asteroids, window
    spawn_asteroids()
    check_toroidal()
    check_asteroid_hit(player, asteroids)
    check_rocket_hits()
    if player.is_alive:
        count_score()
    render_lives()
    render_score()
    all_sprites.draw(window)
    all_sprites.update()


# Главный игровой цикл
player = Player(sprite, sprite_boost, pygame.time.get_ticks())
asteroids = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
attempt_start_time = pygame.time.get_ticks()
game_over = False
running = True


while running:

    keys = pygame.key.get_pressed()
    controls_handler(keys)

    window.blit(bg, (0, 0))

    if not game_over:
        game_cycle()
    else:
        window.blit(go, ((W // 2) - 250, (H // 2) - 250))
        window.blit(restart, ((W // 2) - 250, (H // 2 + 125)))
        text = font_big.render(f"Score: {player.score}", True, (255, 255, 255))
        window.blit(text, (W // 2 - text.get_rect().width // 2, H // 2 + text.get_rect().height // 2 + 15))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()