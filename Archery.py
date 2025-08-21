import pygame, math, random, array

# ---------- init ----------
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
WIDTH, HEIGHT = 900, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery — Shooter Boy Edition 🎯")
clock = pygame.time.Clock()
FPS = 60

# ---------- colors ----------
WHITE=(245,245,245); BLACK=(25,25,25)
SKY=(185,220,255); GRASS=(98,172,90)
WOOD=(150,100,60); LITE=(230,230,230)
YELLOW=(255,215,0); RED=(225,60,60); BLUE=(60,100,220); DARK=(70,70,70)
BUTTON_BG=(50,150,255); BUTTON_HOVER=(80,180,255)

# ---------- tiny synth ----------
def tone(freq, secs, vol=0.18, shape="sine"):
    sr=44100; n=int(sr*secs)
    buf=array.array("h")
    for t in range(n):
        if shape=="sine": s=math.sin(2*math.pi*freq*t/sr)
        elif shape=="square": s=1.0 if ((t*freq*2)//sr)%2==0 else -1.0
        else: s=math.sin(2*math.pi*freq*t/sr)
        v=int(s*vol*32767)
        buf.append(v); buf.append(v)
    return pygame.mixer.Sound(buffer=buf)

sfx_shoot = tone(900, 0.07, 0.22, "square")
sfx_hit   = tone(660, 0.12, 0.24, "sine")

# ---------- draw helpers ----------
def draw_bg():
    screen.fill(SKY)
    pygame.draw.rect(screen, GRASS, (0, HEIGHT-90, WIDTH, 90))
    pygame.draw.circle(screen, (150,205,170), (140, HEIGHT-50), 170)
    pygame.draw.circle(screen, (150,205,170), (430, HEIGHT-55), 210)
    pygame.draw.circle(screen, (150,205,170), (760, HEIGHT-45), 190)

def draw_button(rect, text, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_BG
    pygame.draw.rect(screen, color, rect, border_radius=8)
    label = font_big.render(text, True, WHITE)
    screen.blit(label, (rect.x + rect.width//2 - label.get_width()//2,
                        rect.y + rect.height//2 - label.get_height()//2))

# ---------- classes ----------
class Target:
    def __init__(self):
        self.x = WIDTH-160
        self.base_y = HEIGHT//2
        self.y = self.base_y
        self.vy = 1.7
        self.range = 120
        self.rings = [70,58,46,34,22,10]
        self.colors = [WHITE, DARK, LITE, BLUE, RED, YELLOW]

    def update(self):
        self.y += self.vy
        if self.y < self.base_y - self.range or self.y > self.base_y + self.range:
            self.vy *= -1

    def draw(self, surf):
        sh = pygame.Surface((200,140), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0,0,0,70), (20,100,160,30))
        surf.blit(sh, (self.x-100, self.y-60))
        pygame.draw.rect(surf, WOOD, (self.x-10, self.y+70, 20, 70), border_radius=6)
        pygame.draw.rect(surf, WOOD, (self.x-55, self.y+120, 110, 16), border_radius=8)
        for r,c in zip(self.rings, self.colors):
            pygame.draw.circle(surf, c, (int(self.x), int(self.y)), r)
            pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y)), r, 2)
        pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y)), 4)

    def score_for_point(self, px, py):
        d = math.hypot(px - self.x, py - self.y)
        if d <= 10: return 50
        if d <= 22: return 25
        if d <= 34: return 15
        if d <= 46: return 10
        if d <= 58: return 5
        if d <= 70: return 2
        return 0

class Bow:
    def __init__(self):
        self.x = 120
        self.y = HEIGHT-100

    def update(self, mouse_pos):
        _, my = mouse_pos
        self.y += (my - self.y) * 0.22

    def draw(self, surf, aim_angle, charge_t):
        radius = 80
        rect = pygame.Rect(self.x - radius, self.y - radius, radius*2, radius*2)
        pygame.draw.arc(surf, WOOD, rect, 1.05*math.pi, 1.95*math.pi, 8)
        pygame.draw.arc(surf, (180,120,70), rect.inflate(-10,-10), 1.05*math.pi, 1.95*math.pi, 5)
        top = (self.x - radius*math.cos(math.radians(60)),
               self.y - radius*math.sin(math.radians(60)))
        bot = (self.x - radius*math.cos(math.radians(300)),
               self.y - radius*math.sin(math.radians(300)))
        pull = 0 + 100*charge_t
        notch = (self.x + pull*math.cos(aim_angle), self.y + pull*math.sin(aim_angle))
        pygame.draw.line(surf, (230,230,230), top, notch, 2)
        pygame.draw.line(surf, (230,230,230), bot, notch, 2)
        pygame.draw.rect(surf, (70,50,30), (self.x-8, self.y-26, 16, 52), border_radius=6)

