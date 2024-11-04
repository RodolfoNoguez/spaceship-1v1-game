import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)


AMMO_HIT_AUDIO = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
AMMO_AUDIO = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HP_FONT = pygame.font.SysFont('algerian', 40)
WINNER_FONT = pygame.font.SysFont('algerian', 100)

FPS = 120
VELOCITY = 4
AMMO_VELOCITY = 6
MAX_AMMO = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90 )

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_v2.png')), (WIDTH, HEIGHT))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(red, yellow, red_ammo, yellow_ammo, red_hp, yellow_hp):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_hp_text = HP_FONT.render("Health: " + str(red_hp), 1, WHITE)
    yellow_hp_text = HP_FONT.render("Health: " + str(yellow_hp), 1, WHITE)
    WIN.blit(red_hp_text, (WIDTH - red_hp_text.get_width() - 10, 10))
    WIN.blit(yellow_hp_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))




    for ammo in red_ammo:
        pygame.draw.rect(WIN, RED, ammo)

    for ammo in yellow_ammo:
        pygame.draw.rect(WIN, YELLOW, ammo)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VELOCITY

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:  # RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15:  # DOWN
        red.y += VELOCITY



def handle_ammo(yellow_ammo, red_ammo, yellow, red):
    for ammo in yellow_ammo:
        ammo.x += AMMO_VELOCITY
        if red.colliderect(ammo):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_ammo.remove(ammo)
        elif ammo.x > WIDTH:
            yellow_ammo.remove(ammo)

    for ammo in red_ammo:
        ammo.x -= AMMO_VELOCITY
        if yellow.colliderect(ammo):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_ammo.remove(ammo)
        elif ammo.x < 0:
            red_ammo.remove(ammo)





def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_ammo = []
    yellow_ammo = []

    red_hp = 15
    yellow_hp = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_ammo) < MAX_AMMO:
                    ammo = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_ammo.append(ammo)
                    AMMO_AUDIO.play()

                if event.key == pygame.K_RCTRL and len(red_ammo) < MAX_AMMO:
                    ammo = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_ammo.append(ammo)
                    AMMO_AUDIO.play()
            if event.type == RED_HIT:
                red_hp -= 1
                AMMO_HIT_AUDIO.play()
            if event.type == YELLOW_HIT:
                yellow_hp -= 1
                AMMO_HIT_AUDIO.play()



        winner_text = ""
        if red_hp <= 0:
            winner_text = "Yellow Wins!"

        if yellow_hp <= 0:
            winner_text = 'Red Wins!'

        if winner_text != "":
            draw_winner(winner_text)
            break




        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_ammo(yellow_ammo, red_ammo, yellow, red)
        draw_window(red, yellow, red_ammo, yellow_ammo, red_hp, yellow_hp)

    main()


if __name__ == "__main__":
    main()


