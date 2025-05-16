import pygame
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, UI_PANEL, UI_BORDER, UI_TEXT,
                     TOWER_TYPES, SHOP_TOWERS)

class ShopMenu:
    def __init__(self):
        self.panel_width = 600
        self.panel_height = 400
        self.x = (WINDOW_WIDTH - self.panel_width) // 2
        self.y = (WINDOW_HEIGHT - self.panel_height) // 2
        
        # Create tower display rectangles
        self.tower_rects = {}
        self.setup_tower_displays()
        
        # Back button
        self.back_button = pygame.Rect(
            self.x + self.panel_width//2 - 60,
            self.y + self.panel_height - 60,
            120, 40
        )
        
        # Fonts
        self.font_big = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 24)
        
    def setup_tower_displays(self):
        tower_width = 150
        tower_height = 200
        spacing = 20
        start_x = self.x + spacing
        start_y = self.y + 80
        
        x = start_x
        for tower_type, info in SHOP_TOWERS.items():
            self.tower_rects[tower_type] = {
                "rect": pygame.Rect(x, start_y, tower_width, tower_height),
                "info": info
            }
            x += tower_width + spacing
            
    def draw(self, screen, loadout_system, money):
        # Draw semi-transparent background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw main panel
        pygame.draw.rect(screen, UI_PANEL,
                        (self.x, self.y, self.panel_width, self.panel_height))
        pygame.draw.rect(screen, UI_BORDER,
                        (self.x, self.y, self.panel_width, self.panel_height), 2)
        
        # Draw title
        title = self.font_big.render("Tower Shop", True, UI_TEXT)
        screen.blit(title, (self.x + (self.panel_width - title.get_width())//2, self.y + 20))
        
        # Draw money
        money_text = self.font_big.render(f"${money}", True, UI_TEXT)
        screen.blit(money_text, (self.x + 20, self.y + 20))
        
        # Draw towers
        for tower_type, data in self.tower_rects.items():
            rect = data["rect"]
            info = data["info"]
            stats = TOWER_TYPES[tower_type]
            
            # Draw tower panel
            pygame.draw.rect(screen, (60, 60, 60), rect)
            pygame.draw.rect(screen, UI_BORDER, rect, 2)
            
            # Draw tower preview
            preview_size = 40
            preview_x = rect.centerx
            preview_y = rect.y + 50
            pygame.draw.circle(screen, stats["color"],
                             (preview_x, preview_y), preview_size//2)
            
            # Draw tower info
            name = self.font.render(tower_type.title(), True, UI_TEXT)
            screen.blit(name, (rect.x + 10, rect.y + 10))
            
            # Draw stats
            y = preview_y + 40
            stat_texts = [
                f"Damage: {stats['damage']}",
                f"Range: {stats['range']}",
                f"Fire Rate: {60//stats['fire_rate']}/s"
            ]
            if "splash_damage" in stats:
                stat_texts.append(f"Splash: {stats['splash_damage']}")
                
            for text in stat_texts:
                stat = self.font.render(text, True, UI_TEXT)
                screen.blit(stat, (rect.x + 10, y))
                y += 20
            
            # Draw cost/status
            if tower_type in loadout_system.get_available_towers():
                status = self.font.render("Owned", True, (0, 255, 0))
            else:
                cost = info["unlock_cost"]
                color = (255, 0, 0) if money < cost else (0, 255, 0)
                status = self.font.render(f"Cost: ${cost}", True, color)
            screen.blit(status, (rect.x + 10, rect.bottom - 30))
            
            # Draw description
            desc = self.font.render(info["description"], True, UI_TEXT)
            screen.blit(desc, (rect.x + 10, rect.bottom - 50))
        
        # Draw back button
        pygame.draw.rect(screen, (80, 80, 80), self.back_button)
        pygame.draw.rect(screen, UI_BORDER, self.back_button, 2)
        back_text = self.font.render("Back", True, UI_TEXT)
        text_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, text_rect)
        
    def handle_click(self, pos, loadout_system, money):
        """Handle mouse clicks in the shop menu"""
        if self.back_button.collidepoint(pos):
            return "back"
            
        # Check tower purchases
        for tower_type, data in self.tower_rects.items():
            if (data["rect"].collidepoint(pos) and 
                tower_type not in loadout_system.get_available_towers()):
                cost = data["info"]["unlock_cost"]
                if money >= cost:
                    loadout_system.add_tower(tower_type)
                    return ("buy", tower_type, cost)
                    
        return None