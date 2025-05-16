import pygame
import math
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, UI_PANEL, UI_BORDER, UI_TEXT, UI_HIGHLIGHT, UI_BACKGROUND

class Button:
    def __init__(self, x, y, width, height, text, color=(60, 63, 65), hover_color=(80, 83, 85)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        self.click_time = 0
        self.animation_duration = 10
        
    def draw(self, screen):
        # Calculate button animation
        current_time = pygame.time.get_ticks()
        animation_progress = max(0, min(1, (current_time - self.click_time) / self.animation_duration))
        
        # Draw button with animation
        color = self.hover_color if self.is_hovered else self.color
        if animation_progress < 1:
            # Scale button slightly during click animation
            scale = 0.95 + 0.05 * animation_progress
            width = int(self.rect.width * scale)
            height = int(self.rect.height * scale)
            x = self.rect.centerx - width//2
            y = self.rect.centery - height//2
            rect = pygame.Rect(x, y, width, height)
        else:
            rect = self.rect
            
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, UI_BORDER, rect, 2, border_radius=8)
        
        # Draw text with shadow
        text_surface = self.font.render(self.text, True, UI_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        
        # Draw shadow
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click_time = pygame.time.get_ticks()
                return True
        return False

class MainMenu:
    def __init__(self):
        # Create stylized buttons with different colors for each function
        button_width = 200
        button_height = 50
        button_x = 50
        button_spacing = 20
        
        self.buttons = {
            'play': Button(button_x, 200, button_width, button_height, 
                         "Play", (40, 120, 40), (60, 140, 60)),
            'shop': Button(button_x, 200 + (button_height + button_spacing), 
                         button_width, button_height, 
                         "Shop", (120, 40, 40), (140, 60, 60)),
            'settings': Button(button_x, 200 + 2 * (button_height + button_spacing), 
                             button_width, button_height, 
                             "Settings", (40, 40, 120), (60, 60, 140)),
            'audio': Button(button_x, 200 + 3 * (button_height + button_spacing), 
                          button_width, button_height, 
                          "Audio", (120, 120, 40), (140, 140, 60))
        }
        
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.background_alpha = 128
        
        # Title animation
        self.title_bounce = 0
        self.title_bounce_speed = 0.1
        self.title_offset = 0
        
    def update(self):
        # Update title bounce animation
        self.title_bounce += self.title_bounce_speed
        self.title_offset = math.sin(self.title_bounce) * 5
        
    def draw(self, screen, demo_game=None):
        # Draw demo gameplay in background if available
        if demo_game:
            demo_game.draw(screen)
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(self.background_alpha)
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(UI_BACKGROUND)
        
        # Draw animated title with glow effect
        title_text = "Tower Defense"
        glow_surfaces = []
        
        # Create glow effect
        for i in range(3):
            size = 72 + i * 2
            font = pygame.font.Font(None, size)
            glow = font.render(title_text, True, (80, 80, 100))
            glow.set_alpha(50 - i * 15)
            glow_rect = glow.get_rect(center=(WINDOW_WIDTH//4, 80 + self.title_offset))
            glow_surfaces.append((glow, glow_rect))
            
        # Draw glow layers
        for glow, rect in glow_surfaces:
            screen.blit(glow, rect)
            
        # Draw main title
        title = self.title_font.render(title_text, True, UI_TEXT)
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        
        # Draw shadow
        screen.blit(title_shadow, (WINDOW_WIDTH//4 - title.get_width()//2 + 2, 
                                 82 + self.title_offset))
        # Draw title
        screen.blit(title, (WINDOW_WIDTH//4 - title.get_width()//2, 
                           80 + self.title_offset))
        
        # Draw subtitle
        subtitle = self.subtitle_font.render("Choose Your Path", True, UI_HIGHLIGHT)
        screen.blit(subtitle, (80, 140))
        
        # Draw all buttons
        for button in self.buttons.values():
            button.draw(screen)
            
    def handle_event(self, event):
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                return button_name
        return None

class PauseMenu:
    def __init__(self):
        width = 300
        height = 400
        x = (WINDOW_WIDTH - width) // 2
        y = (WINDOW_HEIGHT - height) // 2
        
        self.panel_rect = pygame.Rect(x, y, width, height)
        button_width = 200
        button_height = 50
        button_x = x + width//2 - button_width//2
        button_spacing = 20
        
        self.buttons = {
            'resume': Button(button_x, y + 100, button_width, button_height, 
                           "Resume", (40, 120, 40)),
            'settings': Button(button_x, y + 100 + (button_height + button_spacing), 
                             button_width, button_height, 
                             "Settings", (40, 40, 120)),
            'main_menu': Button(button_x, y + 100 + 2 * (button_height + button_spacing), 
                              button_width, button_height, 
                              "Main Menu", (120, 40, 40))
        }
        
    def draw(self, screen):
        # Draw semi-transparent background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw panel with border
        pygame.draw.rect(screen, UI_PANEL, self.panel_rect, border_radius=10)
        pygame.draw.rect(screen, UI_BORDER, self.panel_rect, 2, border_radius=10)
        
        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("Paused", True, UI_TEXT)
        screen.blit(title, (self.panel_rect.centerx - title.get_width()//2, 
                           self.panel_rect.y + 30))
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(screen)
            
    def handle_event(self, event):
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                return button_name
        return None