class Arrow:
    def __init__(self, x, y, ang, speed):
        self.x, self.y, self.ang = x, y, ang
        self.vx = speed*math.cos(ang)
        self.vy = speed*math.sin(ang)
        self.g  = 640.0
        self.len = 34
        self.alive = True

    def update(self, dt):
        self.vy += self.g*dt
        self.x  += self.vx*dt
        self.y  += self.vy*dt
        self.ang = math.atan2(self.vy, self.vx)
        if self.x<-60 or self.x>WIDTH+80 or self.y>HEIGHT+120:
            self.alive = False

    def tip(self):
        return (self.x + self.len*math.cos(self.ang),
                self.y + self.len*math.sin(self.ang))

    def draw(self, surf):
        tail=(self.x - 8*math.cos(self.ang), self.y - 8*math.sin(self.ang))
        tip = self.tip()
        pygame.draw.line(surf, (90,60,40), tail, tip, 3)
        tri = 10
        p1=tip
        p2=(tip[0]-tri*math.cos(self.ang-math.radians(12)), tip[1]-tri*math.sin(self.ang-math.radians(12)))
        p3=(tip[0]-tri*math.cos(self.ang+math.radians(12)), tip[1]-tri*math.sin(self.ang+math.radians(12)))
        pygame.draw.polygon(surf, (200,200,200), [p1,p2,p3]); pygame.draw.polygon(surf, BLACK, [p1,p2,p3],1)
        fb=(tail[0]-4*math.cos(self.ang), tail[1]-4*math.sin(self.ang))
        l=(fb[0]+10*math.cos(self.ang+math.radians(150)), fb[1]+10*math.sin(self.ang+math.radians(150)))
        r=(fb[0]+10*math.cos(self.ang-math.radians(150)), fb[1]+10*math.sin(self.ang-math.radians(150)))
        pygame.draw.polygon(surf, (230,40,40), [tail,l,fb])
        pygame.draw.polygon(surf, (40,120,230), [tail,r,fb])

# Shooter boy
shooter_img = pygame.Surface((40,40))
shooter_img.fill((50,150,255))
pygame.draw.rect(shooter_img,(0,0,0),(5,5,30,30))

# ---------- HUD ----------
font_big  = pygame.font.SysFont("Arial", 34, bold=True)
font_med  = pygame.font.SysFont("Arial", 22)
good_font = pygame.font.SysFont("Arial", 62, bold=True)

