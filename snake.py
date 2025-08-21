import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

class Colors:
    BACKGROUND = (15, 15, 35)
    GRID = (30, 30, 50)
    SNAKE_HEAD = (50, 180, 50)
    SNAKE_BODY = (50, 200, 100)
    SNAKE_BELLY = (80, 220, 130)
    FOOD = (255, 100, 100)
    FOOD_GLOW = (255, 150, 150)
    TEXT = (240, 240, 240)
    GAME_OVER = (255, 100, 100)
    WALL_WARNING = (255, 200, 50)
    PARTICLE = (255, 255, 100)
    UI_PANEL = (25, 25, 45)
    EYE_WHITE = (255, 255, 255)
    EYE_BLACK = (0, 0, 0)
    TONGUE = (220, 50, 50)

class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.uniform(2, 6)
        
    def update(self, dt):
        self.x += self.velocity[0] * dt * 60
        self.y += self.velocity[1] * dt * 60
        self.lifetime -= dt * 60
        self.size *= 0.98
        
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = max(0, min(255, int(255 * (self.lifetime / self.max_lifetime))))
            size = max(1, int(self.size))
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color[:3], alpha), (size, size), size)
            screen.blit(particle_surface, (int(self.x - size), int(self.y - size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particle(self, x, y, color, count=10):
        for _ in range(count):
            velocity = [random.uniform(-3, 3), random.uniform(-3, 3)]
            lifetime = random.uniform(30, 60)
            self.particles.append(Particle(x, y, color, velocity, lifetime))
            
    def add_explosion(self, x, y, color, count=20):
        for _ in range(count):
            velocity = [random.uniform(-8, 8), random.uniform(-8, 8)]
            lifetime = random.uniform(20, 40)
            self.particles.append(Particle(x, y, color, velocity, lifetime))
            
    def update(self):
        self.particles = [p for p in self.particles if p.lifetime > 0 and p.size > 0.5]
        for particle in self.particles:
            particle.update(1)
            
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

class Snake:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.reset()
        
    def reset(self):
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = (1, 0)  # Right
        self.next_direction = (1, 0)
        self.grow_pending = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif keys[pygame.K_DOWN] and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif keys[pygame.K_LEFT] and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and self.direction != (-1, 0):
            self.next_direction = (1, 0)
            
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Wall collision detection
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or 
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            return "WALL_COLLISION"
            
        self.body.insert(0, new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
            
        return "OK"
        
    def grow(self):
        self.grow_pending += 1
        
    def check_self_collision(self):
        head = self.body[0]
        return head in self.body[1:]
        
    def get_head_position(self):
        return self.body[0]

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.random_position()
        
    def random_position(self):
        return (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
        
    def respawn(self, snake_body):
        while True:
            self.position = self.random_position()
            if self.position not in snake_body:
                break

class ModernSnakeGame:
    def __init__(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.GRID_WIDTH = 32
        self.GRID_HEIGHT = 24
        self.CELL_SIZE = 25
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Wall Collision Mode")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.snake = Snake(self.GRID_WIDTH, self.GRID_HEIGHT)
        self.food = Food(self.GRID_WIDTH, self.GRID_HEIGHT)
        self.particles = ParticleSystem()
        
        self.score = 0
        self.game_state = "MENU"
        self.move_timer = 0
        self.move_delay = 150
        
        self.wall_collision_pos = None
        self.background = self.create_gradient_background()
        
    def create_gradient_background(self):
        background = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        for y in range(self.WINDOW_HEIGHT):
            color_value = min(25, 15 + int((y / self.WINDOW_HEIGHT) * 10))
            color = (color_value, color_value, min(45, color_value + 20))
            pygame.draw.line(background, color, (0, y), (self.WINDOW_WIDTH, y))
        return background
        
    def draw_snake_head(self, x, y, direction):
        pixel_x = x * self.CELL_SIZE
        pixel_y = y * self.CELL_SIZE
        
        head_rect = pygame.Rect(pixel_x + 2, pixel_y + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
        pygame.draw.ellipse(self.screen, Colors.SNAKE_HEAD, head_rect)
        
        highlight_rect = pygame.Rect(pixel_x + 4, pixel_y + 4, self.CELL_SIZE - 12, self.CELL_SIZE // 3)
        pygame.draw.ellipse(self.screen, Colors.SNAKE_BELLY, highlight_rect)
        
        center_x = pixel_x + self.CELL_SIZE // 2
        center_y = pixel_y + self.CELL_SIZE // 2
        
        eye_size = 4
        pupil_size = 2
        
        if direction == (1, 0):  # Right
            left_eye = (center_x + 3, center_y - 4)
            right_eye = (center_x + 3, center_y + 4)
        elif direction == (-1, 0):  # Left
            left_eye = (center_x - 3, center_y - 4)
            right_eye = (center_x - 3, center_y + 4)
        elif direction == (0, -1):  # Up
            left_eye = (center_x - 4, center_y - 3)
            right_eye = (center_x + 4, center_y - 3)
        else:  # Down
            left_eye = (center_x - 4, center_y + 3)
            right_eye = (center_x + 4, center_y + 3)
        
        pygame.draw.circle(self.screen, Colors.EYE_WHITE, left_eye, eye_size)
        pygame.draw.circle(self.screen, Colors.EYE_WHITE, right_eye, eye_size)
        pygame.draw.circle(self.screen, Colors.EYE_BLACK, left_eye, pupil_size)
        pygame.draw.circle(self.screen, Colors.EYE_BLACK, right_eye, pupil_size)
        
    def draw_snake_body(self, x, y, index):
        pixel_x = x * self.CELL_SIZE
        pixel_y = y * self.CELL_SIZE
        
        body_rect = pygame.Rect(pixel_x + 3, pixel_y + 3, self.CELL_SIZE - 6, self.CELL_SIZE - 6)
        intensity = max(0.4, 1 - (index / len(self.snake.body)) * 0.6)
        body_color = tuple(max(0, min(255, int(c * intensity))) for c in Colors.SNAKE_BODY)
        
        pygame.draw.ellipse(self.screen, body_color, body_rect)
                
    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake.body):
            if i == 0:
                self.draw_snake_head(x, y, self.snake.direction)
            else:
                self.draw_snake_body(x, y, i)
                
    def draw_food(self):
        x, y = self.food.position
        center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = y * self.CELL_SIZE + self.CELL_SIZE // 2
        
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 3 + 2
        
        glow_surface = pygame.Surface((self.CELL_SIZE + 20, self.CELL_SIZE + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*Colors.FOOD_GLOW, 100), 
                         (self.CELL_SIZE//2 + 10, self.CELL_SIZE//2 + 10), 
                         self.CELL_SIZE//2 + pulse)
        self.screen.blit(glow_surface, (x * self.CELL_SIZE - 10, y * self.CELL_SIZE - 10))
        
        pygame.draw.circle(self.screen, Colors.FOOD, 
                         (center_x, center_y), 
                         self.CELL_SIZE//2 - 2)
        
    def draw_menu(self):
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.UI_PANEL, 220))
        self.screen.blit(overlay, (0, 0))
        
        title_text = self.font.render("🐍 Snake Game - Wall Mode", True, Colors.TEXT)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(title_text, title_rect)
        
        instructions = [
            "🎮 Use ARROW KEYS to control the snake",
            "🧱 Hitting walls = GAME OVER",
            "🍎 Eat the glowing food to grow",
            "🚀 Press SPACE to start"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, Colors.TEXT)
            rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 20 + i * 30))
            self.screen.blit(text, rect)
            
    def draw_game_over(self):
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.UI_PANEL, 220))
        self.screen.blit(overlay, (0, 0))
        
        if self.wall_collision_pos:
            fx, fy = self.wall_collision_pos
            center_x = fx * self.CELL_SIZE + self.CELL_SIZE // 2
            center_y = fy * self.CELL_SIZE + self.CELL_SIZE // 2
            self.particles.add_explosion(center_x, center_y, Colors.GAME_OVER, 50)
        
        game_over_text = self.font.render("💥 Wall Collision!", True, Colors.GAME_OVER)
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.small_font.render(f"Final Score: {self.score}", True, Colors.TEXT)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.small_font.render("Press SPACE to restart", True, Colors.TEXT)
        restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, Colors.TEXT)
        self.screen.blit(score_text, (20, 20))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "MENU" and event.key == pygame.K_SPACE:
                    self.game_state = "PLAYING"
                elif self.game_state == "GAME_OVER" and event.key == pygame.K_SPACE:
                    self.reset_game()
                elif self.game_state == "PLAYING":
                    self.snake.update()
                    
        return True
        
    def reset_game(self):
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.score = 0
        self.game_state = "PLAYING"
        self.move_delay = 150
        self.particles = ParticleSystem()
        self.wall_collision_pos = None
        
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            running = self.handle_events()
            
            if self.game_state == "PLAYING":
                self.move_timer += dt
                
                if self.move_timer >= self.move_delay:
                    move_result = self.snake.move()
                    
                    if move_result == "WALL_COLLISION":
                        self.wall_collision_pos = self.snake.body[0]
                        self.game_state = "GAME_OVER"
                    elif self.snake.check_self_collision():
                        self.wall_collision_pos = self.snake.body[0]
                        self.game_state = "GAME_OVER"
                    else:
                        if self.snake.get_head_position() == self.food.position:
                            self.score += 1
                            self.snake.grow()
                            self.food.respawn(self.snake.body)
                            self.move_delay = max(80, self.move_delay - 3)
                    
                    self.move_timer = 0
                        
            self.particles.update()
            
            self.screen.blit(self.background, (0, 0))
            
            if self.game_state == "MENU":
                self.draw_menu()
            elif self.game_state == "PLAYING":
                game_area = pygame.Rect(0, 0, self.GRID_WIDTH * self.CELL_SIZE, self.GRID_HEIGHT * self.CELL_SIZE)
                pygame.draw.rect(self.screen, (20, 20, 40), game_area)
                
                for x in range(self.GRID_WIDTH):
                    for y in range(self.GRID_HEIGHT):
                        rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                        pygame.draw.rect(self.screen, Colors.GRID, rect, 1)
                
                self.draw_food()
                self.draw_snake()
                self.particles.draw(self.screen)
                self.draw_hud()
                
            elif self.game_state == "GAME_OVER":
                self.draw_game_over()
                
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ModernSnakeGame()
    game.run() 