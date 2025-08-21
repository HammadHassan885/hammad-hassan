# Zombie Shooter — single file, no external assets
# Controls: WASD move · Mouse aim · LMB shoot · R reload · P pause
# Space = start / restart · Esc = quit

import pygame, math, random, array, sys

# ---------- Init ----------
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
WIDTH, HEIGHT = 960, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter — no assets")
clock = pygame.time.Clock()
FPS = 60
rand = random.Random()

# ---------- Difficulty / Tuning ----------
ZOMBIE_SPEED_RANGE = (40, 70)   # ↓ slower base speed (was ~75–110)
ZOMBIE_SPEED_PER_LEVEL = 3      # ↓ slower scaling per level (was 6)
SPAWN_COOLDOWN_MIN = 0.60       # ↓ fewer spawns at high level (was 0.35)

# ---------- Colors ----------
BG1 = (20, 22, 28)
BG2 = (18, 20, 24)
GRID = (30, 34, 42)
WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
RED = (220, 60, 60)
GREEN = (70, 200, 120)
YELLOW = (255, 215, 80)
CYAN = (90, 200, 220)
ORANGE = (255, 150, 60)

# ---------- Tiny Synth: make tones on the fly (no files) ----------
def tone(freq=440.0, secs=0.12, vol=0.25, shape="sine"):
    sr = 44100
    n = int(sr * secs)
    buf = array.array("h")
    # very light attack/decay to reduce clicks
    attack = max(1, int(n * 0.01))
    release = max(1, int(n * 0.08))
    for t in range(n):
        # waveform
        ph = 2 * math.pi * freq * t / sr
        if shape == "square":
            s = 1.0 if math.sin(ph) >= 0 else -1.0
        elif shape == "tri":
            s = 2 / math.pi * math.asin(math.sin(ph))
        elif shape == "saw":
            s = 2.0 * ((t * freq / sr) % 1) - 1.0
        else:
            s = math.sin(ph)
        # envelope
        if t < attack:
            env = t / attack
        elif t > n - release:
            env = max(0.0, (n - t) / release)
        else:
            env = 1.0
        v = int(max(-1.0, min(1.0, s * env)) * vol * 32767)
        buf.append(v); buf.append(v)
    return pygame.mixer.Sound(buffer=buf)

# SFX
sfx_shoot = tone(1200, 0.06, 0.28, "square")
sfx_reload = tone(420, 0.12, 0.22, "tri")
sfx_hit_z = tone(660, 0.08, 0.26, "sine")
sfx_headshot = tone(880, 0.09, 0.30, "square")
sfx_player_hurt = tone(180, 0.18, 0.30, "sine")
sfx_pick = tone(520, 0.09, 0.26, "sine")
sfx_gameover = tone(90, 0.7, 0.28, "saw")

# Background pad (gentle chord loop)
pad_notes = [(196, 0.035), (246.94, 0.030), (293.66, 0.028)]
for f, v in pad_notes:
    try:
        tone(f, 4.0, v, "sine").play(loops=-1)
    except Exception:
        pass

# ---------- Helpers ----------
def draw_grid():
    screen.fill(BG1)
    # subtle vignette gradient
    vg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(vg, (*BG2, 130), (0, 0, WIDTH, HEIGHT), border_radius=0)
    screen.blit(vg, (0, 0))
    # grid
    step = 40
    for x in range(0, WIDTH, step):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, step):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

def clamp(v, a, b): return a if v < a else b if v > b else v

def angle_to(a, b):
    return math.atan2(b[1]-a[1], b[0]-a[0])

def dist(a, b):
    return math.hypot(b[0]-a[0], b[1]-a[1])

