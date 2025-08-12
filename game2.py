import pygame
import sys
import random
import math
from enum import Enum
from collections import deque

# Initialize Pygame
pygame.init()

# Modern color scheme with safe color values
class Colors:
    BACKGROUND = (15, 15, 35)
    GRID = (30, 30, 50)
    SNAKE_HEAD = (100, 255, 150)
    SNAKE_BODY = (50, 200, 100)
    FOOD = (255, 100, 100)
    FOOD_GLOW = (255, 150, 150)
    TEXT = (240, 240, 240)
    GAME_OVER = (255, 100, 100)
    PARTICLE = (255, 255, 100)
    UI_PANEL = (25, 25, 45)

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
            
            # Create a surface for the particle with proper alpha
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color[:3], alpha), (size, size), size)
            screen.blit(particle_surface, (int(self.x - size), int(self.y - size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particle(self, x, y, color, count=10):
        for _ in range(count):
            velocity = [
                random.uniform(-3, 3),
                random.uniform(-3, 3)
            ]
            lifetime = random.uniform(30, 60)  # frames
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
        
        # Create gradient background
        self.background = self.create_gradient_background()
        
    def create_gradient_background(self):
        background = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        for y in range(self.WINDOW_HEIGHT):
            color_value = min(25, 15 + int((y / self.WINDOW_HEIGHT) * 10))
            color = (color_value, color_value, min(45, color_value + 20))
            pygame.draw.line(background, color, (0, y), (self.WINDOW_WIDTH, y))
        return background
        
    def draw_rounded_rect(self, surface, color, rect, radius, width=0):
        """Draw a rounded rectangle"""
        x, y, w, h = rect
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius, width)
        pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius, width)
        pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius, width)
        pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius, width)
        
        pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h), width)
        pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius), width)
        
    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake.body):
            pixel_x = x * self.CELL_SIZE
            pixel_y = y * self.CELL_SIZE
            
            if i == 0:  # Head
                color = Colors.SNAKE_HEAD
                # Glow effect
                glow_size = self.CELL_SIZE + 10
                glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*Colors.SNAKE_HEAD, 50), 
                                 (glow_size//2, glow_size//2), glow_size//2)
                self.screen.blit(glow_surface, (pixel_x - 5, pixel_y - 5))
            else:
                # Gradient body
                intensity = max(0.4, 1 - (i / len(self.snake.body)) * 0.6)
                color = tuple(max(0, min(255, int(c * intensity))) for c in Colors.SNAKE_BODY)
                
            # Draw snake segment
            segment_rect = pygame.Rect(pixel_x + 2, pixel_y + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            self.draw_rounded_rect(self.screen, color, segment_rect, 5)
            
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
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.UI_PANEL, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Title with shadow
        title_text = self.font.render("Modern Snake Game", True, Colors.TEXT)
        title_shadow = self.font.render("Modern Snake Game", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "🎮 Use ARROW KEYS to control the snake",
            "🍎 Eat the glowing food to grow",
            "💀 Don't hit yourself or edges",
            "🚀 Press SPACE to start"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, Colors.TEXT)
            rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 20 + i * 30))
            self.screen.blit(text, rect)
            
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.UI_PANEL, 220))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text with shadow
        game_over_text = self.font.render("Game Over!", True, Colors.GAME_OVER)
        game_over_shadow = self.font.render("Game Over!", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_shadow, (game_over_rect.x + 2, game_over_rect.y + 2))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.small_font.render(f"Final Score: {self.score}", True, Colors.TEXT)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Press SPACE to restart", True, Colors.TEXT)
        restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_hud(self):
        # Score background
        score_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 128))
        self.screen.blit(score_bg, (10, 10))
        
        # Score text
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
                    
                    # Check food collision
                    if self.snake.get_head_position() == self.food.position:
                        self.score += 1
                        self.snake.grow()
                        
                        # Add particles at food position
                        fx, fy = self.food.position
                        center_x = fx * self.CELL_SIZE + self.CELL_SIZE // 2
                        center_y = fy * self.CELL_SIZE + self.CELL_SIZE // 2
                        self.particles.add_particle(center_x, center_y, Colors.FOOD, 15)
                        
                        self.food.respawn(self.snake.body)
                        
                        # Increase difficulty
                        self.move_delay = max(80, self.move_delay - 3)
                        
                    # Check collision
                    if self.snake.check_collision():
                        self.game_state = "GAME_OVER"
                        
            self.particles.update()
            
            # Drawing
            self.screen.blit(self.background, (0, 0))
            
            if self.game_state == "MENU":
                self.draw_menu()
            elif self.game_state == "PLAYING":
                # Draw game area
                game_area = pygame.Rect(0, 0, self.GRID_WIDTH * self.CELL_SIZE, self.GRID_HEIGHT * self.CELL_SIZE)
                pygame.draw.rect(self.screen, (20, 20, 40), game_area)
                
                # Draw grid
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