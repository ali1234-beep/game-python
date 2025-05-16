import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TOWER_SIZE = 40
TILE_SIZE = 40
ENEMY_SIZE = 20
ENEMY_SPEED = 2
SPAWN_RATE = 60  # Frames between enemy spawns

# Add new constants
TOWER_TYPES = {
    "Sniper": {
        "damage": 50,
        "fire_rate": 60,  # Frames between shots
        "range": 200,
        "cost": 100,
        "color": (50, 50, 150)
    },
    "Assault": {
        "damage": 10,
        "fire_rate": 15,
        "range": 120,
        "cost": 75,
        "color": (150, 50, 50)
    },
    "Cannon": {
        "damage": 25,
        "fire_rate": 45,
        "range": 150,
        "cost": 150,
        "color": (50, 150, 50)
    }
}

# Add new constants after TOWER_TYPES
UPGRADE_PATHS = {
    "Sniper": {
        "damage": {
            "name": "Damage",
            "levels": [
                {"cost": 100, "multiplier": 1.5},
                {"cost": 200, "multiplier": 2.0},
                {"cost": 300, "multiplier": 2.5}
            ]
        },
        "range": {
            "name": "Range",
            "levels": [
                {"cost": 75, "multiplier": 1.3},
                {"cost": 150, "multiplier": 1.6},
                {"cost": 225, "multiplier": 2.0}
            ]
        }
    },
    "Assault": {
        "fire_rate": {
            "name": "Fire Rate",
            "levels": [
                {"cost": 100, "multiplier": 0.8},
                {"cost": 200, "multiplier": 0.6},
                {"cost": 300, "multiplier": 0.4}
            ]
        },
        "damage": {
            "name": "Damage",
            "levels": [
                {"cost": 75, "multiplier": 1.5},
                {"cost": 150, "multiplier": 2.0},
                {"cost": 225, "multiplier": 2.5}
            ]
        }
    },
    "Cannon": {
        "damage": {
            "name": "Damage",
            "levels": [
                {"cost": 125, "multiplier": 1.5},
                {"cost": 250, "multiplier": 2.0},
                {"cost": 375, "multiplier": 2.5}
            ]
        },
        "fire_rate": {
            "name": "Fire Rate",
            "levels": [
                {"cost": 100, "multiplier": 0.8},
                {"cost": 200, "multiplier": 0.6},
                {"cost": 300, "multiplier": 0.5}
            ]
        }
    }
}

# Add these constants at the top with other constants
STARTING_ENEMY_HEALTH = 100
HEALTH_SCALING_FACTOR = 1.2
BASE_HEALTH = 100
WAVE_ENEMY_COUNT = 10  # Number of enemies per wave

# Add to the constants section
NORMAL_SPEED = 1
FAST_SPEED = 2

# Add to constants section
STARTING_MONEY = 180
MAX_TOWERS = 10
 
# Add wave timer constant
WAVE_TIMER = 30  # Seconds between waves
TOWER_SPACING = TOWER_SIZE  # Minimum distance between towers

# Difficulty settings
DIFFICULTIES = {
    "Easy": {
        "enemy_health_multiplier": 0.8,
        "enemy_speed_multiplier": 0.8,
        "starting_money": 200
    },
    "Normal": {
        "enemy_health_multiplier": 1.0,
        "enemy_speed_multiplier": 1.0,
        "starting_money": 150
    },
    "Hard": {
        "enemy_health_multiplier": 1.2,
        "enemy_speed_multiplier": 1.2,
        "starting_money": 100
    }
}

# Shop and loadout constants
MAX_LOADOUT_SLOTS = 4
SHOP_TOWERS = {
    "Sniper": {
        "unlock_cost": 1000,
        "description": "Long range, high damage"
    },
    "Assault": {
        "unlock_cost": 800,
        "description": "Fast firing, medium range"
    },
    "Cannon": {
        "unlock_cost": 1500,
        "description": "Area damage, slow firing"
    }
}

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)  # Darker forest green
PATH_COLOR = (139, 69, 19)  # Saddle brown - darker path
LIGHT_GREEN = (46, 139, 34)  # Slightly lighter forest green
DARK_GREEN = (25, 100, 25)  # Very dark green for contrast
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
UPGRADE_PANEL_COLOR = (40, 40, 40)
UPGRADE_BUTTON_COLOR = (60, 60, 60)
UPGRADE_HOVER_COLOR = (80, 80, 80)
UPGRADE_TEXT_COLOR = (220, 220, 220)

