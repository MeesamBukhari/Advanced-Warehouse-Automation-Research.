import pygame
import json
import os
from .theme import Theme
from .ui_system import Panel, Button, Slider
from core.warehouse import Warehouse, Position, CellType
from core.algorithms import bfs, ucs, a_star

class ControlPanel(Panel):
    def __init__(self, rect, on_run, on_reset, on_algo_change):
        super().__init__(rect, "Control Panel")
        self.algorithms = ["A*", "BFS", "UCS"]
        self.current_algo_idx = 0
        
        self.algo_btn = Button(pygame.Rect(rect.x + 20, rect.y + 70, 160, 40), "Algo: A*", self.toggle_algo, color=Theme.SECONDARY)
        self.run_btn = Button(pygame.Rect(rect.x + 20, rect.y + 120, 160, 40), "RUN", on_run, color=Theme.PRIMARY)
        self.reset_btn = Button(pygame.Rect(rect.x + 20, rect.y + 170, 160, 40), "RESET", on_reset, color=Theme.DANGER)
        
        self.on_algo_change = on_algo_change
        self.components = [self.algo_btn, self.run_btn, self.reset_btn]

    def toggle_algo(self):
        self.current_algo_idx = (self.current_algo_idx + 1) % len(self.algorithms)
        algo = self.algorithms[self.current_algo_idx]
        self.algo_btn.text = f"Algo: {algo}"
        self.on_algo_change(algo)

    def handle_event(self, event):
        super().handle_event(event)
        for comp in self.components:
            comp.handle_event(event)

    def draw(self, screen):
        super().draw(screen)
        for comp in self.components:
            comp.draw(screen)

class StatsPanel(Panel):
    def __init__(self, rect):
        super().__init__(rect, "Stats Dashboard")
        self.stats = {
            "Algorithm": "A*",
            "Steps": 0,
            "Explored": 0,
            "Time": "0ms",
            "Items": "0/3"
        }

    def update_stats(self, **kwargs):
        self.stats.update(kwargs)

    def draw(self, screen):
        super().draw(screen)
        font = Theme.get_font(Theme.FONT_SIZE_S, bold=False)
        for i, (key, val) in enumerate(self.stats.items()):
            # Label
            label_surf = font.render(f"{key}:", True, Theme.TEXT_DIM)
            screen.blit(label_surf, (self.rect.x + 25, self.rect.y + 70 + i * 24))
            # Value
            val_surf = font.render(str(val), True, Theme.TEXT_MAIN)
            screen.blit(val_surf, (self.rect.x + 130, self.rect.y + 70 + i * 24))

class ScenarioViewer(Panel):
    def __init__(self, rect, on_scenario_load):
        super().__init__(rect, "Scenario Viewer")
        self.on_scenario_load = on_scenario_load
        self.scenarios = [f for f in os.listdir('scenarios') if f.endswith('.json')]
        self.current_idx = 0
        
        self.prev_btn = Button(pygame.Rect(rect.x + 20, rect.y + 70, 90, 35), "< Prev", self.prev_scenario, color=Theme.SURFACE)
        self.next_btn = Button(pygame.Rect(rect.x + 120, rect.y + 70, 90, 35), "Next >", self.next_scenario, color=Theme.SURFACE)
        self.components = [self.prev_btn, self.next_btn]

    def prev_scenario(self):
        if not self.scenarios: return
        self.current_idx = (self.current_idx - 1) % len(self.scenarios)
        self.load_current()

    def next_scenario(self):
        if not self.scenarios: return
        self.current_idx = (self.current_idx + 1) % len(self.scenarios)
        self.load_current()

    def load_current(self):
        path = os.path.join('scenarios', self.scenarios[self.current_idx])
        with open(path, 'r') as f:
            data = json.load(f)
            self.on_scenario_load(data)

    def handle_event(self, event):
        super().handle_event(event)
        for comp in self.components:
            comp.handle_event(event)

    def draw(self, screen):
        super().draw(screen)
        font = Theme.get_font(Theme.FONT_SIZE_S)
        if self.scenarios:
            name = self.scenarios[self.current_idx].replace('.json', '').title()
            surf = font.render(f"Current: {name}", True, Theme.SECONDARY)
            screen.blit(surf, (self.rect.x + 25, self.rect.y + 120))
        for comp in self.components:
            comp.draw(screen)
