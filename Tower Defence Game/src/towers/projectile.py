import pygame
import math
from constants import PROJECTILE_SPEED

class Projectile:
    def __init__(self, x, y, target, damage, tower_type, splash_damage=0):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.splash_damage = splash_damage
        self.tower_type = tower_type
        self.dead = False
        self.trail = []
        self.max_trail_length = 10
        
        # Visual properties based on tower type
        self.color = {
            "basic": (50, 150, 255),  # Changed from gray to blue
            "rapid": (0, 255, 255),
            "sniper": (255, 0, 0),
            "splash": (255, 165, 0),
            "missile": (255, 255, 0)
        }.get(tower_type, (255, 255, 255))
        
        self.size = {
            "basic": 4,
            "rapid": 3,
            "sniper": 6,
            "splash": 5,
            "missile": 5
        }.get(tower_type, 4)
        
    def update(self):
        if self.dead:
            return
            
        # Store current position for trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
            
        # Move towards target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < PROJECTILE_SPEED:
            # Hit target
            self.target.health -= self.damage
            self.dead = True
            return
            
        # Update position
        self.x += (dx/distance) * PROJECTILE_SPEED
        self.y += (dy/distance) * PROJECTILE_SPEED
        
    def draw(self, screen):
        # Draw trail effect
        for i, (trail_x, trail_y) in enumerate(self.trail):
            # Calculate alpha based on position in trail
            alpha = int((i / len(self.trail)) * 255)
            trail_color = (*self.color, alpha)
            
            # Draw trail segment with transparency
            trail_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, 
                             (self.size//2, self.size//2), 
                             self.size//2 * (i/len(self.trail)))
            screen.blit(trail_surface, 
                       (trail_x - self.size//2, trail_y - self.size//2))
        
        # Draw main projectile
        if not self.dead:
            # Special effects based on tower type
            if self.tower_type == "missile":
                # Draw missile with flame trail
                angle = math.atan2(self.target.y - self.y, 
                                 self.target.x - self.x)
                points = [
                    (self.x + math.cos(angle) * self.size,
                     self.y + math.sin(angle) * self.size),
                    (self.x + math.cos(angle + 2.3) * self.size,
                     self.y + math.sin(angle + 2.3) * self.size),
                    (self.x + math.cos(angle - 2.3) * self.size,
                     self.y + math.sin(angle - 2.3) * self.size),
                ]
                pygame.draw.polygon(screen, self.color, points)
                
            elif self.tower_type == "splash":
                # Draw with inner glow
                glow_surface = pygame.Surface((self.size*2, self.size*2), 
                                           pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*self.color, 128), 
                                 (self.size, self.size), self.size)
                screen.blit(glow_surface, 
                          (self.x - self.size, self.y - self.size))
                pygame.draw.circle(screen, self.color, 
                                 (int(self.x), int(self.y)), self.size//2)
                
            else:
                # Standard projectile
                pygame.draw.circle(screen, self.color, 
                                 (int(self.x), int(self.y)), self.size)