# ---------- Classes ----------
class Player:
    def __init__(self):
        self.x, self.y = WIDTH//2, HEIGHT//2
        self.r = 16
        self.speed = 260
        self.hp = 100
        self.max_hp = 100
        self.mag = 12
        self.mag_max = 12
        self.reserve = 120
        self.reload_time = 0.9
        self.reload_t = 0.0
        self.reloading = False
        self.fire_cd = 0.14
        self.fire_t = 0.0

    def rect(self): return pygame.Rect(self.x-self.r, self.y-self.r, self.r*2, self.r*2)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        mx = my = 0
        if keys[pygame.K_w]: my -= 1
        if keys[pygame.K_s]: my += 1
        if keys[pygame.K_a]: mx -= 1
        if keys[pygame.K_d]: mx += 1
        if mx or my:
            l = math.hypot(mx, my)
            self.x += (mx/l) * self.speed * dt
            self.y += (my/l) * self.speed * dt
        self.x = clamp(self.x, 20, WIDTH-20)
        self.y = clamp(self.y, 20, HEIGHT-20)

        if self.fire_t > 0: self.fire_t -= dt
        if self.reloading:
            self.reload_t -= dt
            if self.reload_t <= 0:
                need = self.mag_max - self.mag
                take = min(need, self.reserve)
                self.mag += take
                self.reserve -= take
                self.reloading = False
        # Auto start reload if mag empty and reserve present
        if self.mag == 0 and self.reserve > 0 and not self.reloading:
            self.start_reload()

    def start_reload(self):
        if self.reloading or self.mag == self.mag_max or self.reserve <= 0: return
        self.reloading = True
        self.reload_t = self.reload_time
        sfx_reload.play()

    def try_shoot(self, bullets, target_pos):
        if self.reloading or self.mag <= 0 or self.fire_t > 0: return
        ang = angle_to((self.x, self.y), target_pos)
        spread = math.radians(2.3)
        ang += rand.uniform(-spread, spread)
        speed = 720
        bullets.append(Bullet(self.x, self.y, ang, speed))
        self.mag -= 1
        self.fire_t = self.fire_cd
        sfx_shoot.play()

    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        ang = angle_to((self.x, self.y), (mx, my))
        # body
        pygame.draw.circle(surf, CYAN, (int(self.x), int(self.y)), self.r)
        # head
        hx = self.x + math.cos(ang)*8
        hy = self.y + math.sin(ang)*8
        pygame.draw.circle(surf, WHITE, (int(hx), int(hy)), 8)
        # gun
        gx = self.x + math.cos(ang)*self.r
        gy = self.y + math.sin(ang)*self.r
        gx2 = gx + math.cos(ang)*18
        gy2 = gy + math.sin(ang)*18
        pygame.draw.line(surf, BLACK, (gx, gy), (gx2, gy2), 6)
        pygame.draw.line(surf, ORANGE, (gx, gy), (gx2, gy2), 3)

class Bullet:
    def __init__(self, x, y, ang, speed):
        self.x, self.y = x, y
        self.vx = math.cos(ang)*speed
        self.vy = math.sin(ang)*speed
        self.life = 0.9
        self.alive = True
        self.r = 3

    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.life -= dt
        if self.life <= 0 or self.x<0 or self.x>WIDTH or self.y<0 or self.y>HEIGHT:
            self.alive = False

    def draw(self, surf):
        pygame.draw.circle(surf, YELLOW, (int(self.x), int(self.y)), self.r)

class Zombie:
    def __init__(self, lvl=1):
        side = rand.choice(["l","r","t","b"])
        pad = 24
        if side=="l": self.x, self.y = -pad, rand.randrange(HEIGHT)
        elif side=="r": self.x, self.y = WIDTH+pad, rand.randrange(HEIGHT)
        elif side=="t": self.x, self.y = rand.randrange(WIDTH), -pad
        else: self.x, self.y = rand.randrange(WIDTH), HEIGHT+pad
        self.r = 16
        # ↓ slower movement and gentler scaling
        self.speed = rand.uniform(*ZOMBIE_SPEED_RANGE) + lvl*ZOMBIE_SPEED_PER_LEVEL
        self.hp = 2 + lvl//2
        self.headshot_r = 8

    def update(self, dt, player_pos):
        ang = angle_to((self.x, self.y), player_pos)
        self.x += math.cos(ang)*self.speed*dt
        self.y += math.sin(ang)*self.speed*dt

    def hit(self, bx, by):
        # Return score, headshot?
        d_body = math.hypot(bx-self.x, by-self.y)
        if d_body <= self.r+3:
            head = (self.x + (bx-self.x)*0.65, self.y + (by-self.y)*0.65)
            if math.hypot(bx-head[0], by-head[1]) <= self.headshot_r:
                self.hp -= 2
                return 2, True
            self.hp -= 1
            return 1, False
        return 0, False

    def draw(self, surf):
        # body
        pygame.draw.circle(surf, (90, 180, 80), (int(self.x), int(self.y)), self.r)
        # head highlight
        pygame.draw.circle(surf, (130, 220, 120), (int(self.x), int(self.y)), 8)
        # eyes
        pygame.draw.circle(surf, BLACK, (int(self.x-3), int(self.y-2)), 2)
        pygame.draw.circle(surf, BLACK, (int(self.x+3), int(self.y-2)), 2)

