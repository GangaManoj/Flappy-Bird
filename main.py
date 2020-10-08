import pygame, sys

def draw_floor():
    screen.blit(floor_surface, (floor_x,520))
    screen.blit(floor_surface, (floor_x + 400,520))

pygame.init()
screen = pygame.display.set_mode((400,600))
clock = pygame.time.Clock()

#game variables
gravity = 0.12
bird_movement = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (400,600))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (400,80))
floor_x = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale(bird_surface, (50,35))
bird_rect = bird_surface.get_rect(center = (75,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird_movement = 0
                bird_movement -= 5

    screen.blit(bg_surface, (0,0))
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    draw_floor()
    floor_x -= 1
    if floor_x <= -400:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)