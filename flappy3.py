import pygame
import random
import math
import array

pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# ----------- Sound generation ----------
def make_sound(freq, duration=0.1, volume=0.2, shape="sine"):
    sr = 44100
    n = int(sr*duration)
    buf = array.array("h")
    for t in range(n):
        if shape == "sine":
            s = math.sin(2*math.pi*freq*t/sr)
        elif shape == "square":
            s = 1.0 if ((t*freq*2)//sr)%2==0 else -1.0
        else:
            s = math.sin(2*math.pi*freq*t/sr)
        v = int(s*volume*32767)
        buf.append(v)
        buf.append(v)
    return pygame.mixer.Sound(buffer=buf)

jump_sound = make_sound(1000, 0.07)
score_sound = make_sound(800, 0.1)
gameover_sound = make_sound(300, 0.3)

# Ambient background loop
ambient1 = make_sound(220, 0.8, 0.05)
ambient2 = make_sound(277, 0.8, 0.05)
ambient3 = make_sound(330, 0.8, 0.05)
ambient1.play(loops=-1)
ambient2.play(loops=-1)
ambient3.play(loops=-1)

# ----------- Classes -----------
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.width = 40
        self.height = 30
        self.gravity = 0.4
        self.velocity = 0
        self.jump_strength = -7

    def jump(self):
        self.velocity = self.jump_strength
        jump_sound.play()

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        pygame.draw.ellipse(screen, YELLOW, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, WHITE, (self.x + 30, self.y + 10), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 32, self.y + 10), 2)

class Pipe:
    def __init__(self):
        self.width = 60
        self.gap_height = 160
        self.x = WIDTH
        self.gap_start = random.randint(100, HEIGHT - self.gap_height - 100)
        self.passed = False

    def update(self):
        self.x -= 3

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_start))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.gap_start - 20, self.width, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_start + self.gap_height, self.width, HEIGHT))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.gap_start + self.gap_height, self.width, 20))

# ----------- Utility -----------
def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont("Arial", size, bold=True)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

# ----------- Game Loop -----------
def game_loop():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        screen.fill((135, 206, 235))  # Sky blue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                if event.key == pygame.K_SPACE and game_over:
                    return True

        if not game_over:
            bird.update()

            # Pipes update
            for pipe in pipes:
                pipe.update()
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
                    score_sound.play()

            if pipes[-1].x < WIDTH - 350:
                pipes.append(Pipe())

            # Collision check
            for pipe in pipes:
                if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width:
                    if bird.y < pipe.gap_start or bird.y + bird.height > pipe.gap_start + pipe.gap_height:
                        game_over = True
                        gameover_sound.play()
            if bird.y <= 0 or bird.y + bird.height >= HEIGHT:
                game_over = True
                gameover_sound.play()

        bird.draw()
        for pipe in pipes:
            pipe.draw()

        draw_text(f"Score: {score}", 30, WHITE, 10, 10, center=False)

        if game_over:
            draw_text("GAME OVER", 50, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Press SPACE to Retry", 25, WHITE, WIDTH // 2, HEIGHT // 2 + 20)

        pygame.display.flip()

    return False

def start_screen():
    while True:
        screen.fill((135, 206, 235))
        draw_text("Flappy Bird", 50, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press SPACE to Start", 25, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

# ----------- Main Loop -----------
while True:
    if not start_screen():
        break
    if not game_loop():
        break

pygame.quit()