# Add to Colors section
UI_BACKGROUND = (30, 35, 45)
UI_PANEL = (45, 50, 60)
UI_BORDER = (70, 75, 85)
UI_TEXT = (200, 210, 220)
UI_HIGHLIGHT = (80, 160, 220)

# Path points for enemies to follow (x, y coordinates)
PATH_POINTS = [
    (-20, 100),     # Start off-screen
    (100, 100),     # First turn
    (100, 300),     # Down
    (300, 300),     # Right
    (300, 150),     # Up
    (500, 150),     # Right
    (500, 400),     # Down
    (800, 400)      # Exit
]

# Add boss enemy constants at the top with other constants
BOSS_WAVE_INTERVAL = 5  # Boss appears every 5 waves
BOSS_SIZE = 40  # Bigger than normal enemies
BOSS_HEALTH_MULTIPLIER = 5
BOSS_SPEED_MULTIPLIER = 0.5
BOSS_REWARD = 100  # More money for killing a boss

# Add to Constants section
BASE_SIZE = 80
BASE_POSITION = (750, 400)  # End of path
SHAKE_INTENSITY = 5

# Add new class for projectiles
class Projectile:
    def __init__(self, x, y, target, tower_type):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 10
        self.damage = TOWER_TYPES[tower_type]["damage"]
        self.color = TOWER_TYPES[tower_type]["color"]
        
    def move(self):
        # Calculate direction to target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return True
        
        # Normalize and multiply by speed
        self.x += (dx/distance) * self.speed
        self.y += (dy/distance) * self.speed
        
        # Check if hit target
        if distance < 5:
            self.target.health -= self.damage
            return True
        return False
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)

# Update Tower class
class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type
        self.stats = TOWER_TYPES[tower_type].copy()  # Make a copy so we can modify stats
        self.show_range = False
        self.shoot_counter = 0
        self.projectiles = []
        self.upgrades = {key: 0 for key in UPGRADE_PATHS[tower_type]}

    def can_shoot(self):
        return self.shoot_counter >= self.stats["fire_rate"]

    def get_closest_enemy(self, enemies):
        closest_enemy = None
        min_dist = float('inf')
        
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            dist = (dx**2 + dy**2)**0.5
            
            if dist <= self.stats["range"] and dist < min_dist:
                closest_enemy = enemy
                min_dist = dist
        
        return closest_enemy

    def update(self, enemies):
        self.shoot_counter += 1
        
        # Update existing projectiles
        self.projectiles = [p for p in self.projectiles if not p.move()]
        
        # Check for new shots
        if self.can_shoot():
            target = self.get_closest_enemy(enemies)
            if target:
                self.projectiles.append(Projectile(self.x, self.y, target, self.type))
                self.shoot_counter = 0

    def draw(self, screen):
        # Draw tower
        pygame.draw.circle(screen, self.stats["color"], 
                         (self.x, self.y), TOWER_SIZE // 2)
        
        # Draw range circle if selected or mouse hovering
        if self.show_range:
            pygame.draw.circle(screen, (255, 255, 255, 128), 
                             (self.x, self.y), 
                             self.stats["range"], 1)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

# Modify the Enemy class
class Enemy:
    def __init__(self, wave_number):
        self.x = PATH_POINTS[0][0]
        self.y = PATH_POINTS[0][1]
        self.path_index = 0
        # Scale health with wave number
        self.max_health = int(STARTING_ENEMY_HEALTH * (HEALTH_SCALING_FACTOR ** wave_number))
        self.health = self.max_health

    def move(self):
        target_x, target_y = PATH_POINTS[self.path_index + 1]
        
        # Move towards the current target point
        if self.x < target_x:
            self.x += ENEMY_SPEED
        elif self.x > target_x:
            self.x -= ENEMY_SPEED
        
        if self.y < target_y:
            self.y += ENEMY_SPEED
        elif self.y > target_y:
            self.y -= ENEMY_SPEED
            
        # Check if reached current target
        if (abs(self.x - target_x) < ENEMY_SPEED and 
            abs(self.y - target_y) < ENEMY_SPEED):
            if self.path_index < len(PATH_POINTS) - 2:
                self.path_index += 1

    def draw(self, screen):
        # Draw enemy
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), ENEMY_SIZE // 2)
        
        # Draw health bar
        health_bar_width = 40
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (
            self.x - health_bar_width//2,
            self.y - ENEMY_SIZE - health_bar_height - 2,
            health_bar_width,
            health_bar_height
        ))
        pygame.draw.rect(screen, (0, 255, 0), (
            self.x - health_bar_width//2,
            self.y - ENEMY_SIZE - health_bar_height - 2,
            health_bar_width * health_ratio,
            health_bar_height
        ))

