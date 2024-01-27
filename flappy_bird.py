import sys
import pygame
import random

pygame.init()
# Variable
WIDTH, HEIGHT = 500, 800
floor_x = 0
gravity = 0.25
bird_movement = 0
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pipe_list = []
game_state = True
bird_index = 0
score = 0
high_score = 0
active_score = True
# GAME NAME
pygame.display.set_caption("Space Dodge")
# IMG
BG = pygame.transform.scale(pygame.image.load("img/bg_night.png"), (WIDTH, HEIGHT))
Floor_IMG = pygame.transform.scale2x(pygame.image.load("img/floor.png"))
Pipe_IMG = pygame.transform.scale2x(pygame.image.load("img/pipe_red.png"))
Bird_mid_IMG = pygame.transform.scale2x(pygame.image.load("img/red_bird_mid_flap.png"))
Bird_up_IMG = pygame.transform.scale2x(pygame.image.load("img/red_bird_up_flap.png"))
Bird_down_IMG = pygame.transform.scale2x(pygame.image.load("img/red_bird_down_flap.png"))

game_font = pygame.font.Font('font/Flappy.TTF', 30)

bird_list = [Bird_mid_IMG, Bird_up_IMG, Bird_down_IMG]

Bird_IMG = bird_list[bird_index]
clock = pygame.time.Clock()

bird_rect = Bird_IMG.get_rect(center=(100, 400))

crete_pipe = pygame.USEREVENT
create_bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_bird_flap, 100)
pygame.time.set_timer(crete_pipe, 1200)


def generate_pipe_rect():
    random_pipe = random.randrange(300, 600)
    pipe_rect_top = Pipe_IMG.get_rect(midbottom=(700, random_pipe - 250))
    pipe_rect_down = Pipe_IMG.get_rect(midtop=(700, random_pipe))
    return pipe_rect_down, pipe_rect_top


def check_collision(list_pipe):
    global active_score
    for pipe in list_pipe:
        if bird_rect.colliderect(pipe):
            active_score = True
            return False
        if bird_rect.top <= -50 or bird_rect.bottom >= 900:
            active_score = True
            return False
    return True


def move_pipe_rect(lst):
    for l in lst:
        l.centerx -= 5
    inside_pipe = [pipe for pipe in lst if pipe.right > -50]
    return inside_pipe


def get_bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def display_score(state):
    test1 = game_font.render(str(score), True, (255, 255, 255, 0))
    test1_rect = test1.get_rect(center=(250, 80))
    test2 = game_font.render(f'High Score:{high_score}', False, (255, 255, 255))
    test2_rect = test1.get_rect(center=(170, 600))
    if state == 'active':
        WIN.blit(test1, test1_rect)
    else:
        WIN.blit(test1, test1_rect)
        WIN.blit(test2, test2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                score += 1
                active_score = False
            if pipe.centerx < 0:
                active_score = True

    if score > high_score:
        high_score = score
    return high_score


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_r and game_state == False:
                game_state = True
                pipe_list.clear()
                bird_rect.center = (100, 400)
                bird_movement = 0
                score = 0

        if event.type == crete_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == create_bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            Bird_IMG, bird_rect = get_bird_animation()
    WIN.blit(BG, (0, 0))
    WIN.blit(Floor_IMG, (floor_x, 650))
    WIN.blit(Floor_IMG, (floor_x + 670, 650))

    clock.tick(90)
    if game_state:
        WIN.blit(Bird_IMG, bird_rect)
        game_state = check_collision(pipe_list)
        pipe_list = move_pipe_rect(pipe_list)

        for pipe in pipe_list:
            if pipe.bottom >= 800:
                WIN.blit(Pipe_IMG, pipe)
            else:
                revers_img_pipe = pygame.transform.flip(Pipe_IMG, False, True)
                WIN.blit(revers_img_pipe, pipe)
        update_score()
        display_score('active')
    else:
        display_score('game_over')

    bird_movement += gravity
    bird_rect.centery += bird_movement
    floor_x -= 1
    if floor_x <= -670:
        floor_x = 0
    pygame.display.update()