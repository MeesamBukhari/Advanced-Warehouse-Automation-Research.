import pygame

class Theme:
    # Cyberpunk-Tactical Palette
    BACKGROUND = (5, 5, 20)        # Near-black indigo
    SURFACE = (15, 15, 45, 180)    # Deep indigo translucent
    PANEL_BORDER = (0, 255, 255)   # Cyan Neon
    
    PRIMARY = (0, 255, 180)        # Neon Mint (Robot)
    SECONDARY = (180, 0, 255)      # Neon Purple (Path)
    ACCENT = (255, 200, 0)         # Neon Gold (Items)
    DANGER = (255, 50, 50)         # Neon Red (Obstacles)
    
    TEXT_MAIN = (200, 240, 255)    # Light Cyan
    TEXT_DIM = (100, 140, 180)     # Dim Blue
    
    # Grid Colors (Tactical)
    GRID_EMPTY = (10, 10, 35)
    GRID_SHELF = (30, 30, 70)
    GRID_OBSTACLE = (100, 0, 40)
    GRID_PATH = (180, 0, 255, 150)
    GRID_EXPLORED = (40, 40, 100, 80)
    GRID_TRAIL = (0, 255, 180, 200)
    
    # Scanline Effect
    SCANLINE = (0, 255, 255, 15)

    # Fonts
    FONT_SIZE_L = 40
    FONT_SIZE_M = 28
    FONT_SIZE_S = 18

    @classmethod
    def get_font(cls, size, bold=True):
        try:
            return pygame.font.SysFont("Consolas, Courier New, monospace", size, bold=bold)
        except:
            return pygame.font.SysFont("monospace", size, bold=bold)
