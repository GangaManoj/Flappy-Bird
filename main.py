import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x,520))
    screen.blit(floor_surface, (floor_x + 400,520))

def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop =(500, random_pipe_height))
    bottom_pipe = pipe_surface.get_rect(midbottom =(500, random_pipe_height-200))
    return (top_pipe, bottom_pipe)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)

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

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (70,420))
pipe_list = []
pipe_height = [450, 350, 250]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird_movement = 0
                bird_movement -= 5
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    
    screen.blit(bg_surface, (0,0))

    # bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    # pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # floor
    draw_floor()
    floor_x -= 1
    if floor_x <= -400:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)