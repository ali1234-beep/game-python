import pygame
import math
from constants import BOSS_SIZE, BOSS_REWARD, LEVEL_100_BOSS, ENEMY_SPEED
from .enemy import Enemy

class BossEnemy(Enemy):
    def __init__(self, wave_number):
        super().__init__(wave_number)
        
        # Check if this is the level 100 boss
        if wave_number == 100:
            self.is_special_boss = True
            self.size = LEVEL_100_BOSS["size"]
            self.health = self.max_health * LEVEL_100_BOSS["health_multiplier"]
            self.max_health = self.health
            self.speed = ENEMY_SPEED * LEVEL_100_BOSS["speed_multiplier"]
            self.color = LEVEL_100_BOSS["color"]
            self.reward = LEVEL_100_BOSS["reward"]
        else:
            self.is_special_boss = False
            self.size = BOSS_SIZE
            self.health *= 3  # Regular boss has 3x health
            self.max_health = self.health
            self.color = (255, 50, 50)  # Red color for regular boss
            self.reward = BOSS_REWARD
            
        self.shield_active = True
        self.shield_health = self.max_health * 0.3
        self.max_shield_health = self.shield_health
        self.phase = 1
        self.angle = 0
        self.vertices = 5 if not self.is_special_boss else 8  # Special boss has 8 sides
        self.value = self.reward
        
    def take_damage(self, amount):
        if self.shield_active:
            self.shield_health -= amount
            if self.shield_health <= 0:
                self.shield_active = False
                self.phase = 2
            self.hit_flash = 10
        else:
            super().take_damage(amount)
            if self.health < self.max_health * 0.3:
                self.phase = 3
                self.speed = self.speed * 1.5  # Enrage at low health
        
    def draw(self, screen):
        # Special effects for level 100 boss
        if self.is_special_boss:
            # Rotating aura effect
            aura_radius = self.size + 10 + math.sin(self.angle * 2) * 5
            for i in range(16):
                angle = self.angle + (i * math.pi / 8)
                aura_x = self.x + math.cos(angle) * aura_radius
                aura_y = self.y + math.sin(angle) * aura_radius
                aura_color = (
                    180 + int(75 * math.sin(self.angle + i)),
                    0,
                    180 + int(75 * math.cos(self.angle + i))
                )
                pygame.draw.circle(screen, aura_color, (int(aura_x), int(aura_y)), 5)
        
        # Draw boss body
        if self.hit_flash > 0:
            flash_intensity = min(255, self.hit_flash * 25)
            color = (min(255, self.color[0] + flash_intensity),
                    min(255, self.color[1] + flash_intensity),
                    min(255, self.color[2] + flash_intensity))
            self.hit_flash -= 1
        else:
            color = self.color
            
        # Draw the boss with phase-specific effects
        if self.phase == 1:
            # Phase 1: Shield phase
            # Draw shield
            shield_radius = self.size + 5
            shield_color = (100, 100, 255, 
                          int(255 * (self.shield_health / self.max_shield_health)))
            shield_surface = pygame.Surface((shield_radius*2, shield_radius*2), 
                                         pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, shield_color,
                             (shield_radius, shield_radius), shield_radius)
            screen.blit(shield_surface, 
                       (self.x - shield_radius, self.y - shield_radius))
            
        # Draw geometric shape based on boss type
        points = []
        for i in range(self.vertices):
            angle = self.angle + (2 * math.pi * i / self.vertices)
            x = self.x + math.cos(angle) * self.size
            y = self.y + math.sin(angle) * self.size
            points.append((x, y))
        
        pygame.draw.polygon(screen, color, points)
        
        if self.phase >= 2:
            # Phase 2 and 3: Add effects
            if self.is_special_boss:
                # Special boss gets more intense effects
                for i in range(self.vertices):
                    angle = self.angle + (2 * math.pi * i / self.vertices)
                    length = self.size + 15 + math.sin(self.angle * 3) * 8
                    end_x = self.x + math.cos(angle) * length
                    end_y = self.y + math.sin(angle) * length
                    pygame.draw.line(screen, (180, 0, 180), 
                                   (self.x, self.y), (end_x, end_y), 3)
            else:
                # Regular boss effects
                if self.phase == 3:  # Enraged phase
                    for i in range(8):
                        angle = self.angle + (math.pi * 2 * i / 8)
                        length = self.size + 10 + math.sin(self.angle * 5) * 5
                        end_x = self.x + math.cos(angle) * length
                        end_y = self.y + math.sin(angle) * length
                        pygame.draw.line(screen, (255, 100, 0), 
                                       (self.x, self.y), (end_x, end_y), 2)
        
        # Draw health bars
        self._draw_health_bars(screen)
        
        # Update rotation
        self.angle += 0.02 if not self.is_special_boss else 0.04
        
    def _draw_health_bars(self, screen):
        health_width = 60
        health_height = 6
        spacing = 2
        
        # Main health bar
        health_x = self.x - health_width/2
        health_y = self.y - self.size - 15
        
        # Health bar background (red)
        pygame.draw.rect(screen, (255, 0, 0),
                        (health_x, health_y, health_width, health_height))
        
        # Health bar foreground (green)
        health_percent = self.health / self.max_health
        if health_percent > 0:
            pygame.draw.rect(screen, (0, 255, 0),
                           (health_x, health_y, 
                            health_width * health_percent, health_height))
            
        # Shield bar (if active)
        if self.shield_active:
            shield_y = health_y - health_height - spacing
            # Shield bar background (gray)
            pygame.draw.rect(screen, (100, 100, 100),
                           (health_x, shield_y, health_width, health_height))
            
            # Shield bar foreground (blue)
            shield_percent = self.shield_health / self.max_shield_health
            if shield_percent > 0:
                pygame.draw.rect(screen, (0, 100, 255),
                               (health_x, shield_y, 
                                health_width * shield_percent, health_height))