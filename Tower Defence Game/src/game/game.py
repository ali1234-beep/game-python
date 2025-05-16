import pygame
import random
import math
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, TOWER_TYPES, PATH_POINTS,
                     UI_PANEL, UI_BORDER, UI_TEXT, DIFFICULTIES, BASE_POSITION,
                     BASE_SIZE, SHAKE_INTENSITY, BASE_HEALTH, WAVE_TIMER,
                     WAVE_ENEMY_COUNT, BOSS_WAVE_INTERVAL)
from src.towers.tower import Tower
from src.enemies.enemy import Enemy
from src.enemies.boss_enemy import BossEnemy
from src.ui.tower_selector import TowerSelector

class Game:
    def __init__(self, difficulty):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.difficulty = difficulty
        self.difficulty_settings = DIFFICULTIES[difficulty]
        self.clock = pygame.time.Clock()
        
        # Game state
        self.towers = []
        self.enemies = []
        self.selected_tower = None
        self.wave_number = 0
        self.wave_timer = WAVE_TIMER * 60
        self.wave_active = False
        self.enemies_spawned = 0
        self.spawn_counter = 0
        self.base_health = BASE_HEALTH
        self.base_shake = 0
        self.game_speed = 1
        self.money = self.difficulty_settings["starting_money"]
        self.game_started = False
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 24)  # Smaller font for detailed stats
        self.tower_selector = TowerSelector()
        self.upgrade_buttons = {}
        self.selected_tower_type = None  # For tower placement
        self.is_placing_tower = False
        self.start_button_rect = pygame.Rect(WINDOW_WIDTH - 140, WINDOW_HEIGHT - 60, 120, 40)
        
        self.setup_upgrade_buttons()

    def setup_upgrade_buttons(self):
        if not self.selected_tower:
            return
            
        button_height = 40
        margin = 10
        start_y = 100
        
        self.upgrade_buttons.clear()
        for upgrade_type, info in TOWER_TYPES[self.selected_tower.type].items():
            if upgrade_type in ["damage", "range", "fire_rate", "splash_damage"]:
                current_level = self.selected_tower.upgrades.get(upgrade_type, 0)
                if current_level < 3:  # Max 3 levels per upgrade
                    cost = 100 * (current_level + 1)  # Increasing costs
                    rect = pygame.Rect(10, start_y, 180, button_height)
                    self.upgrade_buttons[upgrade_type] = {
                        "rect": rect,
                        "cost": cost,
                        "level": current_level
                    }
                    start_y += button_height + margin

    def handle_splash_damage(self, enemy, damage, splash_radius):
        hit_pos = (enemy.x, enemy.y)
        for other_enemy in self.enemies:
            if other_enemy != enemy:
                dx = other_enemy.x - hit_pos[0]
                dy = other_enemy.y - hit_pos[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= splash_radius:
                    # Damage falls off with distance
                    damage_multiplier = 1 - (distance / splash_radius)
                    other_enemy.health -= damage * damage_multiplier

    def update(self):
        if not self.game_started:
            return

        # Update wave timer and spawn enemies
        if self.wave_timer > 0:
            self.wave_timer -= self.game_speed
        elif not self.wave_active:
            self.wave_number += 1
            self.enemies_spawned = 0
            self.wave_active = True
            self.wave_timer = WAVE_TIMER * 60

        # Update based on game speed
        for _ in range(self.game_speed):
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.move()
                if enemy.health <= 0:
                    self.money += enemy.value
                    self.enemies.remove(enemy)
                elif enemy.reached_end:
                    damage = 20 if isinstance(enemy, BossEnemy) else 10
                    self.base_health -= damage
                    self.base_shake = 10
                    self.enemies.remove(enemy)

            # Update towers
            for tower in self.towers:
                # Store old enemy health values to detect hits
                old_health = {enemy: enemy.health for enemy in self.enemies}
                
                tower.update(self.enemies)
                
                # Check for hits and apply splash damage
                for enemy in self.enemies:
                    if enemy.health < old_health[enemy]:
                        # Hit detected, apply splash damage if tower has it
                        if "splash_damage" in tower.stats and tower.stats["splash_damage"] > 0:
                            splash_radius = tower.stats["range"] * 0.3  # 30% of tower range
                            self.handle_splash_damage(enemy, tower.stats["splash_damage"], splash_radius)

            # Spawn enemies
            if self.wave_active and self.enemies_spawned < WAVE_ENEMY_COUNT:
                self.spawn_counter += 1
                if self.spawn_counter >= 60:  # Spawn rate
                    self.spawn_counter = 0
                    if self.wave_number % BOSS_WAVE_INTERVAL == 0:
                        self.enemies.append(BossEnemy(self.wave_number))
                    else:
                        self.enemies.append(Enemy(self.wave_number))
                    self.enemies_spawned += 1
                    if self.enemies_spawned >= WAVE_ENEMY_COUNT:
                        self.wave_active = False

            # Update base shake effect
            if self.base_shake > 0:
                self.base_shake -= 1

    def draw_base(self):
        # Calculate shake offset
        shake_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY) if self.base_shake > 0 else 0
        shake_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY) if self.base_shake > 0 else 0
        base_x = BASE_POSITION[0] + shake_x
        base_y = BASE_POSITION[1] + shake_y
        
        # Calculate health percentage
        health_percent = self.base_health / BASE_HEALTH
        
        # Bridge main structure (horizontal beam)
        bridge_width = BASE_SIZE * 1.5
        bridge_height = BASE_SIZE // 3
        pygame.draw.rect(self.screen, (120, 120, 120),
                        (base_x - bridge_width//2, base_y - bridge_height//2,
                         bridge_width, bridge_height))
        
        # Draw bridge supports
        support_width = bridge_height
        support_height = BASE_SIZE // 2
        gap = bridge_width // 3
        
        # Left support
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (base_x - bridge_width//2, base_y - bridge_height//2,
                         support_width, support_height))
                         
        # Right support
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (base_x + bridge_width//2 - support_width, base_y - bridge_height//2,
                         support_width, support_height))
        
        # Draw bridge surface details based on health
        if health_percent > 0:
            for i in range(4):
                plank_x = base_x - bridge_width//2 + (bridge_width//4) * i
                plank_width = bridge_width//5
                pygame.draw.rect(self.screen, (139, 69, 19),  # Wood color
                               (plank_x, base_y - bridge_height//2,
                                plank_width, bridge_height))
        else:
            # Draw broken bridge
            for i in range(4):
                if random.random() > 0.5:  # Random broken planks
                    plank_x = base_x - bridge_width//2 + (bridge_width//4) * i
                    plank_width = bridge_width//5
                    plank_height = bridge_height * random.uniform(0.3, 0.7)
                    pygame.draw.rect(self.screen, (101, 67, 33),  # Darker wood color
                                   (plank_x, base_y - bridge_height//2,
                                    plank_width, plank_height))
        
        # Draw health indicator
        health_width = bridge_width
        health_height = 8
        health_x = base_x - health_width//2
        health_y = base_y - bridge_height - health_height - 5
        
        # Health bar background
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (health_x, health_y, health_width, health_height))
        
        # Health bar foreground
        if health_percent > 0:
            pygame.draw.rect(self.screen, (0, 255, 0),
                           (health_x, health_y,
                            health_width * health_percent, health_height))

    def draw_death_screen(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font_big = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        game_over = font_big.render("Game Over!", True, (255, 0, 0))
        wave_text = font_small.render(f"You survived {self.wave_number} waves", True, (255, 255, 255))
        retry_text = font_small.render("Press R to Retry", True, (255, 255, 255))
        menu_text = font_small.render("Press M for Menu", True, (255, 255, 255))
        
        self.screen.blit(game_over, (WINDOW_WIDTH//2 - game_over.get_width()//2, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(wave_text, (WINDOW_WIDTH//2 - wave_text.get_width()//2, WINDOW_HEIGHT//2))
        self.screen.blit(retry_text, (WINDOW_WIDTH//2 - retry_text.get_width()//2, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(menu_text, (WINDOW_WIDTH//2 - menu_text.get_width()//2, WINDOW_HEIGHT//2 + 100))

    def draw_start_button(self):
        # Draw start button in bottom right
        color = (60, 120, 60) if not self.game_started else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.start_button_rect)
        pygame.draw.rect(self.screen, (100, 255, 100), self.start_button_rect, 3)
        
        text = self.font.render("Start", True, UI_TEXT)
        text_rect = text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_upgrade_panel(self):
        if not self.selected_tower:
            return
            
        # Draw panel background
        panel_height = len(self.upgrade_buttons) * 50 + 220  # Extra space for stats
        panel_rect = pygame.Rect(5, 50, 200, panel_height)
        pygame.draw.rect(self.screen, UI_PANEL, panel_rect)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, 2)
        
        # Draw tower info and current stats
        title = self.font.render(f"{self.selected_tower.type.title()}", True, UI_TEXT)
        self.screen.blit(title, (15, 60))
        
        # Draw current stats with labels
        y = 100
        stats_to_show = {
            "damage": "Damage",
            "range": "Range",
            "fire_rate": "Fire Rate",
            "splash_damage": "Splash Damage"
        }
        
        for stat, label in stats_to_show.items():
            if stat in self.selected_tower.stats:
                value = self.selected_tower.stats[stat]
                if stat == "fire_rate":
                    # Convert fire rate to shots per second
                    text = f"{label}: {60/value:.1f}/s"
                else:
                    text = f"{label}: {value}"
                stat_text = self.stats_font.render(text, True, UI_TEXT)
                self.screen.blit(stat_text, (15, y))
                y += 25
        
        # Draw upgrade buttons
        y += 20  # Add spacing between stats and upgrade buttons
        for upgrade_type, button in self.upgrade_buttons.items():
            rect = pygame.Rect(10, y, 180, 40)  # Update button position
            button["rect"] = rect  # Store updated rect
            cost = button["cost"]
            level = button["level"]
            
            # Draw button
            color = (60, 120, 60) if self.money >= cost else (120, 60, 60)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, UI_BORDER, rect, 2)
            
            # Draw text
            text = f"{upgrade_type.replace('_', ' ').title()} (${cost})"
            text_surface = self.font.render(text, True, UI_TEXT)
            self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))
            
            # Draw level indicators
            for i in range(3):
                indicator_rect = pygame.Rect(rect.right - 60 + i*15, rect.y + 5, 10, 10)
                color = (0, 255, 0) if i < level else (100, 100, 100)
                pygame.draw.rect(self.screen, color, indicator_rect)
            
            y += 50

    def draw(self):
        # Draw background and path
        self.screen.fill((34, 139, 34))  # Green background
        for i in range(len(PATH_POINTS) - 1):
            pygame.draw.line(self.screen, (139, 69, 19), PATH_POINTS[i], 
                           PATH_POINTS[i + 1], 40)
        
        # Draw base
        self.draw_base()
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)
        
        # Draw tower placement preview
        if self.is_placing_tower and self.selected_tower_type:
            mouse_pos = pygame.mouse.get_pos()
            color = TOWER_TYPES[self.selected_tower_type]["color"]
            alpha = 128 if self.can_place_tower(mouse_pos) else 64
            preview_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(preview_surface, (*color, alpha), (20, 20), 20)
            self.screen.blit(preview_surface, (mouse_pos[0] - 20, mouse_pos[1] - 20))
        
        # Draw UI elements
        self.draw_status_bar()
        self.tower_selector.draw(self.screen, self.money)
        if self.selected_tower:
            self.draw_upgrade_panel()
        
        if self.base_health <= 0:
            self.draw_death_screen()
        
        # Draw start button
        self.draw_start_button()
            
        pygame.display.flip()
        self.clock.tick(60)

    def draw_status_bar(self):
        # Draw top status bar background
        pygame.draw.rect(self.screen, UI_PANEL, (0, 0, WINDOW_WIDTH, 40))
        
        # Draw wave info
        wave_text = f"Wave {self.wave_number}"
        if not self.wave_active:
            next_wave = int(self.wave_timer / 60)
            wave_text += f" (Next: {next_wave}s)"
        text = self.font.render(wave_text, True, UI_TEXT)
        self.screen.blit(text, (10, 10))
        
        # Draw money
        money_text = self.font.render(f"${self.money}", True, UI_TEXT)
        self.screen.blit(money_text, (WINDOW_WIDTH//2 - money_text.get_width()//2, 10))
        
        # Draw health
        health_text = self.font.render(f"Health: {self.base_health}", True, UI_TEXT)
        self.screen.blit(health_text, (WINDOW_WIDTH - health_text.get_width() - 10, 10))

    def handle_events(self, events):
        if self.base_health <= 0:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.difficulty)
                        return "restart"
                    elif event.key == pygame.K_m:
                        return "menu"
            return None
            
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check start button
                if self.start_button_rect.collidepoint(mouse_pos):
                    self.game_started = True
                    return
                
                # Check tower selector
                if self.tower_selector.handle_event(event, mouse_pos):
                    self.selected_tower_type = self.tower_selector.selected_tower
                    self.is_placing_tower = bool(self.selected_tower_type)
                    self.selected_tower = None  # Deselect any selected tower
                    continue
                
                # Left click
                if event.button == 1:
                    if self.is_placing_tower:
                        if self.can_place_tower(mouse_pos):
                            cost = TOWER_TYPES[self.selected_tower_type]["cost"]
                            if self.money >= cost:
                                self.money -= cost
                                self.towers.append(Tower(mouse_pos[0], mouse_pos[1], 
                                                       self.selected_tower_type))
                    else:
                        # Check upgrade buttons if tower selected
                        if self.selected_tower:
                            for upgrade_type, button in self.upgrade_buttons.items():
                                if button["rect"].collidepoint(mouse_pos):
                                    cost = button["cost"]
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.apply_upgrade(self.selected_tower, upgrade_type)
                                        self.setup_upgrade_buttons()
                                    return
                        
                        # Check tower selection
                        for tower in self.towers:
                            dx = mouse_pos[0] - tower.x
                            dy = mouse_pos[1] - tower.y
                            if dx*dx + dy*dy <= (30*30):  # 30 pixel radius
                                self.selected_tower = tower
                                tower.show_range = True
                                self.setup_upgrade_buttons()
                                return
                                
                        # Deselect if clicked elsewhere
                        if self.selected_tower:
                            self.selected_tower.show_range = False
                            self.selected_tower = None
                            self.upgrade_buttons.clear()
                
                # Right click to cancel tower placement or selection
                elif event.button == 3:
                    if self.is_placing_tower:
                        self.is_placing_tower = False
                        self.selected_tower_type = None
                    elif self.selected_tower:
                        self.selected_tower.show_range = False
                        self.selected_tower = None
                        self.upgrade_buttons.clear()
                        
    def can_place_tower(self, pos):
        x, y = pos
        
        # Check if too close to path
        for i in range(len(PATH_POINTS) - 1):
            start = pygame.math.Vector2(PATH_POINTS[i])
            end = pygame.math.Vector2(PATH_POINTS[i + 1])
            tower_pos = pygame.math.Vector2(x, y)
            
            # Calculate distance to line segment
            line_vec = end - start
            point_vec = tower_pos - start
            line_len = line_vec.length()
            
            if line_len:
                proj = point_vec.dot(line_vec) / line_len
                proj = max(0, min(proj, line_len))
                closest = start + (line_vec * proj / line_len)
                distance = (tower_pos - closest).length()
                
                if distance < 40:  # Minimum distance from path
                    return False
        
        # Check if too close to other towers
        for tower in self.towers:
            dx = x - tower.x
            dy = y - tower.y
            if (dx*dx + dy*dy) < (50*50):  # Minimum distance between towers
                return False
                
        # Check if too close to base
        dx = x - BASE_POSITION[0]
        dy = y - BASE_POSITION[1]
        if (dx*dx + dy*dy) < ((BASE_SIZE + 20) * (BASE_SIZE + 20)):
            return False
            
        return True

    def apply_upgrade(self, tower, upgrade_type):
        tower.upgrades[upgrade_type] = tower.upgrades.get(upgrade_type, 0) + 1
        level = tower.upgrades[upgrade_type]
        
        # Apply upgrade effects
        if upgrade_type == "damage":
            tower.stats["damage"] = int(TOWER_TYPES[tower.type]["damage"] * (1.5 ** level))
        elif upgrade_type == "range":
            tower.stats["range"] = int(TOWER_TYPES[tower.type]["range"] * (1.3 ** level))
        elif upgrade_type == "fire_rate":
            tower.stats["fire_rate"] = int(TOWER_TYPES[tower.type]["fire_rate"] * (0.7 ** level))
        elif upgrade_type == "splash_damage":
            tower.stats["splash_damage"] = int(TOWER_TYPES[tower.type]["splash_damage"] * (1.5 ** level))