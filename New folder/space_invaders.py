#to run this game open cmd and type cd "C:\Users\Kanal Vyas\Documents\sem 5\space invaders\New folder"
#python space_invaders.py


import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions  
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Title and icon
pygame.display.set_caption("Space Invaders")

# Player
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_image = pygame.image.load('enemy.png')  #  enemy image 
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Resize 
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.1)
    enemy_y_change.append(40)

# Bullet
bullet_x = 0
bullet_y = 480
bullet_y_change = 0.8
bullet_state = "ready"  # "ready" means bullet is not visible, "fire" means bullet is moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, white)
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, white)
    screen.blit(over_text, (200, 250))

def draw_player(x, y):
    # Calculate the points for a pentagon
    radius = 30  # Size of the pentagon
    points = [
        (x + radius * math.cos(math.radians(angle)), y + radius * math.sin(math.radians(angle)))
        for angle in range(0, 360, 72)  # 72 degrees between each vertex (360/5)
    ]
    pygame.draw.polygon(screen, (0, 0, 255), points)

def draw_enemy(x, y):
    # Draw the enemy image at (x, y)
    screen.blit(enemy_image, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    pygame.draw.rect(screen, (0, 0, 255), (x, y, 5, 15))  # Bullet color changed to blue

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# Main game loop
running = True
while running:
    screen.fill(black)  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke checks
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    player_x = max(40, min(player_x, 760))  # Boundaries

    # Enemy movement
    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 30:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 770:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        # Collision check
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        draw_enemy(enemy_x[i], enemy_y[i])

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    draw_player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()