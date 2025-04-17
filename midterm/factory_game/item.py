import pygame


class Item:
    COLORS = {
        "Iron Ore": (180, 180, 180),
        "Copper Ore": (255, 100, 100),
        "Iron": (100, 100, 255),
        "Copper": (255, 165, 0),
        "Product": (0, 255, 0),
    }

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Item({self.name})"

    def draw_icon(self, surface, x, y):
        color = self.COLORS.get(self.name, (255, 255, 255))
        pygame.draw.circle(surface, color, (x, y), 6)
