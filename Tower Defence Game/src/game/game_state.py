import pygame
import math
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, INITIAL_TOWERS, 
                     STARTING_MONEY)
from src.ui.menu import MainMenu, PauseMenu
from src.ui.settings_menu import SettingsMenu
from src.ui.difficulty_menu import DifficultyMenu
from src.ui.shop_menu import ShopMenu
from src.game.demo_game import GameDemo
from src.game.game import Game

class LoadoutSystem:
    def __init__(self):
        self.unlocked_towers = INITIAL_TOWERS.copy()  # Start with just 3 towers
        self.owned_towers = []  # Additional towers bought from shop
        
    def add_tower(self, tower_type):
        """Add a new tower type to owned towers after purchase"""
        if tower_type not in self.unlocked_towers and tower_type not in self.owned_towers:
            self.owned_towers.append(tower_type)
            
    def get_available_towers(self):
        """Get all towers available to the player"""
        return self.unlocked_towers + self.owned_towers

class GameState:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.loadout = LoadoutSystem()
        
        # Initialize all game states
        self.current_state = "main_menu"
        self.main_menu = MainMenu()
        self.difficulty_menu = DifficultyMenu()
        self.pause_menu = PauseMenu()
        self.settings_menu = SettingsMenu()
        self.shop_menu = ShopMenu()
        self.demo_game = GameDemo()  # Background gameplay for main menu
        self.game = None
        
        # State flags
        self.is_paused = False
        self.in_settings = False
        self.in_shop = False
        self.selected_difficulty = None
        self.previous_state = None  # For returning from settings
        self.money = STARTING_MONEY["normal"]  # Default starting money

        self.enemies_remaining = 0
        self.in_intermission = False
        self.intermission_timer = 0
        self.INTERMISSION_DURATION = 5000  # 5 seconds
        self.score_multiplier = 1
        self.kill_streak = 0
        
    def run(self):
        while True:
            # Get all events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state == "game":
                            if self.in_settings:
                                self.in_settings = False
                            else:
                                self.is_paused = not self.is_paused
                        elif self.in_settings:
                            self.in_settings = False
                            self.current_state = self.previous_state
                        
                self.handle_event(event)
            
            # Update
            self.update()
            
            # Draw
            self.draw()
            
            # Maintain 60 FPS
            self.clock.tick(60)
            
    def handle_event(self, event):
        if self.in_settings:
            action = self.settings_menu.handle_event(event)
            if action == "back":
                self.in_settings = False
                self.current_state = self.previous_state
            return

        if self.in_shop and event.type == pygame.MOUSEBUTTONDOWN:
            result = self.shop_menu.handle_click(event.pos, self.loadout, self.money)
            if result == "back":
                self.in_shop = False
                self.current_state = self.previous_state
            elif result and isinstance(result, tuple) and result[0] == "buy":
                _, tower_type, cost = result
                self.money -= cost
            return
            
        if self.current_state == "main_menu":
            action = self.main_menu.handle_event(event)
            if action == "play":
                self.current_state = "difficulty_menu"
            elif action == "settings":
                self.previous_state = self.current_state
                self.in_settings = True
            elif action == "shop":
                self.previous_state = self.current_state
                self.in_shop = True
                
        elif self.current_state == "difficulty_menu":
            action = self.difficulty_menu.handle_event(event)
            if action in ["easy", "normal", "hard"]:
                self.selected_difficulty = action
                self.game = Game(self.selected_difficulty)
                self.current_state = "game"
                self.game.game_started = True  # Auto-start game
            elif action == "back":
                self.current_state = "main_menu"
                
        elif self.current_state == "game":
            if self.is_paused:
                action = self.pause_menu.handle_event(event)
                if action == "resume":
                    self.is_paused = False
                elif action == "settings":
                    self.previous_state = "game"
                    self.in_settings = True
                elif action == "main_menu":
                    self.current_state = "main_menu"
                    self.is_paused = False
                    self.game = None
            else:
                result = self.game.handle_events([event])
                if isinstance(result, tuple) and result[0] == "money":
                    _, amount = result
                    self.money += amount
                
    def update(self):
        if self.current_state == "main_menu":
            self.demo_game.update()  # Update background gameplay
        elif self.current_state == "game" and not self.is_paused and not self.in_settings:
            self.game.update()
            if self.wave_manager.active_wave:
                self.enemies_remaining = len(self.wave_manager.active_wave.enemies)
                if self.enemies_remaining == 0:
                    self.wave_manager.wave_timer = 0  # Skip timer when all enemies dead

            # Handle intermission after boss waves
            if self.wave_manager.current_wave % 5 == 0 and self.enemies_remaining == 0:
                self.in_intermission = True
                self.intermission_timer = pygame.time.get_ticks()

            if self.in_intermission:
                if pygame.time.get_ticks() - self.intermission_timer >= self.INTERMISSION_DURATION:
                    self.in_intermission = False
                    self.wave_manager.start_next_wave()
            
    def draw(self):
        if self.current_state == "main_menu":
            self.main_menu.draw(self.screen, self.demo_game)
        elif self.current_state == "difficulty_menu":
            self.main_menu.draw(self.screen, self.demo_game)  # Keep background
            self.difficulty_menu.draw(self.screen)
        elif self.current_state == "game":
            self.game.draw()
            if self.is_paused:
                self.pause_menu.draw(self.screen)
            self._draw_ui(self.screen)
        
        # Draw shop menu over any state if active
        if self.in_shop:
            self.shop_menu.draw(self.screen, self.loadout, self.money)
        
        # Draw settings menu over any state if active
        if self.in_settings:
            self.settings_menu.draw(self.screen)
                
        pygame.display.flip()
        
    def _draw_ui(self, screen):
        font = pygame.font.Font(None, 36)
        
        # Draw enemies remaining
        enemies_text = f"Enemies Remaining: {self.enemies_remaining}"
        text_surface = font.render(enemies_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        
        # Draw kill streak and multiplier
        streak_text = f"Kill Streak: {self.kill_streak} (x{self.score_multiplier})"
        streak_surface = font.render(streak_text, True, (255, 255, 0))
        screen.blit(streak_surface, (10, 50))
        
        # Draw intermission
        if self.in_intermission:
            font_large = pygame.font.Font(None, 72)
            intermission_text = "INTERMISSION!"
            text_surface = font_large.render(intermission_text, True, (255, 165, 0))
            screen.blit(text_surface, (
                screen.get_width()//2 - text_surface.get_width()//2,
                screen.get_height()//2 - text_surface.get_height()//2
            ))