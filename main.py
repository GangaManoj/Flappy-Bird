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

def check_collision(pipes):
    for pipe in pipes:
        if pipe.colliderect(bird_rect):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 520:
            return False
    return True

def rotate_bird(bird):
    rotated_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return rotated_bird

def animate_bird():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (75, bird_rect.centery))
    return new_bird, new_bird_rect

def display_score(game_state):
    if game_state == "playing":
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (200, 100))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f"Score: {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (200, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255,255,255))
        hight_score_rect = high_score_surface.get_rect(center = (200, 480))
        screen.blit(high_score_surface, hight_score_rect)

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((400,600))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

#game variables
gravity = 0.12
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (400,600))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (400,80))
floor_x = 0

bird_downflap = pygame.transform.scale(pygame.image.load('assets/bluebird-downflap.png').convert_alpha(), (50,35))
bird_midflap = pygame.transform.scale(pygame.image.load('assets/bluebird-midflap.png').convert_alpha(), (50,35))
bird_upflap = pygame.transform.scale(pygame.image.load('assets/bluebird-upflap.png').convert_alpha(), (50,35))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (75,300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (70,420))
pipe_list = []
pipe_height = [450, 350, 250]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (200,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_RETURN and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (75,300)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = animate_bird()
    
    screen.blit(bg_surface, (0,0))

    if game_active:
        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #score
        display_score('playing')
        score += 0.01
    else:
        high_score = update_high_score(score, high_score)
        display_score('game_over')
        screen.blit(game_over_surface, game_over_rect)

    # floor
    draw_floor()
    floor_x -= 1
    if floor_x <= -400:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)