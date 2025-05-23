import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tank Attack 3')

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Color for power boost
ORANGE = (255, 165, 0)  # Color for fireball

# Game clock
clock = pygame.time.Clock()

# Define dash properties
DASH_LENGTH = 15
SPACE_LENGTH = 10

# Song
pygame.mixer.music.load('assets/KKing_Remix.wav')  # Replace with your music file
pygame.mixer.music.play(-1)  # Play the music in a loop

# Define BlueDot class
class BlueDot:
    def __init__(self):
        self.rect = pygame.Rect(700, SCREEN_HEIGHT // 2, 50, 50)
        self.health = 200
        self.lasers = []
        self.fireball = None
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 500  # Fire every 0.5 seconds
        self.power_boosts_hit = 0  # Track power boosts hit

    def move(self, direction):
        if direction == 'up' and self.rect.top > 0:
            self.rect.y -= 5
        elif direction == 'down' and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 5

    def shoot_laser(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer >= self.shoot_delay:
            # Fire a laser to the left from the BlueDot's position
            laser_rect = pygame.Rect(self.rect.left, self.rect.centery, 5, 5)
            self.lasers.append({'rect': laser_rect, 'direction': (-1, 0)})  # Direction is left (-1, 0)
            self.shoot_timer = current_time

    def shoot_fireball(self):
        if self.power_boosts_hit >= 10 and self.fireball is None:
            # Fire a fireball towards a random tank
            self.fireball = pygame.Rect(self.rect.left, self.rect.centery, 20, 20)
            self.power_boosts_hit = 0  # Reset power boost count after shooting fireball

    def draw(self):
        pygame.draw.ellipse(screen, BLUE, self.rect)
        for laser in self.lasers:
            draw_dashed_laser(BLUE, (laser['rect'].x, laser['rect'].y), (laser['rect'].x - 100, laser['rect'].y), 2)
        if self.fireball:
            pygame.draw.circle(screen, ORANGE, (self.fireball.x, self.fireball.y), 20)

    def update(self):
        for laser in self.lasers:
            laser['rect'].x -= 5  # Move lasers to the left (towards tanks/power boosts)
            if laser['rect'].x < 0:
                self.lasers.remove(laser)
        if self.fireball:
            self.fireball.x -= 7  # Move fireball to the left
            if self.fireball.x < 0:
                self.fireball = None  # Remove fireball if it goes off screen

# Define PowerBoost class
class PowerBoost:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 600), random.randint(50, 550), 20, 20)

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

# Define Tank class
class Tank:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.health = 100
        self.lasers = []
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 500  # 2 seconds per shot

    def shoot_laser(self, target):
        # Shoot a laser towards the BlueDot
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer >= self.shoot_delay:
            laser_rect = pygame.Rect(self.rect.right, self.rect.centery, 5, 5)
            self.lasers.append({'rect': laser_rect, 'direction': self.get_direction(target)})
            self.shoot_timer = current_time

    def get_direction(self, target):
        # Calculate the unit vector for direction towards the BlueDot
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        return (dx / distance, dy / distance)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        for laser in self.lasers:
            draw_dashed_laser(RED, (laser['rect'].x, laser['rect'].y), 
                              (laser['rect'].x + 100 * laser['direction'][0], 
                               laser['rect'].y + 100 * laser['direction'][1]), 2)

    def update(self):
        for laser in self.lasers:
            # Move lasers towards the BlueDot
            laser['rect'].x += 5 * laser['direction'][0]
            laser['rect'].y += 5 * laser['direction'][1]
            if laser['rect'].x > SCREEN_WIDTH or laser['rect'].y < 0 or laser['rect'].y > SCREEN_HEIGHT:
                self.lasers.remove(laser)

