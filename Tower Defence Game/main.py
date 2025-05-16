import pygame
from src.game.game_state import GameState

def main():
    # Initialize game state manager
    game_state = GameState()
    
    # Start game loop
    game_state.run()

if __name__ == "__main__":
    main()