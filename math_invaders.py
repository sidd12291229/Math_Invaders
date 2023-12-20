import pygame
import random
import math
from pygame import mixer
import sympy as sp

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Math Invaders")
font = pygame.font.Font('font.ttf', 20)

title_font = pygame.font.Font('font.ttf', 64)
button_font = pygame.font.Font('font.ttf', 32)

def title_screen():
    title_text = title_font.render("Math Invaders", True, (255, 255, 255))
    play_button_text = button_font.render("Play", True, (255, 255, 255))
    quit_button_text = button_font.render("Quit", True, (255, 255, 255))

    screen.blit(title_text, (150, 200))
    pygame.draw.rect(screen, (0, 128, 255), (300, 350, 200, 50))
    pygame.draw.rect(screen, (0, 128, 255), (300, 420, 200, 50))
    screen.blit(play_button_text, (350, 360))
    screen.blit(quit_button_text, (360, 430))

def show_title_screen():
    title_screen()

    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the Play button is clicked
                if 300 <= mouse_x <= 500 and 350 <= mouse_y <= 400:
                    waiting_for_input = False

                # Check if the Quit button is clicked
                elif 300 <= mouse_x <= 500 and 420 <= mouse_y <= 470:
                    pygame.quit()
                    quit()

        pygame.time.Clock().tick(30)

# Score
score_val = 0
bullet_count = 10
scoreX = 5
scoreY = 5
bulletX = 650  
bulletY = 5 

x = sp.symbols('x')
equations = [
    (sp.Eq(4 * x - 7, 9), [4]),
    (sp.Eq(2 * (x + 3), 14), [4]),
    (sp.Eq(5 * x + 2, 27), [5]),
    (sp.Eq(3 * (x - 4), 15), [9]),
    (sp.Eq(6 + 2 * x, 14), [4]),
    (sp.Eq(4 * (x + 2) - 3, 29), [6]),
    (sp.Eq(2 * x - 5, 15), [10]),
    (sp.Eq(7 + 2 * (x - 3), 15), [7]),
    (sp.Eq(9 * x + 5, 41), [4]),
    (sp.Eq(-3 * x + 2, -10), [4]),
    (sp.Eq(2 * (x + 4) + 3, 17), [3]),
    (sp.Eq(5 * (x - 1) - 2, 18), [5]),
    (sp.Eq(6 - 4 * x, -10), [4]),
    (sp.Eq(2 * x - 3, x + 5), [8]),
    (sp.Eq(2 * x + 1, x + 4), [3]),
    (sp.Eq(3 * x + 2, 8), [2]),
    (sp.Eq(4 * (x + 1) + 3, 15), [2]),
    (sp.Eq(5 * (x - 2) - 4, 6), [4]),
    (sp.Eq(2 * x - 3 * (x + 4), -17), [5]),
    (sp.Eq(9 - 2 * (x + 1), 3), [2]),
    (sp.Eq(7 - 3 * x, 16), [-3]),
    (sp.Eq(4 * x + 1, 9), [2]),
    (sp.Eq(3 * (x - 1) + 4, 7), [2]),
    (sp.Eq(8 - 2 * x, 6), [1]),
    (sp.Eq(4 * x - 5, 11), [4]),
    (sp.Eq(9 - 3 * (x - 4), 0), [7]),
]

def show_score(x, y, bx, by):
    score = font.render("Your Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

    bullet_text = font.render("Bullets: " + str(bullet_count), True, (255, 255, 255))
    screen.blit(bullet_text, (bx, by))


# Game Over
game_over_font = pygame.font.Font('font.ttf', 64)

def game_over():
    game_over_text = game_over_font.render("Game Over!", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))

# Background music
mixer.music.load('music.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# loading the player image and location
playerImage = pygame.image.load('spaceship.png')
player_X = 370
player_Y = 523
player_Xchange = 0

# defining index brackets for the enemy's
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 3

for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('alien.png'))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(0.6)
    invader_Ychange.append(50)

# pew pew
bulletImage = pygame.image.load('bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 5
bullet_state = "rest"


# Input box setup
class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (173, 216, 230)
        self.text = ''
        self.txt_surface = font.render(self.text, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (173, 216, 230) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Process the input here (you can use self.text)
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, (0, 0, 0))

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False

def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))

def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))

def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"

# Input box setup
input_box = InputBox(100, 550, 140, 32)

# Choose the first equation outside the game loop
equation, correct_answers = random.choice(equations)
show_title_screen()
pygame.init()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_Xchange = -1.7
            if event.key == pygame.K_d:
                player_Xchange = 1.7
            if event.key == pygame.K_SPACE and bullet_count > 0:
                if bullet_state is "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('bruh.wav')
                    bullet_sound.play()
                    bullet_count -= 1
        if event.type == pygame.KEYUP:
            player_Xchange = 0

        # Handle events for the input box
        input_box.handle_event(event)

    player_X += player_Xchange
    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state is "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    equation_text = f"Solve the equation: {sp.pretty(equation)}"

    equation_surface = font.render(equation_text, True, (255, 255, 255))

    textRect = equation_surface.get_rect()

    textRect.center = (154, 50)

    screen.blit(equation_surface, textRect)

    if not input_box.active and input_box.text:
        user_answer = sp.sympify(input_box.text)
        if user_answer not in correct_answers:
            incorrect_text = font.render("Incorrect. Try again.", True, (255, 0, 0))
            screen.blit(incorrect_text, (50, 100))
            pygame.display.flip()
            pygame.time.delay(1000) 
            input_box.text = ''
        else:
            correct_text = font.render("Correct!", True, (0, 255, 0))
            screen.blit(correct_text, (50, 100))
            pygame.display.flip()
            pygame.time.delay(1000)
            bullet_count += 5
            equation, correct_answers = random.choice(equations)
            input_box.text = ''
        
        input_box.text = ''
    
    if score_val >= 50:
        win_text = game_over_font.render("You Win!", True, (0, 255, 0))
        screen.blit(win_text, (190, 250))
        pygame.display.update()
        pygame.time.delay(2000) 
        win_sound = mixer.Sound('win.mp3')  
        win_sound.play()
        pygame.quit()
        running = False

    # game over
    for i in range(no_of_invaders):
        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                    explosion_sound = mixer.Sound('explosion.mp3')
                    explosion_sound.play()
                game_over()
                break

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]

        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i], i)

    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750

    player(player_X, player_Y)

    # Update the input box
    input_box.update()

    # Display score and bullet count
    show_score(scoreX, scoreY, bulletX, bulletY)

    # Draw the input box
    input_box.draw(screen)

    pygame.display.update()

pygame.quit()