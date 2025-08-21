# =========================================================
# Flappy Bird – Red Edition with Start & Restart Screens
# =========================================================
import pygame, random, math, array

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird – Red Edition")
clock = pygame.time.Clock()

# ---------------------------------------------------------
# Sound helper – tiny procedurally generated tones
# ---------------------------------------------------------
def make_sound(freq, duration, volume=0.3, shape='sine'):
    sample_rate = 44100
    frames = int(sample_rate * duration)
    arr = array.array('h')
    for t in range(frames):
        val = int(volume * 32767 *
                  (math.sin(2 * math.pi * freq * t / sample_rate) if shape == 'sine'
                   else (1 if int(2 * freq * t / sample_rate) % 2 else -1)))
        arr.append(val)
        arr.append(val)  # stereo
    return pygame.mixer.Sound(buffer=arr)

sfx_flap   = make_sound(800, 0.08, 0.25)
sfx_point  = make_sound(1000, 0.15, 0.25)
sfx_die    = make_sound(300, 0.25, 0.4, shape='square')

music_tone = make_sound(220, 4.0, 0.05)
music_tone.play(-1)   # loop forever

# ---------------------------------------------------------
# Bird class
# ---------------------------------------------------------
class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.vel = 0
        self.gravity = 0.5
        self.w, self.h = 34, 24

    def jump(self):
        self.vel = -8
        sfx_flap.play()

    def update(self):
        self.vel += self.gravity
        self.y += self.vel

    def draw(self):
        pygame.draw.ellipse(screen, (255,  50,  50), (self.x, self.y, self.w, self.h))
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 24, self.y + 8), 5)
        pygame.draw.circle(screen, (  0,   0,   0), (self.x + 26, self.y + 8), 2)
        pygame.draw.polygon(screen, (255, 200, 0),
            [(self.x + 32, self.y + 10), (self.x + 38, self.y + 12), (self.x + 32, self.y + 14)])

# ---------------------------------------------------------
# Pipe class
# ---------------------------------------------------------
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.gap_start = random.randint(120, HEIGHT - 220)
        self.gap_height = 130
        self.width = 60

    def update(self):
        self.x -= 4

    def draw(self):
        pygame.draw.rect(screen, (0, 180, 0), (self.x, 0, self.width, self.gap_start))
        pygame.draw.rect(screen, (0, 180, 0),
            (self.x, self.gap_start + self.gap_height, self.width, HEIGHT))

# ---------------------------------------------------------
# Start screen
# ---------------------------------------------------------
def show_start_screen():
    font_big  = pygame.font.SysFont(None, 48)
    font_btn  = pygame.font.SysFont(None, 36)
    title_txt = font_big.render("Flappy Bird", True, (255, 255, 255))
    btn_txt   = font_btn.render("START GAME", True, (0, 0, 0))
    btn_rect  = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)

    while True:
        screen.fill((135, 206, 235))
        screen.blit(title_txt, (WIDTH//2 - title_txt.get_width()//2, HEIGHT//3))
        pygame.draw.rect(screen, (0, 200, 0), btn_rect, border_radius=10)
        screen.blit(btn_txt, (btn_rect.x + (btn_rect.w - btn_txt.get_width())//2,
                              btn_rect.y + 10))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(e.pos):
                return

# ---------------------------------------------------------
# Game Over screen
# ---------------------------------------------------------
def show_game_over_screen(score):
    font_big = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 32)
    btn_txt = font_small.render("CLICK TO RESTART", True, (0, 0, 0))
    btn_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 40)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(font_big.render("Game Over", True, (255, 255, 255)),
                    (WIDTH // 2 - 80, HEIGHT // 2 - 60))
        screen.blit(font_small.render(f"Score: {score}", True, (255, 255, 255)),
                    (WIDTH // 2 - 40, HEIGHT // 2 - 20))
        pygame.draw.rect(screen, (0, 200, 0), btn_rect, border_radius=10)
        screen.blit(btn_txt, (btn_rect.x + (btn_rect.w - btn_txt.get_width())//2,
                              btn_rect.y + 8))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(e.pos):
                return

# ---------------------------------------------------------
# Game loop
# ---------------------------------------------------------
def game_loop():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font_big = pygame.font.SysFont(None, 48)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()
        for p in pipes:
            p.update()

        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        pipes = [p for p in pipes if p.x > -p.width]

        bird_rect = pygame.Rect(bird.x, bird.y, bird.w, bird.h)
        for p in pipes:
            top_rect = pygame.Rect(p.x, 0, p.width, p.gap_start)
            bot_rect = pygame.Rect(p.x, p.gap_start + p.gap_height, p.width, HEIGHT)
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bot_rect):
                sfx_die.play()
                running = False
        if bird.y < 0 or bird.y + bird.h > HEIGHT:
            sfx_die.play()
            running = False

        for p in pipes:
            if not hasattr(p, 'scored') and p.x + p.width < bird.x:
                p.scored = True
                score += 1
                sfx_point.play()

        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (139, 69, 19), (0, HEIGHT - 50, WIDTH, 50))
        bird.draw()
        for p in pipes:
            p.draw()

        score_surf = font_big.render(str(score), True, (255, 255, 255))
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 30))

        pygame.display.flip()
        clock.tick(60)

    return score

# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------
if __name__ == "__main__":
    while True:
        show_start_screen()
        final_score = game_loop()  
        show_game_over_screen(final_score)
