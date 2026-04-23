import pygame
from .theme import Theme

class UIComponent:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

    def draw(self, surface: pygame.Surface):
        pass

class Panel(UIComponent):
    def __init__(self, rect: pygame.Rect, title: str = ""):
        super().__init__(rect)
        self.title = title
        self.surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    def draw(self, screen: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        # Deep translucent surface
        pygame.draw.rect(self.surface, Theme.SURFACE, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        # Neon Border
        pygame.draw.rect(self.surface, Theme.PANEL_BORDER, (0, 0, self.rect.width, self.rect.height), width=2, border_radius=10)
        
        # Scanlines inside panel
        for i in range(0, self.rect.height, 4):
            pygame.draw.line(self.surface, (0, 255, 255, 10), (0, i), (self.rect.width, i))

        if self.title:
            font = Theme.get_font(Theme.FONT_SIZE_M)
            # Title Glow
            title_surf = font.render(self.title, True, Theme.TEXT_MAIN)
            self.surface.blit(title_surf, (20, 20))
            # Underline decorator
            pygame.draw.line(self.surface, Theme.PANEL_BORDER, (20, 55), (150, 55), width=2)
            
        screen.blit(self.surface, (self.rect.x, self.rect.y))

class Button(UIComponent):
    def __init__(self, rect: pygame.Rect, text: str, callback=None, color=None):
        super().__init__(rect)
        self.text = text
        self.callback = callback
        self.base_color = color if color else Theme.PRIMARY

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()

    def draw(self, screen: pygame.Surface):
        color = self.base_color
        if self.is_hovered:
            color = [min(255, c + 50) for c in color]
        
        # Transparent base blit
        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, (*color[:3], 60), (0, 0, self.rect.width, self.rect.height), border_radius=5)
        screen.blit(temp_surface, (self.rect.x, self.rect.y))
        
        # Opaque Border
        pygame.draw.rect(screen, color[:3], self.rect, width=2, border_radius=5)
        
        # Corner decorators
        l, t, w, h = self.rect
        pygame.draw.line(screen, color, (l, t), (l+10, t), 4) # TL
        pygame.draw.line(screen, color, (l, t), (l, t+10), 4)
        pygame.draw.line(screen, color, (l+w-10, t+h), (l+w, t+h), 4) # BR
        pygame.draw.line(screen, color, (l+w, t+h-10), (l+w, t+h), 4)

        font = Theme.get_font(Theme.FONT_SIZE_S)
        text_surf = font.render(self.text, True, color if self.is_hovered else Theme.TEXT_MAIN)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class Slider(UIComponent):
    def __init__(self, rect: pygame.Rect, min_val: float, max_val: float, initial_val: float):
        super().__init__(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.is_dragging = False
        self.handle_radius = 8
        self.update_handle()

    def update_handle(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_center = (self.rect.x + ratio * self.rect.width, self.rect.centery)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.Vector2(event.pos)
            if mouse_pos.distance_to(self.handle_center) < self.handle_radius + 10:
                self.is_dragging = True
            elif self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.update_val_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        if self.is_dragging and event.type == pygame.MOUSEMOTION:
            self.update_val_from_mouse(event.pos[0])

    def update_val_from_mouse(self, x):
        rel_x = max(0, min(x - self.rect.x, self.rect.width))
        self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
        self.update_handle()

    def draw(self, screen: pygame.Surface):
        # Draw track
        pygame.draw.rect(screen, (30, 30, 60), self.rect, border_radius=2)
        # Draw active part
        active_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_center[0] - self.rect.x, self.rect.height)
        pygame.draw.rect(screen, Theme.PRIMARY, active_rect, border_radius=2)
        # Handle
        color = (255, 255, 255) if self.is_hovered or self.is_dragging else Theme.PRIMARY
        pygame.draw.circle(screen, color, (int(self.handle_center[0]), int(self.handle_center[1])), self.handle_radius)
