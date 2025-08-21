import pygame, sys, math, random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 640, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Shooter")

# Colors
COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),
          (255,0,255),(0,255,255),(255,165,0)]
WHITE = (255,255,255)
GRAY = (30,30,30)
RED = (255,50,50)

# Settings
FPS = 60
RADIUS = 20
ROWS = 8
COLS = WIDTH // (RADIUS*2)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,36)

# Bubble class
class Bubble:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.radius=RADIUS
        self.rect=pygame.Rect(self.x-self.radius,self.y-self.radius,
                              self.radius*2,self.radius*2)
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        pygame.draw.circle(win,WHITE,(self.x,self.y),self.radius,2)

# Shooter boy
shooter_img = pygame.Surface((40,40))
shooter_img.fill((50,150,255))
pygame.draw.rect(shooter_img,(0,0,0),(5,5,30,30)) # simple boy

# Create initial grid
def create_grid():
    grid=[]
    for row in range(ROWS):
        row_bubbles=[]
        for col in range(COLS):
            if row<5:
                x=col*RADIUS*2+RADIUS
                y=row*RADIUS*2+RADIUS
                color=random.choice(COLORS)
                row_bubbles.append(Bubble(x,y,color))
            else:
                row_bubbles.append(None)
        grid.append(row_bubbles)
    return grid

grid=create_grid()

# Launcher
launcher_x = WIDTH//2
launcher_y = HEIGHT - 60
launcher_angle = 90
current_bubble = Bubble(launcher_x, launcher_y, random.choice(COLORS))
shooting = False
velocity = [0,0]

score = 0
shots_left = 30  # limited shots
game_over = False

def get_angle(mouse_pos):
    mx,my=mouse_pos
    dx=mx-launcher_x
    dy=my-launcher_y
    angle=math.degrees(math.atan2(-dy,dx))
    return max(20,min(160,angle))

def shoot_bubble():
    global velocity
    rad=math.radians(launcher_angle)
    velocity=[math.cos(rad)*10,-math.sin(rad)*10]

def check_collision(bub):
    for row in grid:
        for cell in row:
            if cell and math.hypot(cell.x-bub.x,cell.y-bub.y)<RADIUS*2-2:
                return True
    return False

def snap_to_grid(bub):
    row=round((bub.y-RADIUS)/(RADIUS*2))
    col=round((bub.x-RADIUS)/(RADIUS*2))
    if row>=len(grid):
        grid.append([None]*COLS)
    if grid[row][col] is None:
        grid[row][col]=Bubble(col*RADIUS*2+RADIUS,row*RADIUS*2+RADIUS,bub.color)
    return row,col

def draw_grid(win):
    for row in grid:
        for cell in row:
            if cell:
                cell.draw(win)

def get_group(row,col,color,visited=None):
    if visited is None:
        visited=set()
    if row<0 or row>=len(grid) or col<0 or col>=COLS: return visited
    cell=grid[row][col]
    if not cell or cell.color!=color or (row,col) in visited: return visited
    visited.add((row,col))
    get_group(row+1,col,color,visited)
    get_group(row-1,col,color,visited)
    get_group(row,col+1,color,visited)
    get_group(row,col-1,color,visited)
    return visited

def remove_floating():
    visited=set()
    for col in range(COLS):
        if grid[0][col]:
            dfs(0,col,visited)
    for r in range(len(grid)):
        for c in range(COLS):
            if grid[r][c] and (r,c) not in visited:
                grid[r][c]=None

def dfs(r,c,visited):
    if r<0 or r>=len(grid) or c<0 or c>=COLS: return
    if (r,c) in visited: return
    if not grid[r][c]: return
    visited.add((r,c))
    dfs(r+1,c,visited)
    dfs(r-1,c,visited)
    dfs(r,c+1,visited)
    dfs(r,c-1,visited)

# Main loop
running=True
while running:
    screen.fill(GRAY)
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.MOUSEMOTION:
            launcher_angle=get_angle(pygame.mouse.get_pos())
        if event.type==pygame.MOUSEBUTTONDOWN and not shooting and not game_over and shots_left>0:
            shooting=True
            shoot_bubble()
            shots_left-=1

    if not game_over:
        if shooting:
            current_bubble.x+=velocity[0]
            current_bubble.y+=velocity[1]
            if current_bubble.x<=RADIUS or current_bubble.x>=WIDTH-RADIUS:
                velocity[0]*=-1
            if current_bubble.y<=RADIUS or check_collision(current_bubble):
                row,col=snap_to_grid(current_bubble)
                group=get_group(row,col,current_bubble.color)
                if len(group)>=3:
                    for r,c in group:
                        grid[r][c]=None
                    score+=len(group)*10
                    remove_floating()
                current_bubble=Bubble(launcher_x,launcher_y,random.choice(COLORS))
                shooting=False

    # check game over
    for c in range(COLS):
        if grid[ROWS-1][c]:
            game_over=True
    if shots_left==0 and not shooting:
        game_over=True

    # draw
    draw_grid(screen)
    if not game_over:
        current_bubble.draw(screen)
        # draw shooter boy
        screen.blit(shooter_img,(launcher_x-20,launcher_y+20))
        pygame.draw.line(screen,WHITE,(launcher_x,launcher_y),
                         (launcher_x+math.cos(math.radians(launcher_angle))*50,
                          launcher_y-math.sin(math.radians(launcher_angle))*50),3)

    # Score display
    score_text=font.render(f"Score: {score}",True,WHITE)
    screen.blit(score_text,(10,10))
    shots_text=font.render(f"Shots: {shots_left}",True,WHITE)
    screen.blit(shots_text,(WIDTH-150,10))

    # Game over
    if game_over:
        over_text=font.render("GAME OVER",True,RED)
        screen.blit(over_text,(WIDTH//2-over_text.get_width()//2,HEIGHT//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
