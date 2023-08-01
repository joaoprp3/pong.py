import pygame
import sys
import random

# Game Objects
class Player:
    """

    :param int xCoordinates: cartesian x value of a rectagle
    :param int yCoordinates: cartesian y value of a rectagle
    :param int width: width of the rectangle
    :param int height: height of the rectangle
    """
    def __init__(self, xCoordinates, yCoordinates, width, height):
        self.body = pygame.Rect(xCoordinates, yCoordinates, width, height)
        self.speed = 0
        self.score = 0

    def movement(self, port):
        if port == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.speed += 6
                if event.key == pygame.K_w:
                    self.speed -= 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.speed -= 6
                if event.key == pygame.K_w:
                    self.speed += 6
        if port == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.speed += 6
                if event.key == pygame.K_UP:
                    self.speed -= 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.speed -= 6
                if event.key == pygame.K_UP:
                    self.speed += 6
    
    def animation(self):
        self.body.y += self.speed
        self.out_of_Bounds(screen_height)
    
    def out_of_Bounds(self, height):
        if self.body.top <= 0:
            self.body.top = 0
        if self.body.bottom >= height:
            self.body.bottom = height
        return None

class Ball:
    def __init__(self, x_Coordinates, y_Coordinates, width, height):
        self.body = pygame.Rect(x_Coordinates, y_Coordinates, width, height)
        self.score_time = pygame.time.get_ticks()
        self.speed_x, self.speed_y = 0, 0
        self.hitSfx = "BallHit.mp3"

    def set_speed(self, moving= True):
        if moving:
            self.speed_y = 7 * random.choice((1, -1))
            self.speed_x = 7 * random.choice((1, -1))
        else:
            self.speed_x, self.speed_y = 0, 0

    def start(self):
        current_time = pygame.time.get_ticks()
        self.body.center = (screen_width/2, screen_height/2)

        if current_time - self.score_time < 2100:
            if current_time - self.score_time < 700:
                if current_time - self.score_time < 10:
                    game_sfx("StartBall.mp3")
                number = game_texts("3", white)
            elif 700 < current_time - self.score_time < 1400:
                number = game_texts("2", white)
            else:
                number = game_texts("1", white)
            screen.blit(number,(screen_width/2 - 10, screen_height/2 +20))
            self.set_speed(False)

        else:
            self.set_speed(True)
            self.score_time = None
            

    def animation(self, player1, player2):
        self.body.x += self.speed_x
        self.body.y += self.speed_y

        if self.body.top <= 0 or self.body.bottom >= screen_height:
            self.speed_y *= -1

        if self.body.left <= 0:
            player2.score +=1
            self.score_time = pygame.time.get_ticks()

        elif self.body.right >= screen_width:
            player1.score +=1
            self.score_time = pygame.time.get_ticks()

        if self.body.colliderect(player1.body) and self.speed_x < 0:
            if abs(self.body.left - player1.body.right) < 10:
                self.speed_x *= -1
                game_sfx(self.hitSfx)
            elif abs(self.body.bottom - player1.body.top) < 10 and self.speed_y > 0:
                self.speed_x *= -1
                self.speed_y *= -1
                game_sfx(self.hitSfx)
            elif abs(self.body.top - player1.body.bottom) < 10 and self.speed_y < 0:
                self.speed_x *= -1
                self.speed_y *= -1
                game_sfx(self.hitSfx)
        if self.body.colliderect(player2.body) and self.speed_x > 0:
            if abs(self.body.right - player2.body.left) < 10:
                self.speed_x *= -1
                game_sfx(self.hitSfx)
            elif abs(self.body.bottom - player2.body.top) < 10 and self.speed_y > 0:
                self.speed_x *= -1
                self.speed_y *= -1
                game_sfx("BallHit.mp3")
            elif abs(self.body.top - player2.body.bottom) < 10 and self.speed_y < 0:
                self.speed_x *= -1
                self.speed_y *= -1
                game_sfx("BallHit.mp3")

class GameManager:
    def run_Game(player1, player2, ball):
        #Game Logic
        ball.animation(player1, player2)
        player1.animation()
        player2.animation()

        # Visual
        """The order of the code = the order of drawning"""
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player1.body)
        pygame.draw.rect(screen, light_grey, player2.body)
        pygame.draw.ellipse(screen, light_grey, ball.body)
        pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

        score_left = game_texts(f"{player1.score}",light_grey, 33)
        score_right = game_texts(f"{player2.score}", light_grey, 33)
        screen.blit(score_left,(600,20))
        screen.blit(score_right,(660,20))

        if ball.score_time:
            ball.start()


'''def opponent_ai():
    if player2.top < ball.y:
        player2.y += player2_speed
    if player2.bottom > ball.y:
        player2.y += player2_speed

    if player2.top <= 0:
        player2.top = 0
    if player2.bottom >= screen_height:
        player2.bottom = screen_height'''

def window_update(window):
    if not window:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        window = True
    elif fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height))
        window = False
    return window

# Main text format
def game_texts(toDisplay, color = (200, 200 , 200), size=33,  font= "freesansbold.ttf"):
    game_font = pygame.font.Font(font, size).render(toDisplay, True, color)
    return game_font

# Main game sounds
def game_sfx(file_path):
    pygame.mixer.Sound(file_path).play(loops=0, maxtime=0, fade_ms=0)

# General setup
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
timer = 0
dt = 0

# Setting up the main window
fullscreen = False
screen_width = 1280
screen_height = 720     # 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
pygame.display.set_icon(pygame.image.load('Icon.png'))

# Game Rectangles
ball = Ball(screen_width/2 - 15, screen_height/2 - 3, 30, 30)
player1 = Player(10, screen_height / 2 - 50, 10, 140)
player2 = Player(screen_width - 20, screen_height / 2 - 50, 10, 140)

# Colors
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
white = (255, 255, 255)

isPaused = False
"""while True:
    game = False
    startup_screen()"""
    # Main loop
while True:
    
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                isPaused = not isPaused
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if timer == 0:
                        timer = 0.001
                    elif timer < 0.5:
                            fullscreen = window_update(fullscreen)
                            timer = 0
        while isPaused:
            player1.movement(1)
            player2.movement(2)
    if timer != 0:
        timer += dt
        # Reset after 0.5 seconds.
        if timer >= 0.5:
            timer = 0

    GameManager.run_Game(player1, player2, ball)

    # Uodating the window
    pygame.display.flip()
    dt = clock.tick(60)/2000