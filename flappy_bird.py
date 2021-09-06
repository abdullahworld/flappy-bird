import pygame 
import sys
import random 



pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()


#Game Variables
gravity = 0.25
bird_movement = 0



bg_surface = pygame.image.load(r"flappy-bird-assets\sprites\background-day.png").convert() #convert allows image to load faster.
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load(r"flappy-bird-assets\sprites\base.png")
floor_surface = pygame.transform.scale2x((floor_surface))
floor_x_pos = 0

bird_surface = pygame.image.load(r"flappy-bird-assets\sprites\bluebird-midflap.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100,512))

pipe_surface = pygame.image.load(r"flappy-bird-assets\sprites\pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_active = True



def create_pipe():

    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return (bottom_pipe, top_pipe)

def move_pipes(pipes):
    for bottom_pipe, top_pipe in pipes:
        bottom_pipe.centerx -= 5
        top_pipe.centerx -= 5

    return pipes

def draw_pipes(pipes):

    for bottom_pipe, top_pipe in pipes:
        flip_surface = pygame.transform.flip(pipe_surface,False, True)
        
        screen.blit(pipe_surface, bottom_pipe)
        screen.blit(flip_surface, top_pipe)



def check_collision(pipes):
    for bottom_pipe, top_pipe in pipes:

        if bird_rect.colliderect(bottom_pipe) or bird_rect.colliderect(top_pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def draw_floor():
    global floor_x_pos

    if floor_x_pos <= -576:
        floor_x_pos = 0
    
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface , (floor_x_pos+ 576,900))


while True:

    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe())
 


    screen.blit(bg_surface, (0,0))

    if game_active:
        #Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)

        #Pipes 
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)

    floor_x_pos -= 1
    draw_floor()

    pygame.display.update()
    clock.tick(120)