class Pickup:
    def __init__(self, x, y, kind):
        self.x, self.y = x, y
        self.kind = kind  # "ammo" or "med"
        self.life = 10.0
        self.r = 10

    def update(self, dt):
        self.life -= dt

    def draw(self, surf):
        if self.kind == "ammo":
            pygame.draw.circle(surf, (255, 230, 120), (int(self.x), int(self.y)), self.r)
            pygame.draw.rect(surf, BLACK, (self.x-6, self.y-3, 12, 6), border_radius=3)
        else:
            pygame.draw.circle(surf, (150, 220, 255), (int(self.x), int(self.y)), self.r)
            pygame.draw.rect(surf, WHITE, (self.x-2, self.y-6, 4, 12), border_radius=2)

# ---------- UI ----------
font_big = pygame.font.SysFont("Verdana", 34, bold=True)
font_med = pygame.font.SysFont("Verdana", 22)
font_sm = pygame.font.SysFont("Verdana", 16)

def draw_hud(p, score, level, paused, state):
    # Health bar
    pygame.draw.rect(screen, BLACK, (18, 14, 222, 20), border_radius=8)
    hw = int(218 * (p.hp / p.max_hp))
    pygame.draw.rect(screen, RED if p.hp<=30 else GREEN, (20, 16, hw, 16), border_radius=6)
    screen.blit(font_sm.render("HP", True, WHITE), (22, 16))
    # Ammo
    ammo = font_med.render(f"Ammo: {p.mag}/{p.reserve}", True, WHITE)
    screen.blit(ammo, (18, 44))
    # Score/Level
    screen.blit(font_med.render(f"Score: {score}", True, WHITE), (WIDTH-180, 16))
    screen.blit(font_sm.render(f"Level: {level}", True, WHITE), (WIDTH-180, 46))
    # Reload indicator
    if p.reloading:
        rr = font_sm.render("Reloading...", True, YELLOW)
        screen.blit(rr, (18, 70))
    if paused and state=="PLAYING":
        txt = font_big.render("PAUSED", True, WHITE)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 14))

