import pygame 
import sys
import random 

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04b_19.ttf" , 40)

#Game Variables
gravity = 0.3
bird_movement = 0

bg_surface = pygame.image.load(r"black_288.png").convert() #convert allows image to load faster.
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("base.png")
floor_surface = pygame.transform.scale2x((floor_surface))
floor_x_pos = 0


def changeColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage
# bird_upflap = pygame.transform.scale2x(pygame.image.load(r"flappy-bird-assets\sprites\bluebird-upflap.png").convert_alpha())
# bird_downflap = pygame.transform.scale2x(pygame.image.load(r"flappy-bird-assets\sprites\bluebird-downflap.png").convert_alpha())
# bird_midflap = pygame.transform.scale2x(pygame.image.load(r"flappy-bird-assets\sprites\bluebird-midflap.png").convert_alpha())

color = pygame.Color(0, 0, 255)
# bird_midflap = changeColor(bird_midflap, color)
# bird_upflap = changeColor(bird_upflap,color)
# bird_downflap = changeColor(bird_downflap, color)



# bird_midflap = pygame.image.load(r"flappy-bird-assets\sprites\bluebird-downflap.png")
# bird_colored = pygame.Surface(bird.get_size()).convert_alpha()
# bird_colored.fill((255,255,255))
# bird_midflap.blit(bird_colored, )
#bird_frames[bird_index]

# bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface_nocolor = pygame.image.load("black_white.png")
bird_rect = bird_surface_nocolor.get_rect(center=(100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer (BIRDFLAP, 200)


color =  pygame.Color(255,0,0)
pipe_surface_nocolor = pygame.image.load(r"pipe-white.png")
pipe_surface_nocolor = pygame.transform.scale2x(pipe_surface_nocolor)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_active = "start"
score = -1
high_score = 0



#Takes rectangle's size, position and a point. Returns true if that
#point is inside the rectangle and false if it isnt.
def pointInRectanlge(px, py, rw, rh, rx, ry):
    if px > rx and px < rx  + rw:
        if py > ry and py < ry + rh:
            return True
    return False

class Slider:
    def __init__(self, position:tuple, upperValue:int=255, sliderWidth:int = 30, text:str="Editing features for simulation",
                 outlineSize:tuple=(300, 100))->None:
        self.position = position
        self.outlineSize = outlineSize
        self.text = text
        self.sliderWidth = sliderWidth
        self.upperValue = upperValue
        
    #returns the current value of the slider
    def getValue(self)->float:
        return self.sliderWidth / (self.outlineSize[0] / self.upperValue)

    #renders slider and the text showing the value of the slider
    def render(self, display:pygame.display)->None:
        #draw outline and slider rectangles
        pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1], 
                                              self.outlineSize[0], self.outlineSize[1]), 3)
        
        pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1], 
                                              self.sliderWidth, self.outlineSize[1] - 10))

        #determite size of font
        self.font = pygame.font.Font(pygame.font.get_default_font(), int((15/100)*self.outlineSize[1]))

        #create text surface with value
        valueSurf = self.font.render(f"{self.text}: {round(self.getValue())}", True, (255, 0, 0))
        
        #centre text
        textx = self.position[0] + (self.outlineSize[0]/2) - (valueSurf.get_rect().width/2)
        texty = self.position[1] + (self.outlineSize[1]/2) - (valueSurf.get_rect().height/2)

        display.blit(valueSurf, (textx, texty))

    #allows users to change value of the slider by dragging it.
    def changeValue(self)->None:
        #If mouse is pressed and mouse is inside the slider
        mousePos = pygame.mouse.get_pos()
        if pointInRectanlge(mousePos[0], mousePos[1]
                            , self.outlineSize[0], self.outlineSize[1], self.position[0], self.position[1]):
            if pygame.mouse.get_pressed()[0]:
                #the size of the slider
                self.sliderWidth = mousePos[0] - self.position[0]

                #limit the size of the slider
                if self.sliderWidth < 1:
                    self.sliderWidth = 0
                if self.sliderWidth > self.outlineSize[0]:
                    self.sliderWidth = self.outlineSize[0]

slider1 = Slider((100,100))
slider2 = Slider((100,200))


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

def rotate_bird(bird):

    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)

    return new_bird 

# def bird_animation():

#     #new_bird = bird_frames[bird_index]
#     #new_bird = 
#     #new_bird_rect = new_bird.get_rect(center= (100, bird_rect.centery))

#     return new_bird, new_bird_rect

def score_display(game_state):

    
    if score < 0:
        display_score = 0
    else:
        display_score = score
    
    if game_state == 'main_game':
        score_surface = game_font.render(f"score {str(display_score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f"score {str(display_score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {str(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(288, 200))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    
    return high_score

while True:

    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and (game_active == False or game_active =='start'):
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = -1

        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe())
            if game_active == True:
                score += 1
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

              


    screen.blit(bg_surface, (0,0))

    if game_active == "start":
        slider1.render(screen)
        slider1.changeValue()

        slider2.render(screen)
        slider2.changeValue()

        r = int(slider1.getValue())
        b = int(slider2.getValue())

        color_pipe =  pygame.Color(r,0,0)
        color_bird = pygame.Color(0,0,b)

        bird_surface = changeColor(bird_surface_nocolor, color_bird)
        pipe_surface = changeColor(pipe_surface_nocolor, color_pipe)

        bird_rect = bird_surface.get_rect(center=(100,512))
        screen.blit(bird_surface, bird_rect)

        bottom_pipe = pipe_surface.get_rect(midtop = (200, 400))
        screen.blit(pipe_surface, bottom_pipe)
        

    if game_active and game_active != 'start':
        #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        #Pipes 
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)

        score_display('main_game') 
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')


    floor_x_pos -= 1
    draw_floor()

    pygame.display.update()
    clock.tick(120)