import pygame
import time
from gui.theme import Theme
from gui.ui_system import Panel, Slider
from gui.panels import ControlPanel, StatsPanel, ScenarioViewer
from gui.charts import create_benchmark_chart
from core.warehouse import Warehouse, Position, CellType, Robot
from core.algorithms import bfs, ucs, a_star

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Warehouse Automation Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        self.frame_count = 0
        
        # Simulation State
        self.warehouse = None
        self.robot = None
        self.current_algo = "A*"
        self.is_running = False
        self.speed = 10  # FPS for animation
        
        # UI Setup
        self.panels = []
        self.setup_ui()
        
        # Load default scenario
        self.load_scenario_from_file("scenarios/default.json")
        
        # Benchmark Data
        self.benchmark_data = {"A*": 0, "BFS": 0, "UCS": 0}
        self.chart_surf = None
        self.update_chart()

    def setup_ui(self):
        self.ctrl_panel = ControlPanel(pygame.Rect(900, 20, 360, 240), self.run_sim, self.reset_sim, self.set_algo)
        self.stats_panel = StatsPanel(pygame.Rect(900, 280, 360, 200))
        self.scen_panel = ScenarioViewer(pygame.Rect(900, 500, 360, 200), self.load_scen_data)
        
        self.speed_slider = Slider(pygame.Rect(1080, 220, 150, 10), 1, 60, 10)
        
        self.panels = [self.ctrl_panel, self.stats_panel, self.scen_panel]

    def set_algo(self, algo):
        self.current_algo = algo
        self.stats_panel.update_stats(Algorithm=algo)

    def load_scenario_from_file(self, path):
        import json
        with open(path, 'r') as f:
            data = json.load(f)
            self.load_scen_data(data)

    def load_scen_data(self, data):
        self.warehouse = Warehouse(data['width'], data['height'])
        
        # Set shelves
        for s in data.get('shelves', []):
            x, y, w, h = s
            for i in range(x, x+w):
                for j in range(y, y+h):
                    self.warehouse.set_cell(i, j, CellType.SHELF)
                    
        # Set obstacles
        for o in data.get('obstacles', []):
            x, y, w, h = o
            for i in range(x, x+w):
                for j in range(y, y+h):
                    self.warehouse.set_cell(i, j, CellType.OBSTACLE)
                    
        # Set Items
        for item in data.get('items', []):
            self.warehouse.set_cell(item[0], item[1], CellType.ITEM)
            
        # Set Robot
        start_pos = data.get('robot_start', [0, 0])
        self.warehouse.set_cell(start_pos[0], start_pos[1], CellType.ROBOT)
        self.robot = Robot(Position(start_pos[0], start_pos[1]))
        
        self.reset_sim()
        self.stats_panel.update_stats(Items=f"0/{len(data.get('items', []))}")
        self.run_benchmark()

    def run_benchmark(self):
        if not self.warehouse or not self.warehouse.items: return
        goal = list(self.warehouse.items)[0] # Just benchmark for first item
        start = self.robot.pos
        
        _, exp_a = a_star(self.warehouse, start, goal)
        _, exp_b = bfs(self.warehouse, start, goal)
        _, exp_u = ucs(self.warehouse, start, goal)
        
        self.benchmark_data = {"A*": len(exp_a), "BFS": len(exp_b), "UCS": len(exp_u)}
        self.update_chart()

    def update_chart(self):
        self.chart_surf = create_benchmark_chart(self.benchmark_data, width=320, height=180)

    def run_sim(self):
        if self.is_running or not self.warehouse.items: return
        
        goal = list(self.warehouse.items)[0] # Get first target
        start = self.robot.pos
        
        start_time = time.time()
        if self.current_algo == "A*":
            path, explored = a_star(self.warehouse, start, goal)
        elif self.current_algo == "BFS":
            path, explored = bfs(self.warehouse, start, goal)
        else:
            path, explored = ucs(self.warehouse, start, goal)
        end_time = time.time()
        
        if path:
            self.robot.set_path(path)
            self.is_running = True
            
            # Show explored on grid
            for pos in explored:
                if self.warehouse.get_cell(pos.x, pos.y) == CellType.EMPTY:
                    self.warehouse.set_cell(pos.x, pos.y, CellType.EXPLORED)
            for pos in path:
                if self.warehouse.get_cell(pos.x, pos.y) not in [CellType.ROBOT, CellType.ITEM]:
                    self.warehouse.set_cell(pos.x, pos.y, CellType.PATH)
            
            self.stats_panel.update_stats(
                Explored=len(explored),
                Time=f"{int((end_time - start_time) * 1000)}ms",
                Steps=len(path)
            )

    def reset_sim(self):
        self.is_running = False
        self.warehouse.reset_path()
        if self.robot:
            start_pos = self.warehouse.robot_pos
            self.robot.pos = start_pos
            self.robot.is_moving = False
            self.robot.trail = [start_pos]
        self.stats_panel.update_stats(Steps=0, Explored=0, Time="0ms")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for panel in self.panels:
                panel.handle_event(event)
            self.speed_slider.handle_event(event)
            self.speed = int(self.speed_slider.value)

    def update(self):
        if self.is_running and self.robot:
            finished = self.robot.update()
            if finished:
                self.is_running = False
                # Collect item logic could go here

    def draw_glow(self, color, pos, radius, strength=5):
        # Pulsating effect
        pulse = (abs(pygame.time.get_ticks() % 1000 - 500) / 500) * 0.3 + 0.7
        radius = int(radius * pulse)
        
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for r in range(strength, 0, -1):
            alpha = int(color[3] * (1 - r/strength) * pulse)
            pygame.draw.circle(surface, (*color[:3], alpha), (radius, radius), radius * r/strength)
        self.screen.blit(surface, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_ADD)

    def draw_grid_decor(self, rect):
        # Tactical corners for cells
        c = Theme.PANEL_BORDER
        l, t, w, h = rect
        pygame.draw.line(self.screen, (*c, 50), (l, t), (l+4, t))
        pygame.draw.line(self.screen, (*c, 50), (l, t), (l, t+4))
        pygame.draw.line(self.screen, (*c, 50), (l+w-4, t+h), (l+w, t+h))
        pygame.draw.line(self.screen, (*c, 50), (l+w, t+h-4), (l+w, t+h))

    def draw(self):
        self.screen.fill(Theme.BACKGROUND)
        
        # Grid Setup
        grid_size = 32
        offset_x, offset_y = 60, 80
        
        # Background Grid (Dots)
        for y in range(0, 720, 40):
            for x in range(0, 1280, 40):
                pygame.draw.circle(self.screen, (30, 30, 80), (x, y), 1)

        # Draw Cells
        for y in range(self.warehouse.height):
            for x in range(self.warehouse.width):
                cell = self.warehouse.get_cell(x, y)
                rect = pygame.Rect(offset_x + x * grid_size, offset_y + y * grid_size, grid_size - 4, grid_size - 4)
                
                # Draw cell base
                self.draw_grid_decor(rect)
                
                if cell == CellType.SHELF:
                    pygame.draw.rect(self.screen, Theme.GRID_SHELF, rect, border_radius=2)
                elif cell == CellType.OBSTACLE:
                    pygame.draw.rect(self.screen, Theme.DANGER, rect, border_radius=2)
                    self.draw_glow((*Theme.DANGER, 40), rect.center, 20)
                elif cell == CellType.ITEM: 
                    self.draw_glow((*Theme.ACCENT, 150), rect.center, 25, strength=6)
                    pygame.draw.rect(self.screen, Theme.ACCENT, rect.inflate(-8,-8), border_radius=2)
                elif cell == CellType.EXPLORED:
                    pygame.draw.rect(self.screen, Theme.GRID_EXPLORED, rect)
                elif cell == CellType.PATH:
                    pygame.draw.rect(self.screen, (*Theme.SECONDARY, 100), rect, border_radius=4)
        
        # Draw Trail
        if len(self.robot.trail) > 1:
            points = [(offset_x + p.x * grid_size + grid_size//2, offset_y + p.y * grid_size + grid_size//2) for p in self.robot.trail]
            pygame.draw.lines(self.screen, Theme.GRID_TRAIL, False, points, 2)

        # Draw Robot (Tactical Drone look)
        rx, ry = self.robot.pos.x, self.robot.pos.y
        rect_r = pygame.Rect(offset_x + rx * grid_size, offset_y + ry * grid_size, grid_size - 4, grid_size - 4)
        self.draw_glow((*Theme.PRIMARY, 180), rect_r.center, 35, strength=8)
        
        # Draw Robot Body
        pygame.draw.rect(self.screen, Theme.PRIMARY, rect_r, border_radius=4)
        pygame.draw.rect(self.screen, (255, 255, 255), rect_r, width=2, border_radius=4)
        # Inner "Eye"
        pygame.draw.circle(self.screen, (255, 255, 255), rect_r.center, 4)

        # Draw UI
        for panel in self.panels:
            panel.draw(self.screen)
        
        # Top HUD Bar
        hud_font = Theme.get_font(Theme.FONT_SIZE_L)
        hud_surf = hud_font.render("WAREHOUSE.ALPHA_v1.0", True, Theme.PANEL_BORDER)
        self.screen.blit(hud_surf, (60, 25))
        
        # Speed Slider Label
        font = Theme.get_font(Theme.FONT_SIZE_S)
        label = font.render(f"SENSOR_SPEED: {self.speed}", True, Theme.TEXT_DIM)
        self.screen.blit(label, (920, 212))
        self.speed_slider.draw(self.screen)
        
        if self.chart_surf:
            self.screen.blit(self.chart_surf, (920, 580))

        # Full-Screen Scanlines overlay
        for i in range(0, 720, 8):
            s = pygame.Surface((1280, 2), pygame.SRCALPHA)
            s.fill(Theme.SCANLINE)
            self.screen.blit(s, (0, i))

        pygame.display.flip()
        self.frame_count += 1

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed if self.is_running else 60)
        pygame.quit()

if __name__ == "__main__":
    app = App()
    app.run()
