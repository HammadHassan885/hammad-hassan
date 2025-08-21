# =========================================================
# Flappy_GUI_v2.py  –  pygame Flappy Bird
# Red bird, sky background, sounds – zero external assets
# =========================================================
import pygame, random, math

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

import array   # <-- builtin module, no install needed

def make_sound(freq, duration, volume=0.3, shape='sine'):                       
    sample_rate = 44100
    frames = int(sample_rate * duration)
    arr = array.array('h')   # signed short (16-bit)
    for t in range(frames):
        val = int(volume * 32767 *
                  (math.sin(2 * math.pi * freq * t / sample_rate) if shape == 'sine'
                   else (1 if int(2 * freq * t / sample_rate) % 2 else -1)))
        arr.append(val)
    return pygame.mixer.Sound(arr)  

sfx_flap   = make_sound(800, 0.08, 0.25)
sfx_point  = make_sound(1000, 0.15, 0.25)
sfx_die    = make_sound(300, 0.25, 0.4, shape='square')

# Background music (very soft birds-like ambient loop)
music_tone = make_sound(220, 4.0, 0.05)
music_tone.play(-1)   # loop forever

# ---------------------------------------------------------
# Bird – red, drawn with vector shape
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
        # red bird body
        pygame.draw.ellipse(screen, (255,  50,  50), (self.x, self.y, self.w, self.h))
        # eye
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 24, self.y + 8), 5)
        pygame.draw.circle(screen, (  0,   0,   0), (self.x + 26, self.y + 8), 2)
        # beak
        pygame.draw.polygon(screen, (255, 200, 0),
            [(self.x + 32, self.y + 10), (self.x + 38, self.y + 12), (self.x + 32, self.y + 14)])

# ---------------------------------------------------------
# Pipe – two green rectangles
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
        # top pipe
        pygame.draw.rect(screen, (0, 180, 0), (self.x, 0, self.width, self.gap_start))
        # bottom pipe
        pygame.draw.rect(screen, (0, 180, 0),
            (self.x, self.gap_start + self.gap_height, self.width, HEIGHT))

# ---------------------------------------------------------
# Game loop
# ---------------------------------------------------------
def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font_big = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 32)

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update
        bird.update()
        for p in pipes:
            p.update()

        # Spawn new pipes
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        # Remove off-screen pipes
        pipes = [p for p in pipes if p.x > -p.width]

        # Collision
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

        # Score
        for p in pipes:
            if not hasattr(p, 'scored') and p.x + p.width < bird.x:
                p.scored = True
                score += 1
                sfx_point.play()

        # Draw everything
        screen.fill((135, 206, 235))  # sky
        # ground strip
        pygame.draw.rect(screen, (139, 69, 19), (0, HEIGHT - 50, WIDTH, 50))
        bird.draw()
        for p in pipes:
            p.draw()

        score_surf = font_big.render(str(score), True, (255, 255, 255))
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 30))

        pygame.display.flip()
        clock.tick(60)

    # Game-over screen
    screen.blit(font_big.render("Game Over", True, (255, 255, 255)),
                (WIDTH // 2 - 80, HEIGHT // 2 - 40))
    screen.blit(font_small.render(f"Score: {score}", True, (255, 255, 255)),
                (WIDTH // 2 - 40, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()