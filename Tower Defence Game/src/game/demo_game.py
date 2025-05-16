import pygame
import random
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, TOWER_TYPES, PATH_POINTS
from src.towers.tower import Tower
from src.enemies.enemy import Enemy
from src.enemies.boss_enemy import BossEnemy

class GameDemo:
    def __init__(self):
        self.towers = []
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_rate = 120  # Slower spawn rate for demo
        self.wave_number = 1
        
        # Place some random towers for the demo
        self.place_random_towers()
        
    def place_random_towers(self):
        tower_types = list(TOWER_TYPES.keys())
        for _ in range(5):  # Place 5 random towers
            x = random.randint(100, WINDOW_WIDTH - 100)
            y = random.randint(100, WINDOW_HEIGHT - 100)
            tower_type = random.choice(tower_types)
            
            # Simple check to avoid placing on path
            valid_position = True
            for i in range(len(PATH_POINTS) - 1):
                start = pygame.math.Vector2(PATH_POINTS[i])
                end = pygame.math.Vector2(PATH_POINTS[i + 1])
                pos = pygame.math.Vector2(x, y)
                
                line_vec = end - start
                point_vec = pos - start
                line_len = line_vec.length()
                
                if line_len:
                    proj = point_vec.dot(line_vec) / line_len
                    proj = max(0, min(proj, line_len))
                    closest = start + (line_vec * proj / line_len)
                    distance = (pos - closest).length()
                    
                    if distance < 50:  # Keep away from path
                        valid_position = False
                        break
            
            if valid_position:
                self.towers.append(Tower(x, y, tower_type))
    
    def update(self):
        # Spawn enemies
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0
            if random.random() < 0.1:  # 10% chance for boss
                self.enemies.append(BossEnemy(self.wave_number))
            else:
                self.enemies.append(Enemy(self.wave_number))
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.reached_end or enemy.health <= 0:
                self.enemies.remove(enemy)
                
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies)
    
    def draw(self, screen):
        # Draw path
        path_width = 40
        for i in range(len(PATH_POINTS) - 1):
            start_pos = PATH_POINTS[i]
            end_pos = PATH_POINTS[i + 1]
            pygame.draw.line(screen, (139, 69, 19), start_pos, end_pos, path_width)
        
        # Draw towers and their projectiles
        for tower in self.towers:
            tower.draw(screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)