# Add BossEnemy class
class BossEnemy(Enemy):
    def __init__(self, wave_number):
        super().__init__(wave_number)
        self.max_health *= BOSS_HEALTH_MULTIPLIER
        self.health = self.max_health
        self.is_boss = True
        self.vertices = 5  # Pentagon shape for boss
        self.rotation = 0
        self.speed = ENEMY_SPEED * BOSS_SPEED_MULTIPLIER
        
    def move(self):
        target_x, target_y = PATH_POINTS[self.path_index + 1]
        
        # Move towards the current target point
        if self.x < target_x:
            self.x += self.speed
        elif self.x > target_x:
            self.x -= self.speed
        
        if self.y < target_y:
            self.y += self.speed
        elif self.y > target_y:
            self.y -= self.speed
            
        # Check if reached current target
        if (abs(self.x - target_x) < self.speed and 
            abs(self.y - target_y) < self.speed):
            self.x = target_x  # Snap to exact position
            self.y = target_y
            if self.path_index < len(PATH_POINTS) - 2:
                self.path_index += 1
        
        # Rotate the boss
        self.rotation += 1
        
    def draw(self, screen):
        # Draw pentagon shape for boss
        points = []
        for i in range(self.vertices):
            angle = self.rotation + (360 / self.vertices) * i
            x = self.x + BOSS_SIZE/2 * pygame.math.Vector2().from_polar((1, angle))[0]
            y = self.y + BOSS_SIZE/2 * pygame.math.Vector2().from_polar((1, angle))[1]
            points.append((x, y))
        
        pygame.draw.polygon(screen, (200, 0, 0), points)  # Darker red for boss
        
        # Draw health bar
        health_bar_width = 60  # Wider health bar for boss
        health_bar_height = 8  # Taller health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (
            self.x - health_bar_width//2,
            self.y - BOSS_SIZE - health_bar_height - 2,
            health_bar_width,
            health_bar_height
        ))
        pygame.draw.rect(screen, (0, 255, 0), (
            self.x - health_bar_width//2,
            self.y - BOSS_SIZE - health_bar_height - 2,
            health_bar_width * health_ratio,
            health_bar_height
        ))