# Function to draw dashed lines (like "- - - -")
def draw_dashed_laser(color, start_pos, end_pos, width=2):
    x1, y1 = start_pos
    x2, y2 = end_pos
    total_length = math.hypot(x2 - x1, y2 - y1)
    
    dash_count = int(total_length // (DASH_LENGTH + SPACE_LENGTH))
    
    for i in range(dash_count):
        start = (
            x1 + (x2 - x1) * ((i * (DASH_LENGTH + SPACE_LENGTH)) / total_length),
            y1 + (y2 - y1) * ((i * (DASH_LENGTH + SPACE_LENGTH)) / total_length)
        )
        end = (
            x1 + (x2 - x1) * (((i * (DASH_LENGTH + SPACE_LENGTH)) + DASH_LENGTH) / total_length),
            y1 + (y2 - y1) * (((i * (DASH_LENGTH + SPACE_LENGTH)) + DASH_LENGTH) / total_length)
        )
        pygame.draw.line(screen, color, start, end, width)

# Function to check collision between lasers/fireballs and targets
def check_collision(lasers, target_rect):
    for laser in lasers:
        if laser['rect'].colliderect(target_rect):  # Access the 'rect' inside the laser dict
            return True
    return False

# Main game loop
def main():
    running = True
    blue_dot = BlueDot()
    tanks = [Tank(50, 100), Tank(50, 250), Tank(50, 400), Tank(50,550)]
    power_boosts = []  # Infinite power boosts will keep being added

    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            blue_dot.move('up')
        if keys[pygame.K_DOWN]:
            blue_dot.move('down')
        if keys[pygame.K_SPACE]:
            blue_dot.shoot_laser()
        if keys[pygame.K_f]:  # Press 'f' to shoot fireball if power boosts >= 10
            blue_dot.shoot_fireball()

        blue_dot.update()
        blue_dot.draw()

        for tank in tanks[:]:
            if tank.health > 0:
                tank.shoot_laser(blue_dot)
                tank.update()
                tank.draw()
            else:
                tanks.remove(tank)  # Remove tank when its health is 0

        # Infinite power boost spawning every 2 seconds
        if pygame.time.get_ticks() % 2000 < 20:
            power_boosts.append(PowerBoost())

        # Draw power boosts and check if blue dot's lasers hit them
        for power_boost in power_boosts[:]:
            power_boost.draw()
            if check_collision(blue_dot.lasers, power_boost.rect):
                blue_dot.power_boosts_hit += 1
                power_boosts.remove(power_boost)  # Remove power boost if hit by blue dot's laser

        # Fireball collision check
        if blue_dot.fireball:  # Ensure fireball is not None before checking
            for tank in tanks:
                if tank.health > 0 and blue_dot.fireball and blue_dot.fireball.colliderect(tank.rect):
                    tank.health -= 20  # Decrease tank's health by 20 if hit by fireball
                    blue_dot.fireball = None  # Remove fireball after hitting a tank

        # Health management for both blue dot and tanks
        for laser in blue_dot.lasers:
            for tank in tanks:
                if tank.health > 0 and check_collision([laser], tank.rect):
                    tank.health -= 1  # Decrease tank's health if hit by blue dot's laser

        for tank in tanks:
            if check_collision(tank.lasers, blue_dot.rect):
                blue_dot.health -= 1  # Decrease blue dot's health if hit by a tank's laser

        # Display health
        font = pygame.font.SysFont(None, 36)
        blue_dot_health_text = font.render(str(blue_dot.health), True, BLACK)
        screen.blit(blue_dot_health_text, (blue_dot.rect.centerx, blue_dot.rect.top - 20))
        
        for tank in tanks:
            tank_health_text = font.render(str(tank.health), True, BLACK)
            screen.blit(tank_health_text, (tank.rect.centerx, tank.rect.top - 20))

        # Display power boosts hit
        power_boost_text = font.render(f'Power Boosts Hit: {blue_dot.power_boosts_hit}', True, BLACK)
        screen.blit(power_boost_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        # Reset game if health drops to zero
        if blue_dot.health <= 0 or len(tanks) == 0:
            running = False

# Run the game
if __name__ == "__main__":
    main()

