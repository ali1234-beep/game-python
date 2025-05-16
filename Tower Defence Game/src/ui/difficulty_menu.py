import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, UI_PANEL, UI_BORDER, UI_TEXT, DIFFICULTIES
from .menu import Button

class DifficultyMenu:
    def __init__(self):
        self.panel_width = 400
        self.panel_height = 500
        self.x = (WINDOW_WIDTH - self.panel_width) // 2
        self.y = (WINDOW_HEIGHT - self.panel_height) // 2
        
        # Create buttons with different colors for each difficulty
        self.buttons = {
            'easy': Button(self.x + 100, self.y + 150, 200, 50, "Easy", (40, 120, 40)),
            'normal': Button(self.x + 100, self.y + 220, 200, 50, "Normal", (120, 120, 40)),
            'hard': Button(self.x + 100, self.y + 290, 200, 50, "Hard", (120, 40, 40)),
            'back': Button(self.x + 100, self.y + 360, 200, 50, "Back", (80, 80, 80))
        }
        
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 24)
        self.selected_difficulty = None
        
    def draw(self, screen):
        # Draw semi-transparent background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw panel
        panel_rect = pygame.Rect(self.x, self.y, self.panel_width, self.panel_height)
        pygame.draw.rect(screen, UI_PANEL, panel_rect, border_radius=10)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 2, border_radius=10)
        
        # Draw title
        title = self.title_font.render("Select Difficulty", True, UI_TEXT)
        screen.blit(title, (self.x + (self.panel_width - title.get_width())//2, self.y + 40))
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(screen)
            
        # Draw difficulty info if one is hovered
        for diff_name, button in self.buttons.items():
            if button.is_hovered and diff_name in DIFFICULTIES:
                self.draw_difficulty_info(screen, diff_name)
                
    def draw_difficulty_info(self, screen, difficulty):
        info_x = self.x + 20
        info_y = self.y + self.panel_height - 80
        
        info_text = [
            f"Starting Money: ${DIFFICULTIES[difficulty]['starting_money']}",
            f"Enemy Health: {int(DIFFICULTIES[difficulty]['health_multiplier'] * 100)}%",
            f"Enemy Speed: {int(DIFFICULTIES[difficulty]['enemy_speed_multiplier'] * 100)}%"
        ]
        
        for text in info_text:
            text_surface = self.info_font.render(text, True, UI_TEXT)
            screen.blit(text_surface, (info_x, info_y))
            info_y += 20
            
    def handle_event(self, event):
        for diff_name, button in self.buttons.items():
            if button.handle_event(event):
                return diff_name
        return None