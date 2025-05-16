import pygame
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, TOWER_TYPES, PANEL_HEIGHT, 
                     UI_PANEL, UI_BORDER, UI_TEXT, UI_BUTTON, UI_BUTTON_HOVER, INITIAL_TOWERS)

class TowerSelector:
    def __init__(self):
        self.panel_rect = pygame.Rect(0, WINDOW_HEIGHT - PANEL_HEIGHT, 
                                    WINDOW_WIDTH, PANEL_HEIGHT)
        self.selected_tower = None
        self.hover_tower = None
        self.unlocked_towers = INITIAL_TOWERS.copy()  # Start with 3 basic towers
        self.buttons = self._create_tower_buttons()
        self.font = pygame.font.Font(None, 24)
        self.stats_font = pygame.font.Font(None, 20)
        self.is_collapsed = True
        self.toggle_button = pygame.Rect(10, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 
                                       40, 40)
        
    def _create_tower_buttons(self):
        buttons = {}
        x_offset = 70  # Start position for first tower
        y_center = WINDOW_HEIGHT - PANEL_HEIGHT/2
        
        # Only create buttons for unlocked towers
        for tower_type in self.unlocked_towers:
            if tower_type in TOWER_TYPES:
                button_rect = pygame.Rect(x_offset, y_center - 25, 50, 50)
                buttons[tower_type] = {
                    "rect": button_rect,
                    "stats": TOWER_TYPES[tower_type],
                    "original_x": x_offset
                }
                x_offset += 70
            
        return buttons
        
    def add_tower(self, tower_type):
        if tower_type not in self.unlocked_towers:
            self.unlocked_towers.append(tower_type)
            self.buttons = self._create_tower_buttons()

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            self.hover_tower = None
            if not self.is_collapsed:
                for tower_type, button in self.buttons.items():
                    if button["rect"].collidepoint(mouse_pos):
                        self.hover_tower = tower_type
                        break
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check toggle button first
                if self.toggle_button.collidepoint(mouse_pos):
                    self.is_collapsed = not self.is_collapsed
                    return False
                
                # Handle tower selection if menu is expanded
                if not self.is_collapsed:
                    for tower_type, button in self.buttons.items():
                        if button["rect"].collidepoint(mouse_pos):
                            # Toggle selection
                            if self.selected_tower == tower_type:
                                self.selected_tower = None
                            else:
                                self.selected_tower = tower_type
                            return True
                        
        return False
        
    def draw(self, screen, money):
        # Draw panel background
        pygame.draw.rect(screen, UI_PANEL, self.panel_rect)
        pygame.draw.rect(screen, UI_BORDER, self.panel_rect, 2)
        
        # Draw toggle button
        pygame.draw.rect(screen, UI_BUTTON_HOVER if self.is_collapsed else UI_BUTTON, 
                        self.toggle_button)
        pygame.draw.rect(screen, UI_BORDER, self.toggle_button, 2)
        
        # Draw arrow
        arrow_points = []
        if self.is_collapsed:
            # Right arrow
            arrow_points = [
                (self.toggle_button.x + 15, self.toggle_button.y + 20),
                (self.toggle_button.x + 30, self.toggle_button.y + 20),
                (self.toggle_button.x + 25, self.toggle_button.y + 15),
                (self.toggle_button.x + 25, self.toggle_button.y + 25)
            ]
        else:
            # Left arrow
            arrow_points = [
                (self.toggle_button.x + 30, self.toggle_button.y + 20),
                (self.toggle_button.x + 15, self.toggle_button.y + 20),
                (self.toggle_button.x + 20, self.toggle_button.y + 15),
                (self.toggle_button.x + 20, self.toggle_button.y + 25)
            ]
        pygame.draw.polygon(screen, UI_TEXT, arrow_points)
        
        # Update tower button positions based on collapse state
        target_x = -200 if self.is_collapsed else 0  # Move buttons off screen when collapsed
        
        # Draw tower buttons
        for tower_type, button in self.buttons.items():
            stats = button["stats"]
            original_x = button["original_x"]
            
            # Animate button position
            current_x = button["rect"].x
            new_x = original_x + target_x
            button["rect"].x = new_x
            
            if not self.is_collapsed:
                # Draw button background
                color = stats["color"]
                if tower_type == self.selected_tower:
                    # Selected state
                    pygame.draw.rect(screen, (color[0]//2, color[1]//2, color[2]//2), 
                                   button["rect"])
                    pygame.draw.rect(screen, UI_BORDER, button["rect"], 3)
                elif tower_type == self.hover_tower:
                    # Hover state
                    pygame.draw.rect(screen, (min(color[0]*1.2, 255), 
                                            min(color[1]*1.2, 255), 
                                            min(color[2]*1.2, 255)), button["rect"])
                    pygame.draw.rect(screen, UI_BORDER, button["rect"], 2)
                else:
                    # Normal state
                    pygame.draw.rect(screen, color, button["rect"])
                    pygame.draw.rect(screen, UI_BORDER, button["rect"], 1)
                    
                # Draw tower preview
                center_x = button["rect"].centerx
                center_y = button["rect"].centery
                pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), 15)
                
                # Draw cost
                cost_text = self.font.render(str(stats["cost"]), True, 
                                           UI_TEXT if money >= stats["cost"] else (255, 0, 0))
                cost_rect = cost_text.get_rect(centerx=center_x, top=button["rect"].bottom + 5)
                screen.blit(cost_text, cost_rect)
            
        # Draw hover tooltip with detailed stats
        if self.hover_tower and self.hover_tower in self.buttons and not self.is_collapsed:
            stats = self.buttons[self.hover_tower]["stats"]
            tooltip_text = [
                f"Type: {self.hover_tower.title()}",
                f"Damage: {stats['damage']}",
                f"Range: {stats['range']}",
                f"Fire Rate: {60//stats['fire_rate']}/s"
            ]
            if "splash_damage" in stats:
                tooltip_text.append(f"Splash: {stats['splash_damage']}")
                
            # Draw tooltip background
            padding = 5
            line_height = 20
            tooltip_width = 150
            tooltip_height = len(tooltip_text) * line_height + padding * 2
            tooltip_x = self.buttons[self.hover_tower]["rect"].right + 10
            tooltip_y = self.buttons[self.hover_tower]["rect"].top
            
            pygame.draw.rect(screen, UI_PANEL, 
                           (tooltip_x, tooltip_y, tooltip_width, tooltip_height))
            pygame.draw.rect(screen, UI_BORDER, 
                           (tooltip_x, tooltip_y, tooltip_width, tooltip_height), 1)
            
            # Draw tooltip text
            for i, line in enumerate(tooltip_text):
                text = self.stats_font.render(line, True, UI_TEXT)
                screen.blit(text, (tooltip_x + padding, 
                                 tooltip_y + padding + i * line_height))