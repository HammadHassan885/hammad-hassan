import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

class Colors:
    BACKGROUND = (15, 15, 35)
    GRID = (30, 30, 50)
    SNAKE_HEAD = (50, 180, 50)  # Darker green for head
    SNAKE_BODY = (50, 200, 100)
    SNAKE_BELLY = (80, 220, 130)
    FOOD = (255, 100, 100)
    FOOD_GLOW = (255, 150, 150)
    TEXT = (240, 240, 240)
    GAME_OVER = (255, 100, 100)
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
        self.body = [(15, 10), (14, 10), (13, 10)]
        self.direction = (1, 0)
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
        new_head = ((head_x + dx) % self.grid_width, (head_y + dy) % self.grid_height)
        self.body.insert(0, new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
            
    def grow(self):
        self.grow_pending += 1
        
    def check_collision(self):
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
        pygame.display.set_caption("Modern Snake Game")
        
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
        
        self.background = self.create_gradient_background()
        
    def create_gradient_background(self):
        background = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        for y in range(self.WINDOW_HEIGHT):
            color_value = min(25, 15 + int((y / self.WINDOW_HEIGHT) * 10))
            color = (color_value, color_value, min(45, color_value + 20))
            pygame.draw.line(background, color, (0, y), (self.WINDOW_WIDTH, y))
        return background
        
    def draw_snake_head(self, x, y, direction):
        """Draw a realistic snake head with eyes, tongue, and scales"""
        pixel_x = x * self.CELL_SIZE
        pixel_y = y * self.CELL_SIZE
        
        # Snake head shape (ellipse)
        head_rect = pygame.Rect(pixel_x + 2, pixel_y + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
        
        # Main head color
        pygame.draw.ellipse(self.screen, Colors.SNAKE_HEAD, head_rect)
        
        # Head highlight
        highlight_rect = pygame.Rect(pixel_x + 4, pixel_y + 4, self.CELL_SIZE - 12, self.CELL_SIZE // 3)
        pygame.draw.ellipse(self.screen, Colors.SNAKE_BELLY, highlight_rect)
        
        # Direction-based positioning for eyes and tongue
        center_x = pixel_x + self.CELL_SIZE // 2
        center_y = pixel_y + self.CELL_SIZE // 2
        
        # Draw eyes based on direction
        eye_size = 4
        pupil_size = 2
        
        if direction == (1, 0):  # Right
            left_eye = (center_x + 3, center_y - 4)
            right_eye = (center_x + 3, center_y + 4)
            tongue_start = (center_x + self.CELL_SIZE // 2 - 2, center_y)
            tongue_end = (center_x + self.CELL_SIZE // 2 + 6, center_y)
        elif direction == (-1, 0):  # Left
            left_eye = (center_x - 3, center_y - 4)
            right_eye = (center_x - 3, center_y + 4)
            tongue_start = (center_x - self.CELL_SIZE // 2 + 2, center_y)
            tongue_end = (center_x - self.CELL_SIZE // 2 - 6, center_y)
        elif direction == (0, -1):  # Up
            left_eye = (center_x - 4, center_y - 3)
            right_eye = (center_x + 4, center_y - 3)
            tongue_start = (center_x, center_y - self.CELL_SIZE // 2 + 2)
            tongue_end = (center_x, center_y - self.CELL_SIZE // 2 - 6)
        else:  # Down
            left_eye = (center_x - 4, center_y + 3)
            right_eye = (center_x + 4, center_y + 3)
            tongue_start = (center_x, center_y + self.CELL_SIZE // 2 - 2)
            tongue_end = (center_x, center_y + self.CELL_SIZE // 2 + 6)
        
        # Draw eyes (white part)
        pygame.draw.circle(self.screen, Colors.EYE_WHITE, left_eye, eye_size)
        pygame.draw.circle(self.screen, Colors.EYE_WHITE, right_eye, eye_size)
        
        # Draw pupils (black part)
        pygame.draw.circle(self.screen, Colors.EYE_BLACK, left_eye, pupil_size)
        pygame.draw.circle(self.screen, Colors.EYE_BLACK, right_eye, pupil_size)
        
        # Draw tongue (forked)
        pygame.draw.line(self.screen, Colors.TONGUE, tongue_start, tongue_end, 2)
        
        # Fork the tongue
        if direction in [(1, 0), (-1, 0)]:  # Horizontal
            fork1 = (tongue_end[0], tongue_end[1] - 2)
            fork2 = (tongue_end[0], tongue_end[1] + 2)
        else:  # Vertical
            fork1 = (tongue_end[0] - 2, tongue_end[1])
            fork2 = (tongue_end[0] + 2, tongue_end[1])
            
        pygame.draw.line(self.screen, Colors.TONGUE, tongue_end, fork1, 1)
        pygame.draw.line(self.screen, Colors.TONGUE, tongue_end, fork2, 1)
        
        # Add nostrils
        nostril_size = 1
        if direction == (1, 0):  # Right
            nostril1 = (center_x + 2, center_y - 2)
            nostril2 = (center_x + 2, center_y + 2)
        elif direction == (-1, 0):  # Left
            nostril1 = (center_x - 2, center_y - 2)
            nostril2 = (center_x - 2, center_y + 2)
        elif direction == (0, -1):  # Up
            nostril1 = (center_x - 2, center_y - 2)
            nostril2 = (center_x + 2, center_y - 2)
        else:  # Down
            nostril1 = (center_x - 2, center_y + 2)
            nostril2 = (center_x + 2, center_y + 2)
            
        pygame.draw.circle(self.screen, (30, 30, 30), nostril1, nostril_size)
        pygame.draw.circle(self.screen, (30, 30, 30), nostril2, nostril_size)
        
    def draw_snake_body(self, x, y, index):
        """Draw snake body segments with scale pattern"""
        pixel_x = x * self.CELL_SIZE
        pixel_y = y * self.CELL_SIZE
        
        # Body segment
        body_rect = pygame.Rect(pixel_x + 3, pixel_y + 3, self.CELL_SIZE - 6, self.CELL_SIZE - 6)
        
        # Gradient effect
        intensity = max(0.4, 1 - (index / len(self.snake.body)) * 0.6)
        body_color = tuple(max(0, min(255, int(c * intensity))) for c in Colors.SNAKE_BODY)
        
        pygame.draw.ellipse(self.screen, body_color, body_rect)
        
        # Scale pattern
        scale_color = tuple(max(0, min(255, int(c * 0.8))) for c in body_color)
        for i in range(3):
            for j in range(3):
                scale_x = pixel_x + 5 + i * 6
                scale_y = pixel_y + 5 + j * 6
                if scale_x < pixel_x + self.CELL_SIZE - 3 and scale_y < pixel_y + self.CELL_SIZE - 3:
                    pygame.draw.circle(self.screen, scale_color, (scale_x, scale_y), 1)
        
    def draw_snake(self):
        """Draw the entire snake with realistic head"""
        for i, (x, y) in enumerate(self.snake.body):
            if i == 0:  # Head
                self.draw_snake_head(x, y, self.snake.direction)
            else:  # Body
                self.draw_snake_body(x, y, i)
                
    def draw_food(self):
        x, y = self.food.position
        center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = y * self.CELL_SIZE + self.CELL_SIZE // 2
        
        # Pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 3 + 2
        
        # Glow effect
        glow_surface = pygame.Surface((self.CELL_SIZE + 20, self.CELL_SIZE + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*Colors.FOOD_GLOW, 100), 
                         (self.CELL_SIZE//2 + 10, self.CELL_SIZE//2 + 10), 
                         self.CELL_SIZE//2 + pulse)
        self.screen.blit(glow_surface, (x * self.CELL_SIZE - 10, y * self.CELL_SIZE - 10))
        
        # Food
        pygame.draw.circle(self.screen, Colors.FOOD, 
                         (center_x, center_y), 
                         self.CELL_SIZE//2 - 2)
        
    def draw_menu(self):
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.UI_PANEL, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Title with emoji
        title_text = self.font.render("🐍 Modern Snake Game", True, Colors.TEXT)
        title_shadow = self.font.render("🐍 Modern Snake Game", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_text, title_rect)
        
        instructions = [
            "🎮 Use ARROW KEYS to control the snake",
            "👀 Watch the realistic snake head with eyes!",
            "🍎 Eat the glowing food to grow",
            "💀 Don't hit yourself or edges",
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
        
        game_over_text = self.font.render("🐍 Game Over!", True, Colors.GAME_OVER)
        game_over_shadow = self.font.render("🐍 Game Over!", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_shadow, (game_over_rect.x + 2, game_over_rect.y + 2))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.small_font.render(f"Final Score: {self.score}", True, Colors.TEXT)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.small_font.render("Press SPACE to restart", True, Colors.TEXT)
        restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_hud(self):
        score_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 128))
        self.screen.blit(score_bg, (10, 10))
        
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
        
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            running = self.handle_events()
            
            if self.game_state == "PLAYING":
                self.move_timer += dt
                
                if self.move_timer >= self.move_delay:
                    self.snake.move()
                    self.move_timer = 0
                    
                    if self.snake.get_head_position() == self.food.position:
                        self.score += 1
                        self.snake.grow()
                        
                        fx, fy = self.food.position
                        center_x = fx * self.CELL_SIZE + self.CELL_SIZE // 2
                        center_y = fy * self.CELL_SIZE + self.CELL_SIZE // 2
                        self.particles.add_particle(center_x, center_y, Colors.FOOD, 15)
                        
                        self.food.respawn(self.snake.body)
                        self.move_delay = max(80, self.move_delay - 3)
                        
                    if self.snake.check_collision():
                        self.game_state = "GAME_OVER"
                        
            self.particles.update()
            
            # Drawing
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