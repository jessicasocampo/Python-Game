import pygame
import time
import random

pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 1000, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VEL = 5
STAR_WIDTH, STAR_HEIGHT = 10, 20
STAR_VEL = 3
FONT = pygame.font.SysFont("comicsans", 30)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x - PLAYER_VEL >= 0:
            self.rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and self.rect.x + PLAYER_VEL + self.rect.width <= WIDTH:
            self.rect.x += PLAYER_VEL

class Star:
    def __init__(self, x):
        self.rect = pygame.Rect(x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)

    def move(self):
        self.rect.y += STAR_VEL

def draw(win, bg, player, elapsed_time, stars):
    win.blit(bg, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    win.blit(time_text, (10, 10))

    pygame.draw.rect(win, "white", player.rect)

    for star in stars:
        pygame.draw.rect(win, "white", star.rect)

def game_over():
    lost_text = FONT.render("You Lost!", 1, "white")
    win.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

def main(win):
    run = True

    player = Player()

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        player.move(keys)

        star_count += clock.tick(30)
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        if star_count > star_add_increment:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                stars.append(Star(star_x))

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for star in stars[:]:
            star.move()
            if star.rect.y > HEIGHT:
                stars.remove(star)
            elif star.rect.y + star.rect.height >= player.rect.y and star.rect.colliderect(player.rect):
                game_over()
                run = False
                break

        draw(win, bg, player, elapsed_time, stars)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("title")

    bg = pygame.transform.scale(pygame.image.load("bgspace.jpg").convert(), (WIDTH, HEIGHT))
    
    main(win)
