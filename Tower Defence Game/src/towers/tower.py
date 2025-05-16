import pygame
import math
from constants import TOWER_TYPES
from .projectile import Projectile

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type
        self.stats = TOWER_TYPES[tower_type].copy()
        self.target = None
        self.fire_cooldown = 0
        self.show_range = False
        self.projectiles = []
        self.upgrades = {}
        self.rotation = 0
        self.pulse_angle = 0
        
    def update(self, enemies):
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.dead:
                self.projectiles.remove(projectile)
        
        # Update firing cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
            
        # Find target if none exists or current target is dead/out of range
        if not self.target or self.target.health <= 0 or self.get_distance_to(self.target) > self.stats["range"]:
            self.find_target(enemies)
            
        # Attack target if it exists and cooldown is ready
        if self.target and self.fire_cooldown <= 0:
            self.fire_at_target()
            
        # Update visual effects
        self.pulse_angle += 0.1
            
    def find_target(self, enemies):
        self.target = None
        min_distance = float('inf')
        
        for enemy in enemies:
            if enemy.health <= 0:
                continue
                
            distance = self.get_distance_to(enemy)
            if distance <= self.stats["range"] and distance < min_distance:
                self.target = enemy
                min_distance = distance
                
    def fire_at_target(self):
        # Calculate direction to target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        angle = math.atan2(dy, dx)
        
        # Update tower rotation
        self.rotation = math.degrees(angle)
        
        # Create new projectile
        self.projectiles.append(Projectile(
            self.x, self.y,
            self.target,
            self.stats["damage"],
            self.type,
            self.stats.get("splash_damage", 0)
        ))
        
        # Reset cooldown
        self.fire_cooldown = self.stats["fire_rate"]
        
    def get_distance_to(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        return math.sqrt(dx*dx + dy*dy)
        
    def draw(self, screen):
        # Draw range circle if selected
        if self.show_range:
            # Draw semi-transparent range circle
            range_surface = pygame.Surface((self.stats["range"]*2, self.stats["range"]*2), 
                                        pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (200, 200, 200, 64), 
                            (self.stats["range"], self.stats["range"]), 
                            self.stats["range"])
            screen.blit(range_surface, 
                       (self.x - self.stats["range"], 
                        self.y - self.stats["range"]))
        
        # Draw tower base (circle)
        pygame.draw.circle(screen, (100, 100, 100), (self.x, self.y), 22)
        
        # Draw tower body with rotation
        color = self.stats["color"]
        points = []
        size = 20
        
        # Calculate tower barrel points
        angle = math.radians(self.rotation)
        barrel_length = 25
        barrel_width = 8
        
        # Base points
        base_points = [
            (self.x + math.cos(angle) * size, 
             self.y + math.sin(angle) * size),
            (self.x + math.cos(angle + math.pi*0.8) * size, 
             self.y + math.sin(angle + math.pi*0.8) * size),
            (self.x + math.cos(angle - math.pi*0.8) * size, 
             self.y + math.sin(angle - math.pi*0.8) * size),
        ]
        
        # Barrel points
        barrel_points = [
            (self.x + math.cos(angle + math.pi/2) * barrel_width,
             self.y + math.sin(angle + math.pi/2) * barrel_width),
            (self.x + math.cos(angle) * barrel_length,
             self.y + math.sin(angle) * barrel_length),
            (self.x + math.cos(angle - math.pi/2) * barrel_width,
             self.y + math.sin(angle - math.pi/2) * barrel_width)
        ]
        
        # Draw tower components
        pygame.draw.polygon(screen, color, base_points)
        pygame.draw.polygon(screen, (color[0]*0.8, color[1]*0.8, color[2]*0.8), 
                          barrel_points)
        
        # Draw upgrade indicators
        if self.upgrades:
            indicator_y = self.y - 30
            for upgrade_type, level in self.upgrades.items():
                # Draw small colored dots for each upgrade level
                for i in range(level):
                    color = {
                        "damage": (255, 0, 0),
                        "range": (0, 255, 0),
                        "fire_rate": (0, 0, 255),
                        "splash_damage": (255, 165, 0)
                    }.get(upgrade_type, (255, 255, 255))
                    
                    pygame.draw.circle(screen, color,
                                     (self.x - 10 + i*7, indicator_y), 3)
                indicator_y -= 6
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
            
        # Draw targeting line if has target
        if self.target and self.show_range:
            pygame.draw.line(screen, (255, 0, 0, 128),
                           (self.x, self.y),
                           (self.target.x, self.target.y), 2)