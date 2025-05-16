import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, UI_PANEL, UI_BORDER, UI_TEXT
from .menu import Button

class SettingsMenu:
    def __init__(self):
        self.panel_width = 400
        self.panel_height = 500
        self.x = (WINDOW_WIDTH - self.panel_width) // 2
        self.y = (WINDOW_HEIGHT - self.panel_height) // 2
        
        # Settings state
        self.settings = {
            'music_volume': 0.7,
            'sfx_volume': 0.8,
            'show_range_circles': True,
            'wave_countdown': True,
            'show_damage_numbers': True
        }
        
        # Create sliders and toggles
        self.create_controls()
        
        # Back button
        self.back_button = Button(
            self.x + self.panel_width//2 - 100,
            self.y + self.panel_height - 70,
            200, 50, "Back"
        )
        
    def create_controls(self):
        # Volume sliders
        self.sliders = {
            'music_volume': {
                'rect': pygame.Rect(self.x + 50, self.y + 100, 300, 20),
                'label': "Music Volume",
                'grabbed': False
            },
            'sfx_volume': {
                'rect': pygame.Rect(self.x + 50, self.y + 170, 300, 20),
                'label': "SFX Volume",
                'grabbed': False
            }
        }
        
        # Toggle buttons
        self.toggles = {
            'show_range_circles': {
                'rect': pygame.Rect(self.x + 50, self.y + 240, 30, 30),
                'label': "Show Tower Range",
                'value': self.settings['show_range_circles']
            },
            'wave_countdown': {
                'rect': pygame.Rect(self.x + 50, self.y + 290, 30, 30),
                'label': "Show Wave Countdown",
                'value': self.settings['wave_countdown']
            },
            'show_damage_numbers': {
                'rect': pygame.Rect(self.x + 50, self.y + 340, 30, 30),
                'label': "Show Damage Numbers",
                'value': self.settings['show_damage_numbers']
            }
        }
        
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
        font = pygame.font.Font(None, 48)
        title = font.render("Settings", True, UI_TEXT)
        screen.blit(title, (self.x + (self.panel_width - title.get_width())//2, self.y + 30))
        
        # Draw sliders
        label_font = pygame.font.Font(None, 32)
        for slider_info in self.sliders.values():
            # Draw label
            label = label_font.render(slider_info['label'], True, UI_TEXT)
            screen.blit(label, (slider_info['rect'].x, slider_info['rect'].y - 25))
            
            # Draw slider background
            pygame.draw.rect(screen, (60, 60, 60), slider_info['rect'])
            pygame.draw.rect(screen, UI_BORDER, slider_info['rect'], 2)
            
            # Draw slider handle
            handle_x = slider_info['rect'].x + slider_info['rect'].width * self.settings[slider_info['label'].lower().replace(' ', '_')]
            handle_rect = pygame.Rect(handle_x - 8, slider_info['rect'].y - 5, 16, 30)
            pygame.draw.rect(screen, UI_TEXT, handle_rect, border_radius=8)
        
        # Draw toggles
        for toggle_info in self.toggles.values():
            # Draw label
            label = label_font.render(toggle_info['label'], True, UI_TEXT)
            screen.blit(label, (toggle_info['rect'].x + 40, toggle_info['rect'].y + 5))
            
            # Draw checkbox
            pygame.draw.rect(screen, (60, 60, 60), toggle_info['rect'])
            pygame.draw.rect(screen, UI_BORDER, toggle_info['rect'], 2)
            
            # Draw check if enabled
            if toggle_info['value']:
                checkmark_points = [
                    (toggle_info['rect'].x + 7, toggle_info['rect'].y + 15),
                    (toggle_info['rect'].x + 12, toggle_info['rect'].y + 20),
                    (toggle_info['rect'].x + 23, toggle_info['rect'].y + 10)
                ]
                pygame.draw.lines(screen, UI_TEXT, False, checkmark_points, 3)
        
        # Draw back button
        self.back_button.draw(screen)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Check slider interaction
            for slider_info in self.sliders.values():
                if slider_info['rect'].collidepoint(mouse_pos):
                    slider_info['grabbed'] = True
                    # Update value based on click position
                    rel_x = (mouse_pos[0] - slider_info['rect'].x) / slider_info['rect'].width
                    rel_x = max(0, min(1, rel_x))
                    self.settings[slider_info['label'].lower().replace(' ', '_')] = rel_x
                    
            # Check toggle interaction
            for toggle_info in self.toggles.values():
                if toggle_info['rect'].collidepoint(mouse_pos):
                    toggle_info['value'] = not toggle_info['value']
                    self.settings[toggle_info['label'].lower().replace(' ', '_')] = toggle_info['value']
                    
            # Check back button
            if self.back_button.handle_event(event):
                return "back"
                
        elif event.type == pygame.MOUSEBUTTONUP:
            # Release all sliders
            for slider_info in self.sliders.values():
                slider_info['grabbed'] = False
                
        elif event.type == pygame.MOUSEMOTION:
            # Update grabbed sliders
            for slider_info in self.sliders.values():
                if slider_info['grabbed']:
                    rel_x = (event.pos[0] - slider_info['rect'].x) / slider_info['rect'].width
                    rel_x = max(0, min(1, rel_x))
                    self.settings[slider_info['label'].lower().replace(' ', '_')] = rel_x
                    
        return None