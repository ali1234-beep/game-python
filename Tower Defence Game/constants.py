import pygame

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Base Settings
BASE_POSITION = (750, 300)  # End of path
BASE_SIZE = 120  # Larger for bridge appearance
BASE_HEALTH = 1000  # More health since enemies die on contact
SHAKE_INTENSITY = 5  # Intensity of shake effect when base is hit

# Game Settings
STARTING_MONEY = {
    "easy": 200,
    "normal": 150,
    "hard": 100
}
STARTING_LIVES = 10
ENEMY_SIZE = 20
BOSS_SIZE = 35  # Regular boss size
PROJECTILE_SPEED = 10
ENEMY_SPEED = 2
PANEL_HEIGHT = 100

# Boss Settings
BOSS_REWARD = 500  # Regular boss reward
BOSS_HEALTH_MULTIPLIER = 3.0  # Regular boss health multiplier

# Enemy Health and Scaling
STARTING_ENEMY_HEALTH = 50  # Lower starting health
HEALTH_SCALING_FACTOR = 1.1  # More gradual scaling
MAX_HEALTH_CAP = 10000  # Cap for regular enemies

# UI Colors
UI_PANEL = (50, 50, 50)
UI_BORDER = (100, 100, 100)
UI_TEXT = (255, 255, 255)
UI_BUTTON = (70, 70, 70)
UI_BUTTON_HOVER = (90, 90, 90)
UI_BUTTON_SELECTED = (30, 30, 30)
UI_HIGHLIGHT = (0, 255, 255)  # Cyan highlight color for UI elements
UI_BACKGROUND = (34, 34, 34)  # Dark background color

# Path Points (define the path enemies follow)
PATH_POINTS = [
    (0, 300),  # Start point
    (200, 300),
    (200, 100),
    (400, 100),
    (400, 500),
    (600, 500),
    (600, 300),
    (750, 300)  # End point at bridge
]

# Tower Types and Stats
TOWER_TYPES = {
    "basic": {
        "cost": 100,
        "damage": 20,
        "range": 150,
        "fire_rate": 30,  # Frames between shots
        "color": (200, 200, 200)
    },
    "rapid": {
        "cost": 150,
        "damage": 10,
        "range": 120,
        "fire_rate": 10,
        "color": (0, 255, 255)
    },
    "sniper": {
        "cost": 250,
        "damage": 100,
        "range": 300,
        "fire_rate": 90,
        "color": (255, 0, 0)
    },
    "splash": {
        "cost": 200,
        "damage": 15,
        "range": 130,
        "fire_rate": 45,
        "splash_damage": 8,
        "splash_range": 50,
        "color": (255, 165, 0)
    },
    "missile": {
        "cost": 300,
        "damage": 50,
        "range": 200,
        "fire_rate": 60,
        "splash_damage": 25,
        "splash_range": 80,
        "color": (255, 255, 0)
    }
}

# Initial Tower Selection
INITIAL_TOWERS = ["basic", "rapid", "sniper"]  # Player starts with these 3 towers

# Shop Configuration
SHOP_TOWERS = {
    "splash": {
        "unlock_cost": 1000,
        "description": "Area damage, medium range"
    },
    "missile": {
        "unlock_cost": 1500,
        "description": "High damage, splash effect"
    }
}

# Upgrade Costs and Limits
UPGRADE_COSTS = {
    "damage": 100,
    "range": 75,
    "fire_rate": 150,
    "splash_damage": 200
}

MAX_UPGRADE_LEVEL = 3

# Wave Settings
WAVE_TIMER = 25  # 25 seconds between waves
WAVE_ENEMY_COUNT = 8  # Start with fewer enemies per wave
BOSS_WAVE_INTERVAL = 10  # Boss every 10 waves

# Special Boss Settings
LEVEL_100_BOSS = {
    "health_multiplier": 50,
    "size": 60,
    "speed_multiplier": 0.7,
    "reward": 2000,
    "color": (180, 0, 180)  # Purple color for special boss
}

# Boss Wave Rewards
BOSS_REWARD = 500  # Extra money for defeating a boss wave

# Difficulty Settings
DIFFICULTIES = {
    "easy": {
        "health_multiplier": 0.8,
        "money_multiplier": 1.2,
        "enemy_speed_multiplier": 0.8,
        "starting_money": 200  # More starting money for easy mode
    },
    "normal": {
        "health_multiplier": 1.0,
        "money_multiplier": 1.0,
        "enemy_speed_multiplier": 1.0,
        "starting_money": 150  # Standard starting money
    },
    "hard": {
        "health_multiplier": 1.2,
        "money_multiplier": 0.8,
        "enemy_speed_multiplier": 1.2,
        "starting_money": 100   # Less starting money for hard mode
    }
}