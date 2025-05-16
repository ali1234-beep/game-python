import pygame
import math
from constants import (PATH_POINTS, ENEMY_SPEED, ENEMY_SIZE, 
                     STARTING_ENEMY_HEALTH, HEALTH_SCALING_FACTOR, MAX_HEALTH_CAP)

class Enemy:
    def __init__(self, wave_number=1):
        self.x = PATH_POINTS[0][0]
        self.y = PATH_POINTS[0][1]
        self.current_point = 0
        # Cap health scaling at MAX_HEALTH_CAP
        base_health = min(
            STARTING_ENEMY_HEALTH * (HEALTH_SCALING_FACTOR ** wave_number),
            MAX_HEALTH_CAP
        )
        self.health = base_health
        self.max_health = self.health
        self.reward = 10 + wave_number * 2  # Smaller reward scaling
        self.speed = ENEMY_SPEED
        self.reached_end = False
        self.size = ENEMY_SIZE
        self.color = (100, 255, 100)  # Base enemy color
        self.hit_flash = 0  # For damage visual effect
        self.value = self.reward
        
    def move(self):
        if self.current_point >= len(PATH_POINTS) - 1:
            self.reached_end = True
            self.health = 0  # Die instantly when reaching base
            return
            
        # Get current target point
        target_x, target_y = PATH_POINTS[self.current_point + 1]
        
        # Calculate direction to move
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.speed:
            # Reached current target point, move to next one
            self.x = target_x
            self.y = target_y
            self.current_point += 1
        else:
            # Move towards target point
            self.x += (dx/distance) * self.speed
            self.y += (dy/distance) * self.speed
            
    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 10  # Start hit flash effect
        
    def is_alive(self):
        return self.health > 0
        
    def draw(self, screen):
        # Draw enemy body
        if self.hit_flash > 0:
            # Flash white when hit
            flash_intensity = min(255, self.hit_flash * 25)
            color = (min(255, self.color[0] + flash_intensity),
                    min(255, self.color[1] + flash_intensity),
                    min(255, self.color[2] + flash_intensity))
            self.hit_flash -= 1
        else:
            color = self.color
            
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Draw health bar
        health_width = 40
        health_height = 5
        health_x = self.x - health_width/2
        health_y = self.y - self.size - 10
        
        # Health bar background (red)
        pygame.draw.rect(screen, (255, 0, 0),
                        (health_x, health_y, health_width, health_height))
        
        # Health bar foreground (green)
        health_percent = self.health / self.max_health
        if health_percent > 0:
            pygame.draw.rect(screen, (0, 255, 0),
                           (health_x, health_y, 
                            health_width * health_percent, health_height))
            
    def get_position(self):
        return self.x, self.y