def draw_center_text(lines, top=HEIGHT//2-80):
    for i, (t, size, col) in enumerate(lines):
        f = pygame.font.SysFont("Verdana", size, bold=True)
        s = f.render(t, True, col)
        screen.blit(s, (WIDTH//2 - s.get_width()//2, top + i * (size + 14)))

# ---------- Game State ----------
player = Player()
bullets = []
zombies = []
pickups = []
score = 0
level = 1
spawn_timer = 0
spawn_cooldown = 1.2
state = "MENU"  # MENU, PLAYING, GAME_OVER
paused = False

def reset_game():
    global player, bullets, zombies, pickups, score, level, spawn_timer, spawn_cooldown, state, paused
    player = Player()
    bullets = []
    zombies = []
    pickups = []
    score = 0
    level = 1
    spawn_timer = 0
    spawn_cooldown = 1.2
    state = "PLAYING"
    paused = False

# ---------- Loop ----------
running = True
while running:
    dt = clock.tick(FPS) / 1_000.0
    mx, my = pygame.mouse.get_pos()

    # Events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            if state == "MENU" and e.key == pygame.K_SPACE:
                reset_game()
            elif state == "GAME_OVER" and e.key == pygame.K_SPACE:
                reset_game()
            elif state == "PLAYING":
                if e.key == pygame.K_r:
                    player.start_reload()
                if e.key == pygame.K_p:
                    paused = not paused
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and state=="PLAYING" and not paused:
            player.try_shoot(bullets, (mx, my))

    # Update
    if state == "PLAYING" and not paused:
        player.update(dt)
        # bullets
        for b in bullets[:]:
            b.update(dt)
            if not b.alive: bullets.remove(b)

        # spawn zombies
        spawn_timer -= dt
        if spawn_timer <= 0:
            zombies.append(Zombie(level))
            # scale difficulty (slower overall; uses SPAWN_COOLDOWN_MIN)
            spawn_cooldown = max(SPAWN_COOLDOWN_MIN, 1.2 - level*0.06)
            spawn_timer = spawn_cooldown
            if rand.random() < 0.04 + level*0.01:
                zombies.append(Zombie(level))  # occasional double spawn

        # update zombies + collisions
        for z in zombies[:]:
            z.update(dt, (player.x, player.y))
            # zombie hits player?
            if dist((z.x, z.y), (player.x, player.y)) < z.r + player.r - 2:
                player.hp -= 12
                sfx_player_hurt.play()
                # push zombie back a little
                a = angle_to((z.x, z.y), (player.x, player.y))
                z.x -= math.cos(a)*22
                z.y -= math.sin(a)*22
                if player.hp <= 0:
                    sfx_gameover.play()
                    state = "GAME_OVER"

        # bullets vs zombies
        for z in zombies[:]:
            for b in bullets[:]:
                if dist((z.x, z.y), (b.x, b.y)) < z.r + 4:
                    sc, hs = z.hit(b.x, b.y)
                    if sc:
                        score += 15 if hs else 8
                        (sfx_headshot if hs else sfx_hit_z).play()
                        b.alive = False
                    if z.hp <= 0:
                        # small chance to drop pickup
                        if rand.random() < 0.14:
                            kind = "ammo" if rand.random()<0.6 else "med"
                            pickups.append(Pickup(z.x, z.y, kind))
                        zombies.remove(z)
                        break
            # remove dead bullets
            bullets[:] = [bb for bb in bullets if bb.alive]

        # pickups
        for p in pickups[:]:
            p.update(dt)
            if p.life <= 0:
                pickups.remove(p); continue
            if dist((p.x, p.y), (player.x, player.y)) < player.r + p.r:
                if p.kind == "ammo":
                    player.reserve += 24
                else:
                    player.hp = clamp(player.hp + 30, 0, player.max_hp)
                sfx_pick.play()
                pickups.remove(p)

        # level up gradually by score
        level = 1 + score // 120

    # Draw
    draw_grid()

    if state == "MENU":
        draw_center_text([
            ("ZOMBIE SHOOTER", 48, WHITE),
            ("WASD to move, Mouse to aim, Left Click to shoot", 22, WHITE),
            ("R to reload • P to pause", 22, WHITE),
            ("Press SPACE to Start", 28, YELLOW)
        ])
    elif state == "PLAYING":
        # draw pickups
        for p in pickups:
            p.draw(screen)
        # draw zombies
        for z in zombies:
            z.draw(screen)
        # draw bullets
        for b in bullets:
            b.draw(screen)
        # draw player + aim line
        player.draw(screen)
        a = angle_to((player.x, player.y), (mx, my))
        lx1 = (player.x + math.cos(a)*player.r, player.y + math.sin(a)*player.r)
        lx2 = (player.x + math.cos(a)*420,      player.y + math.sin(a)*420)
        pygame.draw.line(screen, (255,255,255,50), lx1, lx2, 1)

        draw_hud(player, score, level, paused, state)
    else:  # GAME_OVER
        draw_center_text([
            ("GAME OVER", 64, RED),
            (f"Score: {score}", 30, WHITE),
            ("Press SPACE to Restart", 26, YELLOW)
        ])

    pygame.display.flip()

pygame.quit()
sys.exit()
