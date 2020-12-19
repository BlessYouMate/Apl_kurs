import pygame
import random
import math
from pygame import mixer
import time

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1000, 600))

# Background
background = pygame.image.load('background.png')


# black and white color
color = (0, 0, 0)
color2 = (255, 255, 255)

# button color (red)
bg_color = (136, 0, 21)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.Font('TAKOYAKI.ttf', 40)
bigfont = pygame.font.Font('TAKOYAKI.ttf', 80)

# Background sound
mixer.music.load('background_sound.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Gaar")
icon = pygame.image.load('ninja_icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 50
playerY = 290
playerX_change = 0
playerY_change = 0

# Score
score_value = 0
font = pygame.font.Font('TAKOYAKI.ttf', 30)

# Score_end
score_value_end = 0
font_end = pygame.font.Font('TAKOYAKI.ttf', 50)

textX = 880
textY = 10
# Game over text
game_over_font = pygame.font.Font('TAKOYAKI.ttf', 60)

# help text
help_font = pygame.font.Font('TAKOYAKI.ttf', 30)

end_game = False
start_game = True
start_screen = True
end_screen = False
help_screen = False
settings_screen = False
korean_theme = False
credits_screen = False
quit_button = True


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(1000000000)
    enemyY.append(1000000000)
    enemyX_change.append(0.5)
    enemyY_change.append(0.5)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - bullet is moving
bullet_upImg = pygame.image.load('kunai_up.png')
bulletX = 0
bulletY = 0
bulletX_change = 3
bulletY_change = 3
bullet_state = "ready"


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    game_over_text = game_over_font.render("YOU ARE DEAD", True, (0, 0, 0))
    screen.blit(game_over_text, (350, 230))
    global score_value
    score = font_end.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (450, 300))


def credits_text():
    credits_text = help_font.render("AUTHOR - WIKTOR JASIAK", True, (0, 0, 0))
    screen.blit(credits_text, (250, 20))
    credits_text = help_font.render("YOU CAN STICK TO THE WALL AND THEN GAME BECOMES", True, (0, 0, 0))
    screen.blit(credits_text, (250, 100))
    credits_text = help_font.render("VERY VERY EASY, BUT I WANT TO SAY...", True, (0, 0, 0))
    screen.blit(credits_text, (250, 140))
    credits_text = help_font.render("IT'S TACTIC FOR NOOBS", True, (0, 0, 0))
    screen.blit(credits_text, (250, 180))


def help_text():
    help_text = help_font.render("WELCOME IN GAAR!", True, (0, 0, 0))
    screen.blit(help_text, (250, 20))
    help_text = help_font.render("YOU ARE A WARRIOR WHO HAVE TO FIGHT", True, (0, 0, 0))
    screen.blit(help_text, (250, 60))
    help_text = help_font.render("WITH DANGEROUS DEMONS. MAKE THE HIGHEST SCORE POSSIBLE", True, (0, 0, 0))
    screen.blit(help_text, (250, 100))
    help_text = help_font.render("AND GAIN IMMORTAL GLORY!", True, (0, 0, 0))
    screen.blit(help_text, (250, 140))
    help_text = help_font.render("GODSPEED WARRIOR!", True, (0, 0, 0))
    screen.blit(help_text, (250, 180))

    help_text = help_font.render("CONTROLS", True, (0, 0, 0))
    screen.blit(help_text, (250, 260))
    help_text = help_font.render("MOVEMENT - ARROWS", True, (0, 0, 0))
    screen.blit(help_text, (250, 300))
    help_text = help_font.render("SHOOTING - [W] KEY", True, (0, 0, 0))
    screen.blit(help_text, (250, 340))

    help_text = help_font.render("YOU HAVE ONLY ONE BULLET", True, (0, 0, 0))
    screen.blit(help_text, (550, 210))
    help_text = help_font.render("AT YOUR DISPOSAL AT ONCE", True, (0, 0, 0))
    screen.blit(help_text, (550, 250))
    help_text = help_font.render("SO SHOOT STRAIGHT!", True, (0, 0, 0))
    screen.blit(help_text, (550, 290))


def settings_text():
    settings_text = bigfont.render("SETTINGS", True, (0, 0, 0))
    screen.blit(settings_text, (420, 25))
    in_settings_text = smallfont.render("(just one option but it's still something)", True, (0, 0, 0))
    screen.blit(in_settings_text, (420, 90))


def theme_text():
    theme_text = smallfont.render("CHANGE THEME", True, (0, 0, 0))
    screen.blit(theme_text, (360, 200))


def end():
    for j in range(num_of_enemies):
        enemyX_change[j] = 0
        enemyY_change[j] = 0
        enemyX[j] = 1000000000
        enemyY[j] = 1000000000
        global playerX_change
        global playerY_change
        playerX_change = 0
        playerY_change = 0


def Gong():
    gong_sound = mixer.Sound('gong.wav')
    gong_sound.set_volume(0.2)
    gong_sound.play()


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet_up(x, y):
    global bullet_state
    bullet_state = "fire"
    if korean_theme is True:
        screen.blit(bullet_upImg, (x+1, y-10))
    else:
        screen.blit(bullet_upImg, (x-3, y - 10))


def draw_bullet():
    screen.blit(bullet_upImg, (playerX, playerY))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27 and bullet_state == "fire":
        return True
    else:
        return False


def is_Enemy_Collision(enemyX, enemyY, playerX, playerY):

    distance_enemy = math.sqrt((math.pow(enemyX-playerX, 2)) + (math.pow(enemyY-playerY, 2)))
    if distance_enemy < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((102, 102, 255))
    # background image
    screen.blit(background, (0, 0))

    # SETTINGS SCREEN BUTTON
    if settings_screen is True:
        settings_text()
        theme_text()

        mouse = pygame.mouse.get_pos()

        if 110 - 10 <= mouse[0] <= 110 - 10 + 180 and 450 <= mouse[1] <= 450 + 70:
            pygame.draw.rect(screen, bg_color, [400 - 15, 350, 100, 20])
            text = bigfont.render('MENU', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [4100 - 15, 340, 100, 30])
            text = bigfont.render('MENU', True, color)

            # text on button
        screen.blit(text, (100, 450))

        # JAPANESE CHANGE BUTTON
        if 315 - 10 <= mouse[0] <= 315 - 10 + 160 and 250 <= mouse[1] <= 250 + 30:
            pygame.draw.rect(screen, bg_color, [4100 - 15, 350, 100, 20])
            text = smallfont.render('JAPANESE', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [3110 - 15, 250, 100, 30])
            text = smallfont.render('JAPANESE', True, color)

            # text on button
        screen.blit(text, (310, 250))

        # KOREAN CHANGE BUTTON
        if 525 - 10 <= mouse[0] <= 525 - 10 + 120 and 250 <= mouse[1] <= 250 + 30:
            pygame.draw.rect(screen, bg_color, [4100 - 15, 350, 100, 20])
            text = smallfont.render('KOREAN', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [4010 - 15, 340, 100, 30])
            text = smallfont.render('KOREAN', True, color)

            # text on button
        screen.blit(text, (515, 250))

    if credits_screen is True:
        credits_text()

        mouse = pygame.mouse.get_pos()

        if 110 - 10 <= mouse[0] <= 110 - 10 + 180 and 450 <= mouse[1] <= 450 + 70:
            pygame.draw.rect(screen, bg_color, [1100 - 15, 350, 100, 20])
            text = bigfont.render('MENU', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [1100 - 15, 340, 100, 30])
            text = bigfont.render('MENU', True, color)

            # text on button
        screen.blit(text, (100, 450))

    # HELP SCREEN BUTTON
    if help_screen is True:
        help_text()

        mouse = pygame.mouse.get_pos()

        if 110 - 10 <= mouse[0] <= 110 - 10 + 180 and 450 <= mouse[1] <= 450 + 70:
            pygame.draw.rect(screen, bg_color, [1100 - 15, 350, 100, 20])
            text = bigfont.render('MENU', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [1100 - 15, 340, 100, 30])
            text = bigfont.render('MENU', True, color)

            # text on button
        screen.blit(text, (100, 450))

        if 10 - 10 <= mouse[0] <= 10 - 10 + 465 and 570 <= mouse[1] <= 570 + 70:
            pygame.draw.rect(screen, bg_color, [1100 - 15, 350, 100, 20])
            text = help_font.render('CREDITS AND ONE WORD FROM AUTHOR', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [1100 - 15, 340, 100, 30])
            text = help_font.render('CREDITS AND ONE WORD FROM AUTHOR', True, color)

            # text on button
        screen.blit(text, (10, 570))

    if end_game is True:
        playerImg = pygame.image.load('player_end.png')
        mixer.music.stop()
        game_over_text()
        textY = 2000

        mouse = pygame.mouse.get_pos()

        if 380 - 45 <= mouse[0] <= 380 - 45 + 100 and 350 <= mouse[1] <= 350 + 40:
            pygame.draw.rect(screen, bg_color, [3180 - 45, 350, 100, 40])
            text = smallfont.render('QUIT', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [3180 - 45, 350, 100, 40])
            text = smallfont.render('QUIT', True, color)

            # text on button
        screen.blit(text, (350, 350))

        if 600 - 45 <= mouse[0] <= 600 - 45 + 100 and 350 <= mouse[1] <= 350 + 40:
            pygame.draw.rect(screen, bg_color, [6100 - 45, 350, 100, 40])
            text = smallfont.render('AGAIN', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [6100 - 45, 350, 100, 40])
            text = smallfont.render('AGAIN', True, color)

            # text on button
        screen.blit(text, (550, 350))

        if 140 - 45 <= mouse[0] <= 150 - 45 + 170 and 450 <= mouse[1] <= 450 + 70:
            pygame.draw.rect(screen, bg_color, [4190 - 45, 400, 100, 35])
            text = bigfont.render('MENU', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [4190 - 45, 400, 100, 35])
            text = bigfont.render('MENU', True, color)

            # text on button
        screen.blit(text, (100, 450))

    if start_game is True:
        playerImg = pygame.image.load('player_end.png')
        textY = 200000

        mouse = pygame.mouse.get_pos()

        if 400 <= mouse[0] <= 400 + 200 and 270 <= mouse[1] <= 270 + 60:
            pygame.draw.rect(screen, bg_color, [4100 - 45, 270, 100, 40])
            text = bigfont.render('START', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [4100 - 45, 270, 100, 40])
            text = bigfont.render('START', True, color)

            # text on button
        screen.blit(text, (400, 270))

        if 350 <= mouse[0] <= 350 + 70 and 370 <= mouse[1] <= 370 + 40:
            pygame.draw.rect(screen, bg_color, [3150 - 45, 300, 50, 40])
            text = smallfont.render('HELP', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [4100 - 45, 400, 90, 35])
            text = smallfont.render('HELP', True, color)

            # text on button
        screen.blit(text, (350, 370))

        if 530 <= mouse[0] <= 530 + 160 and 360 <= mouse[1] <= 370 + 40:
            pygame.draw.rect(screen, bg_color, [3150 - 45, 300, 50, 40])
            text = smallfont.render('SETTINGS', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [400 - 45, 400, 100, 40])
            text = smallfont.render('SETTINGS', True, color)

            # text on button
        screen.blit(text, (530, 370))

        if 485 - 45 <= mouse[0] <= 485 - 45 + 80 and 420 <= mouse[1] <= 420 + 35:
            pygame.draw.rect(screen, bg_color, [4190 - 45, 400, 100, 35])
            text = smallfont.render('QUIT', True, color2)

        else:
            pygame.draw.rect(screen, bg_color, [4190 - 45, 400, 100, 35])
            text = smallfont.render('QUIT', True, color)

            # text on button
        screen.blit(text, (445, 420))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # help button
            if 350 <= mouse[0] <= 350 + 70 and 370 <= mouse[1] <= 370 + 40 and start_screen is True\
                    and settings_screen is False and credits_screen is False:

                help_screen = True
                start_game = False

            # CREDITS BUTTON
            if 10 - 10 <= mouse[0] <= 10 - 10 + 465 and 570 <= mouse[1] <= 570 + 70 and help_screen is True:

                help_screen = False
                credits_screen = True

            # SETTINGS BUTTON
            if 530 <= mouse[0] <= 530 + 160 and 360 <= mouse[1] <= 370 + 40 and start_screen is True\
                    and help_screen is False and credits_screen is False:

                start_game = False
                settings_screen = True

            # CHANGE THEME

            # KOREAN
            if 525 - 10 <= mouse[0] <= 525 - 10 + 120 and 250 <= mouse[1] <= 250 + 30 and settings_screen is True\
                    and korean_theme is False:

                background = pygame.image.load('background_korea.png')
                screen.blit(background, (0, 0))
                playerImg = pygame.image.load('player_end.png')
                korean_theme = True
                bullet_upImg = pygame.image.load('shuriken.png')
                bg_color = (0, 162, 232)

            # JAPANESE
            if 320 - 10 <= mouse[0] <= 310 - 10 + 163 and 250 <= mouse[1] <= 250 + 30 and settings_screen is True\
                    and korean_theme is True:

                background = pygame.image.load('background.png')
                screen.blit(background, (0, 0))
                playerImg = pygame.image.load('player_end.png')
                bullet_upImg = pygame.image.load('kunai_up.png')
                bg_color = (136, 0, 21)
                korean_theme = False

            # CREDITS MENU BUTTON
            if 110 - 10 <= mouse[0] <= 110 - 10 + 180 and 450 <= mouse[1] <= 450 + 70 and credits_screen is True:
                start_game = True
                credits_screen = False

            # HELP MENU BUTTON
            if 100 <= mouse[0] <= 100 + 180 and 450 <= mouse[1] <= 450 + 65 and help_screen is True:
                help_screen = False
                start_game = True

            # SETTINGS MENU BUTTON
            if 100 <= mouse[0] <= 100 + 180 and 450 <= mouse[1] <= 450 + 65 and settings_screen is True:
                settings_screen = False
                start_game = True

            # END GAME MENU BUTTON
            if 100 <= mouse[0] <= 100 + 180 and 450 <= mouse[1] <= 450 + 65 and end_game is True:
                start_game = True
                end_screen = False
                end_game = False
                start_screen = True
                quit_button = True
                mixer.music.load('background_sound.mp3')
                mixer.music.play(-1)
                score_value = 0

            # if the mouse is clicked on the button game ends
            # QUIT
            if 380 - 45 <= mouse[0] <= 380 - 45 + 100 and 350 <= mouse[1] <= 350 + 40 and start_screen is False\
                    and end_screen is True and help_screen is False and settings_screen is False\
                    and end_game is True and credits_screen is False:

                running = False

            # QUIT ON START
            if 485 - 45 <= mouse[0] <= 485 - 45 + 80 and 420 <= mouse[1] <= 420 + 35 and start_screen is True\
                    and end_screen is False and settings_screen is False and help_screen is False\
                    and end_game is False and credits_screen is False and quit_button is True:

                running = False

            # Start
            if 400 <= mouse[0] <= 400 + 200 and 270 <= mouse[1] <= 270 + 60 and start_screen is True\
                    and settings_screen is False and help_screen is False and credits_screen is False:

                for i in range(num_of_enemies):
                    enemyImg.append(pygame.image.load('enemy.png'))
                    enemyX[i] = (random.randint(200, 900))
                    enemyY[i] = (random.randint(50, 550))
                    enemyX_change.append(0.5)
                    enemyY_change.append(0.5)
                    start_game = False
                    playerX = 50
                    playerY = 290
                    playerX_change = 0
                    playerY_change = 0
                    textY = 10
                    start_screen = False
                    if korean_theme is True:
                        playerImg = pygame.image.load('player_kr.png')
                    else:
                        playerImg = pygame.image.load('player.png')

            # restart
            if 550 <= mouse[0] <= 550 + 100 and 350 <= mouse[1] <= 350 + 40 and start_screen is False and\
                    end_game is True and help_screen is False and settings_screen is False:

                for i in range(num_of_enemies):
                    mixer.music.load('background_sound.mp3')
                    time.sleep(0.08)
                    enemyImg.append(pygame.image.load('enemy.png'))
                    enemyX[i] = (random.randint(200, 900))
                    enemyY[i] = (random.randint(50, 550))
                    enemyX_change.append(0.5)
                    enemyY_change.append(0.5)
                    start_game = False
                    end_game = False
                    settings_screen = False
                    mixer.music.play(-1)
                    playerX = 50
                    playerY = 290
                    playerX_change = 0
                    playerY_change = 0
                    textY = 10
                    score_value = 0
                    if korean_theme is True:
                        playerImg = pygame.image.load('player_kr.png')
                    else:
                        playerImg = pygame.image.load('player.png')

        # controls
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                playerY_change = -1.2

            if event.key == pygame.K_DOWN:
                playerY_change = 1.2

            if event.key == pygame.K_LEFT:
                playerX_change = -0.3

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_w and end_game is False and start_game is False and start_screen is False:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('knife_throw.wav')
                    bullet_Sound.play()
                    # get the current player coordinates
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet_up(bulletX, bulletY)

    # player borders X
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    if playerX >= 970 and korean_theme is False:
        playerX = 970

    if korean_theme is True and playerX >= 965:
        playerX = 965

    # player borders Y
    playerX += playerX_change

    if playerY <= 0:
        playerY = 0

    if playerY >= 570 and korean_theme is False:
        playerY = 570

    if korean_theme is True and playerY >= 555:
        playerY = 555

    # enemy borders/movement
    for i in range(num_of_enemies):

        # Collision enemy/game over
        enemy_collision = is_Enemy_Collision(enemyX[i], enemyY[i], playerX, playerY)
        if enemy_collision:
            Gong()
            end()
            end_game = True
            end_screen = True
            start_screen = False
            start_game = False
            quit_button = False

        enemyY[i] += enemyY_change[i]

        if enemyY[i] <= 0:
            enemyY_change[i] = 0.3
        elif enemyY[i] >= 555:
            enemyY_change[i] = -0.3

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
        elif enemyX[i] >= 953:
            enemyX_change[i] = -0.3

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            death_Sound = mixer.Sound('death.wav')
            death_Sound.set_volume(0.2)
            death_Sound.play()
            bulletY = playerY
            bulletX = playerX
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(200, 900)
            enemyY[i] = random.randint(50, 550)

        enemy(enemyX[i], enemyY[i], i)
        enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bulletX = playerX
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet_up(bulletX, bulletY)
        bulletY -= bulletY_change

    playerX += playerX_change
    playerY += playerY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