def draw_hud(score, shots_left, charge_t, charging, good_timer):
    screen.blit(font_big.render(f"Score: {score}", True, BLACK), (16, 12))
    screen.blit(font_med.render(f"Shots Left: {shots_left}", True, BLACK), (18, 48))
    bw,bh=210,14; x,y=16,78
    pygame.draw.rect(screen, BLACK, (x-2,y-2,bw+4,bh+4), 2, border_radius=6)
    pygame.draw.rect(screen, BLUE,  (x,y,int(bw*charge_t),bh), border_radius=4)
    screen.blit(shooter_img, (80, HEIGHT-80))
    if good_timer>0:
        gt = good_font.render("GOOD SHOT!", True, (0,180,0))
        screen.blit(gt, (WIDTH//2 - gt.get_width()//2, 40))

# ---------- game state ----------
bow = Bow()
target = Target()
arrows=[]
score=0
shots_left = 10
charging=False
charge_t=0.0
CHARGE_RATE=0.95
SPEED_MIN=380.0
SPEED_MAX=920.0
good_timer=0
game_over = False
game_started = False  # start screen

# Buttons
start_button = pygame.Rect(WIDTH//2-100, HEIGHT//2-40, 200, 60)
restart_button = pygame.Rect(WIDTH//2-100, HEIGHT//2+20, 200, 60)

# ---------- main loop ----------
running=True
while running:
    dt = clock.tick(FPS)/1000.0
    mouse_pos = pygame.mouse.get_pos()
    mx,my = mouse_pos

    for e in pygame.event.get():
        if e.type == pygame.QUIT: running=False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE: running=False
            elif e.key == pygame.K_SPACE: charging=True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE and charging and game_started and not game_over:
                angle = math.atan2(mouse_pos[1]-bow.y, mouse_pos[0]-bow.x)
                angle = max(-math.radians(35), min(math.radians(35), angle))
                speed = SPEED_MIN + (SPEED_MAX-SPEED_MIN)*max(0,min(1,charge_t))
                arrows.append(Arrow(bow.x, bow.y, angle, speed))
                sfx_shoot.play(); shots_left -= 1
                charging=False; charge_t=0.0
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button==1:
            if not game_started and start_button.collidepoint(mx,my):
                game_started = True
                game_over = False
                score = 0
                shots_left = 10
                arrows.clear()
                target.y = target.base_y
            elif game_over and restart_button.collidepoint(mx,my):
                game_over = False
                game_started = True
                score = 0
                shots_left = 10
                arrows.clear()
                target.y = target.base_y
            elif game_started and not game_over:
                charging=True
        elif e.type == pygame.MOUSEBUTTONUP and e.button==1 and charging and game_started and not game_over:
            angle = math.atan2(mouse_pos[1]-bow.y, mouse_pos[0]-bow.x)
            angle = max(-math.radians(35), min(math.radians(35), angle))
            speed = SPEED_MIN + (SPEED_MAX-SPEED_MIN)*max(0,min(1,charge_t))
            arrows.append(Arrow(bow.x, bow.y, angle, speed))
            sfx_shoot.play(); shots_left -= 1
            charging=False; charge_t=0.0

    if charging and game_started: charge_t = min(1.0, charge_t + CHARGE_RATE*dt)

    # ---------- game updates ----------
    if game_started and not game_over:
        bow.update(mouse_pos)
        target.update()
        for a in arrows[:]:
            a.update(dt)
            tip = a.tip()
            pts = target.score_for_point(*tip)
            if pts > 0:
                score += pts
                sfx_hit.play()
                good_timer = 60 if pts>=15 else 40
                arrows.remove(a)  # arrow disappears instantly
                target.y = max(90, min(HEIGHT-90, target.y + random.randint(-22,22)))
            elif tip[0] > WIDTH or tip[0] < 0 or tip[1] > HEIGHT:
                game_over = True
            if not a.alive: arrows.remove(a)
        if good_timer>0: good_timer -= 1
        if shots_left <= 0: game_over = True

    # ---------- draw ----------
    draw_bg()
    if not game_started:
        draw_button(start_button, "START GAME", start_button.collidepoint(mx,my))
    else:
        target.draw(screen)
        if charging:
            prev = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ang = math.atan2(mouse_pos[1]-bow.y, mouse_pos[0]-bow.x)
            ang = max(-math.radians(35), min(math.radians(35), ang))
            spd = SPEED_MIN + (SPEED_MAX-SPEED_MIN)*charge_t
            vx,vy = spd*math.cos(ang), spd*math.sin(ang); g=640
            px,py = bow.x,bow.y; t=0.0
            for _ in range(26):
                t += 0.07
                qx = px + vx*t
                qy = py + vy*t + 0.5*g*t*t
                pygame.draw.circle(prev, (0,0,0,90), (int(qx), int(qy)), 3)
                if qx>WIDTH or qy>HEIGHT+30: break
            screen.blit(prev,(0,0))
        for a in arrows: a.draw(screen)
        aim = math.atan2(mouse_pos[1]-bow.y, mouse_pos[0]-bow.x)
        aim = max(-math.radians(35), min(math.radians(35), aim))
        bow.draw(screen, aim, charge_t)
        draw_hud(score, shots_left, charge_t, charging, good_timer)
        if game_over:
            draw_button(restart_button, "RESTART", restart_button.collidepoint(mx,my))
            go_txt = good_font.render("GAME OVER!", True, RED)
            screen.blit(go_txt, (WIDTH//2 - go_txt.get_width()//2, HEIGHT//2 - 100))

    pygame.display.flip()

pygame.quit()