# Add TowerSelector class
class TowerSelector:
    def __init__(self):
        self.selected_tower = None
        self.tower_boxes = {}
        self.setup_tower_boxes()

    def setup_tower_boxes(self):
        box_width = 60  # Made boxes smaller
        box_height = 60
        margin = 30
        start_x = (WINDOW_WIDTH - (box_width + margin) * len(TOWER_TYPES)) // 2
        y = WINDOW_HEIGHT - 80

        for i, tower_type in enumerate(TOWER_TYPES):
            x = start_x + (box_width + margin) * i
            self.tower_boxes[tower_type] = pygame.Rect(x, y, box_width, box_height)

    def draw(self, screen):
        # Draw tower boxes
        for tower_type, box in self.tower_boxes.items():
            # Draw individual box background
            pygame.draw.rect(screen, (100, 100, 100), box)  # Gray background
            
            # Draw tower preview as circle
            tower_x = box.centerx
            tower_y = box.centery
            pygame.draw.circle(screen, TOWER_TYPES[tower_type]["color"], 
                           (tower_x, tower_y), TOWER_SIZE // 2)

            # Draw tower cost
            font = pygame.font.Font(None, 24)
            cost_text = font.render(str(TOWER_TYPES[tower_type]["cost"]), True, WHITE)
            screen.blit(cost_text, (box.centerx - cost_text.get_width()//2, 
                                  box.bottom - 20))
            
            # Highlight selected tower
            if tower_type == self.selected_tower:
                pygame.draw.rect(screen, WHITE, box, 2)  # White outline for selected tower

    def handle_click(self, pos, right_click=False):
        """Handle mouse clicks on tower selection boxes."""
        # Handle right-click to deselect
        if right_click:
            self.selected_tower = None
            return True

        # Handle left-click selection
        for tower_type, box in self.tower_boxes.items():
            if box.collidepoint(pos):
                self.selected_tower = tower_type
                return True
                
        # Clicking outside tower boxes deselects
        self.selected_tower = None
        return False

# Add these classes before the Game class
class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class LoadoutSystem:
    def __init__(self):
        self.slots = [None] * MAX_LOADOUT_SLOTS
        self.unlocked_towers = ["Assault"]  # Start with basic tower
        self.selected_slot = None
        self.setup_slots()
        
    def setup_slots(self):
        self.slot_rects = []
        slot_size = 70
        margin = 10
        start_x = (WINDOW_WIDTH - (slot_size + margin) * MAX_LOADOUT_SLOTS) // 2
        y = WINDOW_HEIGHT - 180
        
        for i in range(MAX_LOADOUT_SLOTS):
            x = start_x + (slot_size + margin) * i
            self.slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
            
    def draw(self, screen):
        for i, (rect, tower) in enumerate(zip(self.slot_rects, self.slots)):
            # Draw slot background
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
            
            # Draw tower if slot is filled
            if tower:
                pygame.draw.circle(screen, TOWER_TYPES[tower]["color"],
                                 rect.center, TOWER_SIZE // 2)
            
            # Highlight selected slot
            if i == self.selected_slot:
                pygame.draw.rect(screen, (255, 255, 0), rect, 3)

    def handle_click(self, pos):
        for i, rect in enumerate(self.slot_rects):
            if rect.collidepoint(pos):
                self.selected_slot = i
                return True
        return False

class Shop:
    def __init__(self, loadout_system):
        self.loadout = loadout_system
        self.setup_buttons()
        
    def setup_buttons(self):
        self.tower_buttons = {}
        button_height = 60
        margin = 10
        start_y = 100
        
        for i, (tower_type, info) in enumerate(SHOP_TOWERS.items()):
            y = start_y + (button_height + margin) * i
            button = Button(WINDOW_WIDTH//2 - 150, y, 300, button_height,
                          f"{tower_type} - ${info['unlock_cost']}")
            self.tower_buttons[tower_type] = button
            
    def draw(self, screen, money):
        # Draw shop title
        font = pygame.font.Font(None, 48)
        title = font.render("Tower Shop", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 30))
        
        # Draw available money
        money_text = font.render(f"Money: ${money}", True, WHITE)
        screen.blit(money_text, (20, 30))
        
        # Draw tower buttons
        for tower_type, button in self.tower_buttons.items():
            if tower_type not in self.loadout.unlocked_towers:
                button.draw(screen)
                # Draw description
                font = pygame.font.Font(None, 24)
                desc = font.render(SHOP_TOWERS[tower_type]["description"], True, WHITE)
                screen.blit(desc, (button.rect.x, button.rect.bottom + 5))

class TitleScreen:
    def __init__(self):
        self.difficulty_buttons = {
            "Easy": Button(WINDOW_WIDTH//2 - 100, 200, 200, 50, "Easy", (0, 255, 0)),
            "Normal": Button(WINDOW_WIDTH//2 - 100, 280, 200, 50, "Normal", (255, 255, 0)),
            "Hard": Button(WINDOW_WIDTH//2 - 100, 360, 200, 50, "Hard", (255, 0, 0))
        }
        self.shop_button = Button(WINDOW_WIDTH//2 - 100, 440, 200, 50, "Shop")
        
    def draw(self, screen):
        screen.fill((50, 50, 50))
        
        # Draw title
        font = pygame.font.Font(None, 72)
        title = font.render("Tower Defense", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 80))
        
        # Draw buttons
        for button in self.difficulty_buttons.values():
            button.draw(screen)
        self.shop_button.draw(screen)
        
    def handle_click(self, pos):
        # Check difficulty buttons
        for difficulty, button in self.difficulty_buttons.items():
            if button.is_clicked(pos):
                return ("start_game", difficulty)
                
        # Check shop button
        if self.shop_button.is_clicked(pos):
            return ("shop", None)
            
        return (None, None)

# Update Game class with wave management, base health, and upgrade panel
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.towers = []
        self.game_started = False
        self.font = pygame.font.Font(None, 36)
        self.grass_variations = [GREEN, LIGHT_GREEN, DARK_GREEN]
        self.enemies = []
        self.spawn_counter = 0
        self.tower_selector = TowerSelector()
        self.selected_tower_type = None
        self.placement_preview = None
        self.wave_number = 0
        self.enemies_spawned = 0
        self.base_health = BASE_HEALTH
        self.game_speed = NORMAL_SPEED
        self.money = STARTING_MONEY
        self.speed_button_rect = pygame.Rect(20, WINDOW_HEIGHT - 110, 120, 40)  # Above start button
        self.wave_timer = 0  # Start at 0 so first wave begins immediately
        self.wave_active = False
        self.selected_tower = None  # Currently selected tower for upgrading
        self.upgrade_buttons = {}  # Buttons for upgrade paths
        self.setup_upgrade_buttons()
        self.ui_panel_height = 120  # Height of bottom UI panel
        self.base_shake = 0  # Add base shake effect

    def setup_upgrade_buttons(self):
        self.upgrade_buttons.clear()
        if self.selected_tower:
            button_height = 40
            margin = 10
            panel_width = 200
            start_y = 100

            for upgrade_type, upgrade_info in UPGRADE_PATHS[self.selected_tower.type].items():
                current_level = self.selected_tower.upgrades[upgrade_type]
                if current_level < len(upgrade_info["levels"]):
                    cost = upgrade_info["levels"][current_level]["cost"]
                    y = start_y + (button_height + margin) * len(self.upgrade_buttons)
                    button = Button(
                        WINDOW_WIDTH - panel_width - 10, y, 
                        panel_width, button_height,
                        f"{upgrade_info['name']} (${cost})",
                        UPGRADE_BUTTON_COLOR
                    )
                    self.upgrade_buttons[upgrade_type] = button

    def draw_upgrade_panel(self):
        # Move upgrade panel to the left side instead of right
        panel_width = 210
        panel_rect = pygame.Rect(
            10, 50,  # Position on left side
            panel_width, len(self.upgrade_buttons) * 50 + 120
        )
        pygame.draw.rect(self.screen, UPGRADE_PANEL_COLOR, panel_rect)
        pygame.draw.rect(self.screen, UI_BORDER, panel_rect, 2)

        # Draw tower info
        font = pygame.font.Font(None, 28)
        title = font.render(f"{self.selected_tower.type} Tower", True, UPGRADE_TEXT_COLOR)
        self.screen.blit(title, (panel_rect.x + 10, panel_rect.y + 10))

        # Draw current stats
        stats_y = panel_rect.y + 40
        for stat, value in self.selected_tower.stats.items():
            if stat in ["damage", "range", "fire_rate"]:
                stat_text = font.render(
                    f"{stat.replace('_', ' ').title()}: {value}", 
                    True, UPGRADE_TEXT_COLOR
                )
                self.screen.blit(stat_text, (panel_rect.x + 10, stats_y))
                stats_y += 25

        # Update upgrade button positions
        self.setup_upgrade_buttons()

    def draw_placement_preview(self, mouse_pos):
        if self.selected_tower_type:
            x, y = mouse_pos
            # Draw transparent tower preview
            preview_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(preview_surface, (*TOWER_TYPES[self.selected_tower_type]["color"], 128), 
                             (x, y), TOWER_SIZE // 2)
            # Draw range preview
            pygame.draw.circle(preview_surface, (255, 255, 255, 64), 
                             (x, y), TOWER_TYPES[self.selected_tower_type]["range"])
            self.screen.blit(preview_surface, (0, 0))

    def draw_map(self):
        # Fill background with solid green
        self.screen.fill(GREEN)
        
        # Draw path
        path_width = 40
        for i in range(len(PATH_POINTS) - 1):
            start_pos = PATH_POINTS[i]
            end_pos = PATH_POINTS[i + 1]
            pygame.draw.line(self.screen, PATH_COLOR, start_pos, end_pos, path_width)
        
        # Draw rounded corners at path joints
        for point in PATH_POINTS[1:-1]:
            pygame.draw.circle(self.screen, PATH_COLOR, point, path_width // 2)
        
    def draw_start_button(self):
        button_rect = pygame.Rect(20, WINDOW_HEIGHT - 60, 120, 40)
        # Draw light green outline
        pygame.draw.rect(self.screen, (100, 255, 100), button_rect, 3)  # Light green border
        # Draw button background
        inner_rect = pygame.Rect(23, WINDOW_HEIGHT - 57, 114, 34)
        pygame.draw.rect(self.screen, GREEN if not self.game_started else (100, 100, 100), inner_rect)
        text = self.font.render("Start", True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        return button_rect

    def draw_speed_button(self):
        # Draw speed toggle button
        pygame.draw.rect(self.screen, (100, 255, 100), self.speed_button_rect, 3)
        inner_rect = pygame.Rect(self.speed_button_rect.x + 3, self.speed_button_rect.y + 3,
                               self.speed_button_rect.width - 6, self.speed_button_rect.height - 6)
        pygame.draw.rect(self.screen, GRAY, inner_rect)
        speed_text = self.font.render(f"{self.game_speed}x", True, WHITE)
        text_rect = speed_text.get_rect(center=self.speed_button_rect.center)
        self.screen.blit(speed_text, text_rect)
        return self.speed_button_rect

    def is_valid_tower_position(self, x, y):
        # Check if tower is too close to existing towers
        for tower in self.towers:
            dx = x - tower.x
            dy = y - tower.y
            distance = (dx**2 + dy**2)**0.5
            if distance < TOWER_SPACING:
                return False

        # Check if tower is too close to path
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
                
                if distance < 30:  # Minimum distance from path
                    return False
                    
        return True

    def draw_wave_and_health(self):
        # Draw wave number
        wave_text = self.font.render(f"Wave: {self.wave_number}", True, WHITE)
        self.screen.blit(wave_text, (20, 20))
        
        # Draw base health in top right
        health_text = self.font.render(f"Base Health: {self.base_health}", True, WHITE)
        health_rect = health_text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
        self.screen.blit(health_text, health_rect)

    def draw_wave_timer(self):
        if self.game_started:
            seconds_left = self.wave_timer // 60
            timer_text = self.font.render(f"Next Wave: {seconds_left}s", True, WHITE)
            timer_rect = timer_text.get_rect(center=(WINDOW_WIDTH // 2, 20))
            self.screen.blit(timer_text, timer_rect)

    def draw_money(self):
        money_text = self.font.render(f"Money: ${self.money}", True, WHITE)
        money_rect = money_text.get_rect(topright=(WINDOW_WIDTH - 20, 60))  # Below health
        self.screen.blit(money_text, money_rect)

    def can_afford_tower(self, tower_type):
        return (self.money >= TOWER_TYPES[tower_type]["cost"] and 
                len(self.towers) < MAX_TOWERS)

    def draw_base(self):
        # Calculate shake offset
        shake_offset_x = 0
        shake_offset_y = 0
        if self.base_shake > 0:
            shake_offset_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
            shake_offset_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        
        # Draw base with shake effect
        base_x = BASE_POSITION[0] + shake_offset_x
        base_y = BASE_POSITION[1] + shake_offset_y
        
        # Draw castle-like base
        # Main structure
        pygame.draw.rect(self.screen, (150, 150, 150), 
                        (base_x - BASE_SIZE//2, base_y - BASE_SIZE//2, 
                         BASE_SIZE, BASE_SIZE))
        
        # Battlements (top)
        battlement_size = BASE_SIZE // 4
        for i in range(3):
            x = base_x - BASE_SIZE//2 + (i * battlement_size)
            pygame.draw.rect(self.screen, (120, 120, 120),
                           (x, base_y - BASE_SIZE//2 - battlement_size//2,
                            battlement_size, battlement_size))
        
        # Door
        door_width = BASE_SIZE // 3
        door_height = BASE_SIZE // 2
        pygame.draw.rect(self.screen, (101, 67, 33),
                        (base_x - door_width//2,
                         base_y - door_height//2,
                         door_width, door_height))
        
        # Health indicator ring
        health_ratio = self.base_health / BASE_HEALTH
        color = (int(255 * (1 - health_ratio)), int(255 * health_ratio), 0)
        pygame.draw.circle(self.screen, color,
                         (base_x, base_y),
                         BASE_SIZE//2 + 5, 3)

    def update(self):
        if self.game_started:
            # Start first wave immediately when game starts
            if self.wave_number == 0:
                self.wave_number = 1
                self.enemies_spawned = 0
                self.wave_active = True
                self.wave_timer = WAVE_TIMER * 60

            # Update wave timer for subsequent waves
            if self.wave_timer > 0:
                self.wave_timer -= self.game_speed
            elif not self.wave_active and len(self.enemies) == 0:
                # Start new wave
                self.wave_timer = WAVE_TIMER * 60
                self.wave_number += 1
                self.enemies_spawned = 0
                self.wave_active = True

            # Apply game speed to all time-based updates
            for _ in range(self.game_speed):
                # Update enemies and check for death/base damage
                for enemy in self.enemies[:]:
                    enemy.move()
                    if enemy.health <= 0:
                        # Give more money for boss kills
                        self.money += BOSS_REWARD if isinstance(enemy, BossEnemy) else 25
                        self.enemies.remove(enemy)
                        continue
                    if enemy.path_index >= len(PATH_POINTS) - 2:
                        self.base_health -= 20 if isinstance(enemy, BossEnemy) else 10
                        self.base_shake = 10  # Start shake effect
                        self.enemies.remove(enemy)

                # Update base shake effect
                if self.base_shake > 0:
                    self.base_shake -= 1

                # Update towers
                for tower in self.towers:
                    tower.update(self.enemies)

                # Spawn enemies
                if self.wave_active and self.enemies_spawned < (1 if self.wave_number % BOSS_WAVE_INTERVAL == 0 else WAVE_ENEMY_COUNT):
                    self.spawn_counter += 1
                    if self.spawn_counter >= SPAWN_RATE:
                        if self.wave_number % BOSS_WAVE_INTERVAL == 0:
                            self.enemies.append(BossEnemy(self.wave_number))
                        else:
                            self.enemies.append(Enemy(self.wave_number))
                        self.enemies_spawned += 1
                        self.spawn_counter = 0
                        if self.enemies_spawned >= (1 if self.wave_number % BOSS_WAVE_INTERVAL == 0 else WAVE_ENEMY_COUNT):
                            self.wave_active = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = self.draw_start_button()
                
                # Right click to deselect
                if event.button == 3:  # Right mouse button
                    self.tower_selector.handle_click(mouse_pos, right_click=True)
                    self.selected_tower_type = None
                    self.selected_tower = None
                    self.upgrade_buttons.clear()
                # Left click handling
                elif event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(mouse_pos) and not self.game_started:
                        self.game_started = True
                    elif self.speed_button_rect.collidepoint(mouse_pos):
                        self.game_speed = NORMAL_SPEED if self.game_speed == FAST_SPEED else FAST_SPEED
                    # Check tower selection first
                    elif self.tower_selector.handle_click(mouse_pos):
                        self.selected_tower_type = self.tower_selector.selected_tower
                    # Check upgrade buttons if tower is selected
                    elif self.selected_tower:
                        for upgrade_type, button in self.upgrade_buttons.items():
                            if button.is_clicked(mouse_pos):
                                current_level = self.selected_tower.upgrades[upgrade_type]
                                if current_level < len(UPGRADE_PATHS[self.selected_tower.type][upgrade_type]["levels"]):
                                    upgrade_cost = UPGRADE_PATHS[self.selected_tower.type][upgrade_type]["levels"][current_level]["cost"]
                                    if self.money >= upgrade_cost:
                                        self.money -= upgrade_cost
                                        self.selected_tower.upgrades[upgrade_type] += 1
                                        # Apply upgrade effect
                                        multiplier = UPGRADE_PATHS[self.selected_tower.type][upgrade_type]["levels"][current_level]["multiplier"]
                                        if upgrade_type == "damage":
                                            self.selected_tower.stats["damage"] = int(TOWER_TYPES[self.selected_tower.type]["damage"] * multiplier)
                                        elif upgrade_type == "range":
                                            self.selected_tower.stats["range"] = int(TOWER_TYPES[self.selected_tower.type]["range"] * multiplier)
                                        elif upgrade_type == "fire_rate":
                                            self.selected_tower.stats["fire_rate"] = int(TOWER_TYPES[self.selected_tower.type]["fire_rate"] * multiplier)
                                        self.setup_upgrade_buttons()
                                        return
                    # Check tower placement
                    elif (self.game_started and 
                          self.selected_tower_type and 
                          self.is_valid_tower_position(*mouse_pos) and 
                          self.can_afford_tower(self.selected_tower_type)):
                        # Place tower and deduct cost
                        x, y = mouse_pos
                        new_tower = Tower(x, y, self.selected_tower_type)
                        self.towers.append(new_tower)
                        self.money -= TOWER_TYPES[self.selected_tower_type]["cost"]
                    else:
                        # Clicking anywhere else deselects the tower
                        self.tower_selector.selected_tower = None
                        self.selected_tower_type = None

                    # Check tower selection
                    for tower in self.towers:
                        dx = mouse_pos[0] - tower.x
                        dy = mouse_pos[1] - tower.y
                        if (dx*dx + dy*dy) <= (TOWER_SIZE/2)**2:
                            self.selected_tower = tower
                            self.setup_upgrade_buttons()
                            return

            # Show range when hovering over towers
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Update tower range display
                for tower in self.towers:
                    tower_center = (tower.x, tower.y)
                    distance = ((mouse_pos[0] - tower_center[0])**2 + 
                              (mouse_pos[1] - tower_center[1])**2)**0.5
                    tower.show_range = distance <= TOWER_SIZE // 2

    def draw(self):
        # Draw background and game elements
        self.draw_map()
        
        # Draw base first (under towers and enemies)
        self.draw_base()
        
        # Draw towers and enemies
        for tower in self.towers:
            tower.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw bottom UI panel
        panel_rect = pygame.Rect(0, WINDOW_HEIGHT - self.ui_panel_height, WINDOW_WIDTH, self.ui_panel_height)
        pygame.draw.rect(self.screen, UI_PANEL, panel_rect)
        pygame.draw.line(self.screen, UI_BORDER, (0, panel_rect.y), (WINDOW_WIDTH, panel_rect.y), 2)
        
        # Draw UI elements
        self.draw_speed_button()
        self.draw_start_button()
        
        # Draw stats in top bar with nice background
        stats_height = 40
        stats_rect = pygame.Rect(0, 0, WINDOW_WIDTH, stats_height)
        pygame.draw.rect(self.screen, UI_PANEL, stats_rect)
        pygame.draw.line(self.screen, UI_BORDER, (0, stats_height), (WINDOW_WIDTH, stats_height), 2)
        
        # Draw wave and health with new positioning
        wave_text = self.font.render(f"Wave: {self.wave_number}", True, UI_TEXT)
        self.screen.blit(wave_text, (20, 10))
        
        money_text = self.font.render(f"Money: ${self.money}", True, UI_TEXT)
        money_rect = money_text.get_rect(centerx=WINDOW_WIDTH // 2, centery=20)
        self.screen.blit(money_text, money_rect)
        
        health_text = self.font.render(f"Base Health: {self.base_health}", True, UI_TEXT)
        health_rect = health_text.get_rect(right=WINDOW_WIDTH - 20, centery=20)
        self.screen.blit(health_text, health_rect)
        
        # Draw tower selector in bottom panel
        self.tower_selector.draw(self.screen)
        
        # Draw upgrade panel if tower is selected
        if self.selected_tower:
            self.draw_upgrade_panel()
            
        # Draw tower placement preview
        mouse_pos = pygame.mouse.get_pos()
        if self.selected_tower_type and self.is_valid_tower_position(*mouse_pos):
            self.draw_placement_preview(mouse_pos)
            
        pygame.display.flip()
        self.clock.tick(60)

class GameState:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.current_state = "title"  # title, shop, or game
        self.title_screen = TitleScreen()
        self.loadout = LoadoutSystem()
        self.shop = Shop(self.loadout)
        self.game = None
        self.money = STARTING_MONEY
        self.selected_difficulty = None
        
    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.current_state == "title":
                        action, difficulty = self.title_screen.handle_click(mouse_pos)
                        if action == "start_game":
                            self.selected_difficulty = difficulty
                            self.game = Game()
                            # Apply difficulty settings
                            self.game.money = DIFFICULTIES[difficulty]["starting_money"]
                            self.current_state = "game"
                        elif action == "shop":
                            self.current_state = "shop"
                            
                    elif self.current_state == "shop":
                        # Handle shop clicks
                        for tower_type, button in self.shop.tower_buttons.items():
                            if (button.is_clicked(mouse_pos) and 
                                tower_type not in self.loadout.unlocked_towers and 
                                self.money >= SHOP_TOWERS[tower_type]["unlock_cost"]):
                                self.money -= SHOP_TOWERS[tower_type]["unlock_cost"]
                                self.loadout.unlocked_towers.append(tower_type)
                        
                        # Add back button logic
                        back_rect = pygame.Rect(20, WINDOW_HEIGHT - 60, 120, 40)
                        if back_rect.collidepoint(mouse_pos):
                            self.current_state = "title"

            # Update and draw current state
            if self.current_state == "title":
                self.title_screen.draw(self.screen)
            elif self.current_state == "shop":
                self.screen.fill((50, 50, 50))
                self.shop.draw(self.screen, self.money)
                # Draw back button
                back_button = Button(20, WINDOW_HEIGHT - 60, 120, 40, "Back")
                back_button.draw(self.screen)
                # Draw loadout
                self.loadout.draw(self.screen)
            elif self.current_state == "game":
                # Pass the events to the game
                self.game.handle_events(events)
                self.game.update()
                self.game.draw()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game_state = GameState()
    game_state.run()