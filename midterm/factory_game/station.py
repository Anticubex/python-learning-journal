from collections import deque
import pygame
from item import Item


class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.inputs = []
        self.output_buffer = deque()
        self.x = x
        self.y = y
        self.color = (180, 180, 180)

    def insert_item(self, item):
        self.inputs.append(item)
        return True

    def output_item(self):
        if self.output_buffer:
            return self.output_buffer.popleft()
        return None

    def step(self):
        pass

    def draw(self, surface, camera_offset):
        rect = pygame.Rect(
            self.x * 40 - camera_offset[0], self.y * 40 - camera_offset[1], 40, 40
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)

        font = pygame.font.SysFont(None, 16)
        name_surface = font.render(self.name, True, (255, 255, 255))
        surface.blit(name_surface, (rect.x + 2, rect.y + 2))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_x, mouse_y):
            tooltip_lines = (
                ["In:"]
                + [item.name for item in self.inputs]
                + ["Out:"]
                + [item.name for item in self.output_buffer]
            )
            tooltip_surfaces = [
                font.render(line, True, (255, 255, 255)) for line in tooltip_lines
            ]
            max_width = max(surf.get_width() for surf in tooltip_surfaces)
            tooltip_rect = pygame.Rect(
                mouse_x + 10,
                mouse_y + 10,
                max_width + 8,
                8 + 16 * len(tooltip_surfaces),
            )
            pygame.draw.rect(surface, (0, 0, 0), tooltip_rect)
            pygame.draw.rect(surface, (255, 255, 255), tooltip_rect, 1)
            for i, surf in enumerate(tooltip_surfaces):
                surface.blit(surf, (tooltip_rect.x + 4, tooltip_rect.y + 4 + i * 16))

            for i, item in enumerate(self.inputs):
                item.draw_icon(surface, rect.x + 10 + i * 14, rect.y + 30)
            for i, item in enumerate(self.output_buffer):
                item.draw_icon(surface, rect.x + 10 + i * 14, rect.y + 40)
