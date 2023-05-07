import pygame
from pygame import mixer 
pygame.init()
screen_width,screen_height = 600,600 
screen = pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption('Pong')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FPS = 60 
black = (0,0,0)
white = (255,255,255)
pts_win = 5
PADDLE_WIDTH , PADDLE_HEIGHT = 10,150
""" creating a class called paddle where all the attributes of the class can be accessed
 this class stores all the attributes required for a paddle like its position and its colour etc 
 draw_paddle is a function which is to be performed on a paddle(to draw a paddle), into which we pass the attributes of a paddle"""
class Paddles:
    y_change = 8
    def __init__(self,x,y,paddle_wt,paddle_ht):
        self.x = x
        self.y = y
        self.paddle_wt = paddle_wt
        self.paddle_ht = paddle_ht
        self.colour = white
        self.score=0
        y_change = 8

    def draw_paddle(self,screen):
        pygame.draw.rect(screen,self.colour,(self.x,self.y,self.paddle_wt,self.paddle_ht)) # function that draws a rectangle with the given inputs 

    def movement(self,up):
        if up:
            self.y-=self.y_change 
        else:
            self.y+=self.y_change

# comes up with all the drawings in the screen
def draw_in_screen(screen,paddle_list,ball):
    screen.fill(black)
    for paddle_from_paddle_list in paddle_list:
        paddle_from_paddle_list.draw_paddle(screen)# extracts each paddle from paddle_list and performs draw_paddle which is an attribute of class Paddles
    # draws dashes in the centre of the screen 
    for i in range(10,screen_height,screen_height//20):
        pygame.draw.rect(screen,white,((screen_width-PADDLE_WIDTH)//2,i,2,15))
    ball.draw_ball(screen)# draws the ball
    pygame.display.update()


# function that handles all the paddle movement 
""" here each paddle has an attribute called movement, so for example if 'w' is pressed then the conditions give true for 
key[pygame.K_w] as true , here movement function has 2 parameters one is self and other is up, this self points to left_paddle ,
and the class attribute is accessed in name of or under the heading of left_paddle and only it's value(left_paddles y value) is iterated"""

def handle_paddle_motion(key,left_paddle,right_paddle):
    if key[pygame.K_w] and left_paddle.y-left_paddle.y_change>=0:
        left_paddle.movement(up=True)
    elif key[pygame.K_s] and left_paddle.y+left_paddle.y_change+left_paddle.paddle_ht<=screen_height:
        left_paddle.movement(up=False)
    elif key[pygame.K_UP] and right_paddle.y-right_paddle.y_change>=0:
        right_paddle.movement(up=True)
    elif key[pygame.K_DOWN] and right_paddle.y+right_paddle.paddle_ht+right_paddle.y_change<=screen_height:
        right_paddle.movement(up=False)
y_vel_new = 8
colln_snd = mixer.Sound('coll_snd.wav')# loads the sound of collision into the code
game_end_snd = mixer.Sound('winner_sound.wav')# loads the game end sound
def handle_collision(left_paddle,right_paddle,ball):
    if ball.y >=600:
        colln_snd.play()# plays collision sound
        ball.y_vel*=-1

    elif ball.y<=0:
        colln_snd.play()# plays collision sound
        ball.y_vel*=-1

    if ball.x_vel<0 :
        if ball.y>=left_paddle.y and ball.y<=left_paddle.y+left_paddle.paddle_ht:
            if ball.x-BALL_RADIUS<=left_paddle.x+left_paddle.paddle_wt:
                ball.x_vel *= -1 
                colln_snd.play()# plays collision sound
                """ here we are creating a reduction factor that is related to the distance at which the ball hits 
                the paddle and the paddle center based on this the y_vel is changed thereby changing the direction 
                of the ball after it hits the paddle"""
                mid_y = left_paddle.y+left_paddle.paddle_ht/2
                dffn = mid_y-ball.y
                redn_fact = (left_paddle.paddle_ht)/2 /max_vel
                y_vel_new = dffn/redn_fact
                ball.y_vel = y_vel_new 
    
    else:
        if ball.y>=right_paddle.y and ball.y<=right_paddle.y+right_paddle.paddle_ht:
            if ball.x+BALL_RADIUS>=right_paddle.x:
                ball.x_vel *= -1 
                colln_snd.play()# plays collision sound
                """ here we are creating a reduction factor that is related to the distance at which the ball hits 
                the paddle and the paddle center based on this the y_vel is changed thereby changing the direction 
                of the ball after it hits the paddle"""
                mid_y = right_paddle.y+right_paddle.paddle_ht/2
                dffn = mid_y-ball.y
                redn_fact = (right_paddle.paddle_ht)/2 /max_vel
                y_vel_new = dffn/redn_fact
                ball.y_vel = y_vel_new 
 
BALL_RADIUS = 5
max_vel= 6
#creating class ball with its attributes

class Ball:
    """ here in the init function you define all attributes that you pass while calling the class as self.x,self.y etc and any other
    constant attributes like max_vel, colour etc only"""
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = max_vel
        self.y_vel = 1
        self.colour = white 

    def draw_ball(self,screen):
        pygame.draw.circle(screen,self.colour,(self.x,self.y),self.radius)
    
    def ball_motion(self,left_paddle,right_paddle):
        self.x+=self.x_vel
        self.y+=self.y_vel
        if self.x>screen_width:
            self.x=right_paddle.x
            self.y=right_paddle.y+(PADDLE_HEIGHT/2)
            self.y_vel = 0
            left_paddle.score+=1
        if self.x<0:
            self.x=left_paddle.x
            self.y=left_paddle.y+(PADDLE_HEIGHT/2)
            self.y_vel=0
            right_paddle.score+=1

# loading font and assigning the coords for the scores to be displayed 
font = pygame.font.Font('freesansbold.ttf',20)
font_winner = pygame.font.Font('freesansbold.ttf',40)
scr_rt_x=10
scr_rt_y=scr_lft_y=10
scr_lft_x=500

# putting score into screen
def show_score(xl,yl,xr,yr,left_paddle,right_paddle):
    score_l=font.render("Score: "+str(left_paddle.score),True,(255,255,255))
    screen.blit(score_l,(xl,yl))
    score_r=font.render("Score: "+str(right_paddle.score),True,(255,255,255))
    screen.blit(score_r,(xr,yr))
    pygame.display.update()

#the main function where our all functionalities are to be displayed in the due time
def game_play():
    game_running=True
    # we create 2 instance of class Paddles left_paddle and right_paddle and make it into a list 
    left_paddle = Paddles(10,screen_height//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)#creating an instance of a class Paddles 
    right_paddle = Paddles(screen_width-20,screen_height//2 - PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)# creating an instance of a class Paddles
    ball = Ball(screen_width//2,screen_height//2,BALL_RADIUS)# creating instance of class Ball
    paddle_list = [left_paddle,right_paddle]
    while(game_running):
        draw_in_screen(screen,paddle_list,ball)# passing screen and paddle_list as parameters 
        clock.tick(FPS)# we use FPS to make the code run at 60 times per second, this tell the while loop how fast it must run in order to get 60 fps 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_running = False
        key = pygame.key.get_pressed()
        handle_paddle_motion(key,left_paddle,right_paddle)# handles paddle motion
        ball.ball_motion(left_paddle,right_paddle)# ball's motion
        handle_collision(left_paddle,right_paddle,ball)# handle collision
        show_score(scr_rt_x,scr_rt_y,scr_lft_x,scr_lft_y,left_paddle,right_paddle)
        # stopping the ball to display the winner
        game_over = False
        if left_paddle.score==pts_win or right_paddle.score==pts_win:
            game_over = True
            ball.x=300
            ball.y=300
            ball.y_vel=ball.x_vel=0
            left_paddle.y=right_paddle.y=300-75
            left_paddle.y_change=right_paddle.y_change=0
            # displaying the winner
            if left_paddle.score==pts_win:
                winner=font_winner.render("Winner is Left Paddle",True,(255,255,255))
                screen.blit(winner,(90,250))
                pygame.display.update()
            elif right_paddle.score==pts_win:
                winner=font_winner.render("Winner is Right Paddle",True,(255,255,255))
                screen.blit(winner,(90,250))
                pygame.display.update()
    if game_over:
        game_end_snd.play()
        pygame.display.update()
game_play()
