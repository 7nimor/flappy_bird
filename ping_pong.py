import sys
import pygame
import time
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
# GAME NAME
pygame.display.set_caption("Space Dodge")
# IMG
BG = pygame.transform.scale(pygame.image.load("img/bg_night.png"), (WIDTH, HEIGHT))
Floor_IMG = pygame.transform.scale2x(pygame.image.load("img/floor.png"))
Bird_IMG = pygame.transform.scale2x(pygame.image.load("img/red_bird_mid_flap.png"))
Pipe_IMG = pygame.transform.scale2x(pygame.image.load("img/pipe_red.png"))

clock = pygame.time.Clock()

bird_rect = Bird_IMG.get_rect(center=(100, 400))

crete_pipe = pygame.USEREVENT
pygame.time.set_timer(crete_pipe, 1200)


def check_collision(list_pipe):
    for pipe in list_pipe:
        if bird_rect.colliderect(pipe):
            return False
        if bird_rect.top <= -50 or bird_rect.bottom >= 900:
            return False
    return True


def generate_pipe_rect():
    random_pipe = random.randrange(300, 600)
    pipe_rect_top = Pipe_IMG.get_rect(midbottom=(700, random_pipe - 250))
    pipe_rect_down = Pipe_IMG.get_rect(midtop=(700, random_pipe))
    return pipe_rect_down, pipe_rect_top


def move_pipe_rect(lst):
    for l in lst:
        l.centerx -= 5
    inside_pipe = [pipe for pipe in lst if pipe.right > -50]
    return inside_pipe


# def draw(floor_x, pipe_list):


def main(floor_x, bird_movement, game_state, pipe_list):
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
            if event.type == crete_pipe:
                pipe_list.extend(generate_pipe_rect())
        WIN.blit(BG, (0, 0))
        WIN.blit(Floor_IMG, (floor_x, 650))
        WIN.blit(Floor_IMG, (floor_x + 670, 650))

        clock.tick(90)
        if game_state:
            WIN.blit(Bird_IMG, bird_rect)

            # game_state=check_collision(pipe_list)
            game_state = check_collision(pipe_list)
            pipe_list = move_pipe_rect(pipe_list)

            for pipe in pipe_list:
                if pipe.bottom >= 800:
                    WIN.blit(Pipe_IMG, pipe)
                else:
                    revers_img_pipe = pygame.transform.flip(Pipe_IMG, False, True)
                    WIN.blit(revers_img_pipe, pipe)

        bird_movement += gravity
        bird_rect.centery += bird_movement 
        floor_x -= 1
        if floor_x <= -670:
            floor_x = 0
        pygame.display.update()


if __name__ == "__main__":
    main(floor_x, bird_movement, game_state, pipe_list)
