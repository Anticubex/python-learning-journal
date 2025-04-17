import pygame
import sys
import random
from collections import deque
from typing import List, Dict, Optional, Tuple

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
GRID_SIZE = 64
BACKGROUND_COLOR = (50, 50, 50)
UI_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (80, 180, 250)
MATERIAL_COLORS = {
    "iron": (200, 200, 200),
    "copper": (184, 115, 51),
    "coal": (40, 40, 40),
    "plastic": (255, 255, 100),
    "circuit": (0, 180, 0),
    "product": (255, 165, 0),
}

# Game window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Factory Simulation Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
large_font = pygame.font.SysFont("Arial", 24)


# Data Structures
class Queue:
    """Implementation of Queue data structure for managing materials waiting to be processed"""

    def __init__(self, max_size: int = 10):
        self.items = deque()
        self.max_size = max_size

    def enqueue(self, item) -> bool:
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def is_full(self) -> bool:
        return len(self.items) >= self.max_size

    def size(self) -> int:
        return len(self.items)

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None


class Stack:
    """Implementation of Stack data structure for temporary storage"""

    def __init__(self, max_size: int = 10):
        self.items = []
        self.max_size = max_size

    def push(self, item) -> bool:
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def is_full(self) -> bool:
        return len(self.items) >= self.max_size

    def size(self) -> int:
        return len(self.items)


class TreeNode:
    """Node for the binary tree structure representing production stations"""

    def __init__(self, station_type: str, x: int, y: int):
        self.station_type = station_type
        self.x = x
        self.y = y
        self.left = None
        self.right = None
        self.parent = None
        self.station_instance = None


class BinaryTree:
    """Binary tree representing production stations and their relationships"""

    def __init__(self):
        self.root = None

    def insert(
        self, station_type: str, x: int, y: int, parent=None, is_left=True
    ) -> TreeNode:
        new_node = TreeNode(station_type, x, y)

        if parent is None:
            if self.root is None:
                self.root = new_node
        else:
            new_node.parent = parent
            if is_left:
                parent.left = new_node
            else:
                parent.right = new_node

        return new_node

    def find_node_at_position(self, x: int, y: int) -> Optional[TreeNode]:
        """Find a node at the given grid position"""
        return self._find_node_at_position_helper(self.root, x, y)

    def _find_node_at_position_helper(
        self, node: TreeNode, x: int, y: int
    ) -> Optional[TreeNode]:
        if node is None:
            return None

        if node.x == x and node.y == y:
            return node

        left_result = self._find_node_at_position_helper(node.left, x, y)
        if left_result:
            return left_result

        return self._find_node_at_position_helper(node.right, x, y)

    def traverse_in_order(self):
        """In-order traversal of the tree"""
        result = []
        self._traverse_in_order_helper(self.root, result)
        return result

    def _traverse_in_order_helper(self, node: TreeNode, result: List):
        if node:
            self._traverse_in_order_helper(node.left, result)
            result.append(node)
            self._traverse_in_order_helper(node.right, result)


# Game Classes
class Material:
    """Represents materials that flow through the factory"""

    def __init__(self, material_type: str):
        self.material_type = material_type
        self.processing_time = 0

    def draw(self, surface, x: int, y: int, size: int = 20):
        color = MATERIAL_COLORS.get(self.material_type, (255, 255, 255))
        pygame.draw.rect(surface, color, (x, y, size, size))
        pygame.draw.rect(surface, (20, 20, 20), (x, y, size, size), 1)


class Station:
    """Base class for production stations"""

    def __init__(self, station_type: str, x: int, y: int):
        self.station_type = station_type
        self.x = x
        self.y = y
        self.input_queue = Queue(5)
        self.output_queue = Queue(5)
        self.storage_stack = Stack(3)
        self.processing = None
        self.processing_time = 0
        self.processing_total = 60  # frames for processing
        self.active = True

    def process_item(self):
        """Process an item from input to output"""
        if self.processing is None and not self.input_queue.is_empty():
            self.processing = self.input_queue.dequeue()
            self.processing_time = 0

        if self.processing:
            if self.active:
                self.processing_time += 1

            if self.processing_time >= self.processing_total:
                # Processing complete
                output_material = self.transform_material(self.processing)
                if not self.output_queue.is_full():
                    self.output_queue.enqueue(output_material)
                    self.processing = None

    def transform_material(self, material: Material) -> Material:
        """Transform input material to output material"""
        # Default behavior: pass through
        return material

    def draw(self, surface):
        """Draw the station on the surface"""
        # Draw station background
        station_color = self._get_station_color()
        pygame.draw.rect(
            surface,
            station_color,
            (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(
            surface,
            (20, 20, 20),
            (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            2,
        )

        # Draw station label
        label = font.render(self.station_type, True, TEXT_COLOR)
        surface.blit(label, (self.x * GRID_SIZE + 5, self.y * GRID_SIZE + 5))

        # Draw input queue
        if not self.input_queue.is_empty():
            for i, item in enumerate(self.input_queue.items):
                item.draw(
                    surface,
                    self.x * GRID_SIZE + 10,
                    self.y * GRID_SIZE + GRID_SIZE - 25 - i * 5,
                    15,
                )

        # Draw output queue
        if not self.output_queue.is_empty():
            for i, item in enumerate(self.output_queue.items):
                item.draw(
                    surface,
                    self.x * GRID_SIZE + GRID_SIZE - 25,
                    self.y * GRID_SIZE + 10 + i * 5,
                    15,
                )

        # Draw processing item
        if self.processing:
            progress = self.processing_time / self.processing_total
            pygame.draw.rect(
                surface,
                (100, 200, 100),
                (
                    self.x * GRID_SIZE + 10,
                    self.y * GRID_SIZE + GRID_SIZE - 8,
                    (GRID_SIZE - 20) * progress,
                    6,
                ),
            )
            self.processing.draw(
                surface,
                self.x * GRID_SIZE + GRID_SIZE // 2 - 10,
                self.y * GRID_SIZE + GRID_SIZE // 2 - 10,
            )

    def _get_station_color(self):
        """Get color based on station type"""
        colors = {
            "extractor": (100, 100, 150),
            "furnace": (200, 100, 50),
            "assembler": (70, 130, 180),
            "packager": (150, 150, 80),
            "output": (50, 180, 100),
        }
        return colors.get(self.station_type, (120, 120, 120))

    def toggle_active(self):
        """Toggle station active/inactive state"""
        self.active = not self.active

    def is_at_position(self, pos_x: int, pos_y: int) -> bool:
        """Check if station is at grid position"""
        return self.x == pos_x and self.y == pos_y


class Extractor(Station):
    """Extracts raw materials"""

    def __init__(self, x: int, y: int, material_type: str):
        super().__init__("extractor", x, y)
        self.material_type = material_type
        self.extraction_timer = 0
        self.extraction_rate = 120  # frames between extractions

    def update(self):
        """Update extractor to periodically produce materials"""
        if self.active:
            self.extraction_timer += 1
            if self.extraction_timer >= self.extraction_rate:
                self.extraction_timer = 0
                if not self.output_queue.is_full():
                    self.output_queue.enqueue(Material(self.material_type))

        self.process_item()

    def draw(self, surface):
        super().draw(surface)
        # Draw material type
        label = font.render(f"Type: {self.material_type}", True, TEXT_COLOR)
        surface.blit(label, (self.x * GRID_SIZE + 5, self.y * GRID_SIZE + 25))


class Furnace(Station):
    """Processes raw materials into refined materials"""

    def __init__(self, x: int, y: int):
        super().__init__("furnace", x, y)
        self.processing_total = 90  # slower processing

    def transform_material(self, material: Material) -> Material:
        """Transform materials in furnace"""
        if material.material_type == "iron":
            return Material("steel")
        elif material.material_type == "copper":
            return Material("wire")
        else:
            return material


class Assembler(Station):
    """Combines materials to create components"""

    def __init__(self, x: int, y: int):
        super().__init__("assembler", x, y)
        self.processing_total = 120
        self.required_materials = {"iron": 0, "copper": 0}

    def process_item(self):
        """Modified process to require multiple input types"""
        if self.processing is None:
            # Try to get needed materials
            if not self.input_queue.is_empty():
                material = self.input_queue.peek()
                if material.material_type in self.required_materials:
                    self.required_materials[material.material_type] += 1
                    self.storage_stack.push(self.input_queue.dequeue())

                # Check if we have enough materials to start processing
                if (
                    self.required_materials.get("iron", 0) >= 1
                    and self.required_materials.get("copper", 0) >= 1
                ):
                    # Use up materials
                    self.required_materials["iron"] -= 1
                    self.required_materials["copper"] -= 1
                    self.processing = Material("component")
                    self.processing_time = 0

        # Continue with normal processing if we have an item being processed
        if self.processing:
            if self.active:
                self.processing_time += 1

            if self.processing_time >= self.processing_total:
                # Processing complete
                output_material = self.transform_material(self.processing)
                if not self.output_queue.is_full():
                    self.output_queue.enqueue(output_material)
                    self.processing = None

    def transform_material(self, material: Material) -> Material:
        """Combine materials into components"""
        return Material("circuit")


class Packager(Station):
    """Packages components into final products"""

    def __init__(self, x: int, y: int):
        super().__init__("packager", x, y)
        self.processing_total = 80

    def transform_material(self, material: Material) -> Material:
        """Package components into products"""
        if material.material_type == "circuit":
            return Material("product")
        else:
            return material


class OutputStation(Station):
    """Final output for completed products"""

    def __init__(self, x: int, y: int):
        super().__init__("output", x, y)
        self.products_completed = 0

    def process_item(self):
        """Count completed products"""
        if not self.input_queue.is_empty():
            material = self.input_queue.dequeue()
            if material.material_type == "product":
                self.products_completed += 1

    def draw(self, surface):
        super().draw(surface)
        # Draw product count
        label = font.render(f"Products: {self.products_completed}", True, TEXT_COLOR)
        surface.blit(label, (self.x * GRID_SIZE + 5, self.y * GRID_SIZE + 30))


class Conveyor:
    """Connects stations and moves materials between them"""

    def __init__(self, from_station: Station, to_station: Station):
        self.from_station = from_station
        self.to_station = to_station
        self.materials = []
        self.speed = 2  # pixels per frame
        self.path = self._calculate_path()

    def _calculate_path(self) -> List[Tuple[int, int]]:
        """Calculate path from source to destination"""
        start_x = self.from_station.x * GRID_SIZE + GRID_SIZE // 2
        start_y = self.from_station.y * GRID_SIZE + GRID_SIZE // 2
        end_x = self.to_station.x * GRID_SIZE + GRID_SIZE // 2
        end_y = self.to_station.y * GRID_SIZE + GRID_SIZE // 2

        # Simple direct path for now
        return [(start_x, start_y), (end_x, end_y)]

    def update(self):
        """Move materials along conveyor and transfer between stations"""
        # Try to get a material from source station
        if (
            not self.from_station.output_queue.is_empty()
            and not self.to_station.input_queue.is_full()
            and len(self.materials) < 3
        ):
            material = self.from_station.output_queue.dequeue()
            if material:
                # Add to conveyor with starting position
                start_x, start_y = self.path[0]
                self.materials.append(
                    {"material": material, "x": start_x, "y": start_y, "progress": 0.0}
                )

        # Move materials along conveyor
        materials_to_remove = []
        for item in self.materials:
            item["progress"] += 0.01  # Increment progress (0 to 1)

            if item["progress"] >= 1.0:
                # Material reached destination
                if not self.to_station.input_queue.is_full():
                    self.to_station.input_queue.enqueue(item["material"])
                    materials_to_remove.append(item)
            else:
                # Interpolate position based on progress
                start_x, start_y = self.path[0]
                end_x, end_y = self.path[1]
                item["x"] = start_x + (end_x - start_x) * item["progress"]
                item["y"] = start_y + (end_y - start_y) * item["progress"]

        # Remove delivered materials
        for item in materials_to_remove:
            self.materials.remove(item)

    def draw(self, surface):
        """Draw conveyor and materials on it"""
        # Draw conveyor line
        start_x, start_y = self.path[0]
        end_x, end_y = self.path[1]
        pygame.draw.line(
            surface, (150, 150, 150), (start_x, start_y), (end_x, end_y), 5
        )

        # Draw direction indicator (arrow)
        mid_x = start_x + (end_x - start_x) * 0.5
        mid_y = start_y + (end_y - start_y) * 0.5
        angle = pygame.math.Vector2(end_x - start_x, end_y - start_y).normalize()
        normal = pygame.math.Vector2(-angle.y, angle.x) * 5

        # Arrow points
        p1 = (mid_x + angle.x * 8, mid_y + angle.y * 8)
        p2 = (mid_x - angle.x * 8 + normal.x, mid_y - angle.y * 8 + normal.y)
        p3 = (mid_x - angle.x * 8 - normal.x, mid_y - angle.y * 8 - normal.y)

        pygame.draw.polygon(surface, (200, 200, 200), [p1, p2, p3])

        # Draw materials on conveyor
        for item in self.materials:
            item["material"].draw(surface, int(item["x"]) - 10, int(item["y"]) - 10)


class Factory:
    """Main factory class that manages the simulation"""

    def __init__(self):
        self.stations = []
        self.conveyors = []
        self.station_tree = BinaryTree()
        self.selected_station = None
        self.money = 1000
        self.production_cost = 2  # cost per product
        self.product_value = 50  # value per product

        # UI elements
        self.ui_panel_rect = pygame.Rect(WIDTH - 250, 0, 250, HEIGHT)
        self.build_mode = False
        self.build_type = None

        # Initialize the factory layout
        self._initialize_factory()

    def _initialize_factory(self):
        """Create initial factory layout"""
        # Create extractors
        iron_extractor = Extractor(2, 2, "iron")
        copper_extractor = Extractor(2, 6, "copper")

        # Create processing stations
        furnace = Furnace(6, 2)
        assembler = Assembler(10, 4)
        packager = Packager(14, 4)
        output = OutputStation(18, 4)

        # Add stations to list
        self.stations.extend(
            [iron_extractor, copper_extractor, furnace, assembler, packager, output]
        )

        # Create conveyors
        self.conveyors.extend(
            [
                Conveyor(iron_extractor, furnace),
                Conveyor(furnace, assembler),
                Conveyor(copper_extractor, assembler),
                Conveyor(assembler, packager),
                Conveyor(packager, output),
            ]
        )

        # Build station tree
        root = self.station_tree.insert("assembler", 10, 4)
        root.station_instance = assembler

        furnace_node = self.station_tree.insert("furnace", 6, 2, root, True)
        furnace_node.station_instance = furnace

        iron_node = self.station_tree.insert("extractor", 2, 2, furnace_node, True)
        iron_node.station_instance = iron_extractor

        copper_node = self.station_tree.insert("extractor", 2, 6, root, False)
        copper_node.station_instance = copper_extractor

        packager_node = self.station_tree.insert("packager", 14, 4, root, False)
        packager_node.station_instance = packager

        output_node = self.station_tree.insert("output", 18, 4, packager_node, False)
        output_node.station_instance = output

    def update(self):
        """Update the factory simulation"""
        # Update all stations
        for station in self.stations:
            if isinstance(station, OutputStation):
                station.process_item()  # Special handling for output stations
            elif isinstance(station, Extractor):
                station.update()
            else:
                station.process_item()

        # Update all conveyors
        for conveyor in self.conveyors:
            conveyor.update()

        # Update factory finances
        for station in self.stations:
            if isinstance(station, OutputStation):
                if station.products_completed > 0:
                    self.money += station.products_completed * self.product_value
                    station.products_completed = 0

            if station.active:
                # Operating costs
                if random.random() < 0.01:  # Small chance each frame
                    self.money -= self.production_cost

    def draw(self, surface):
        """Draw the factory and all components"""
        # Draw background grid
        for x in range(0, WIDTH - 250, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                pygame.draw.rect(surface, (60, 60, 60), (x, y, GRID_SIZE, GRID_SIZE), 1)

        # Draw conveyors first (below stations)
        for conveyor in self.conveyors:
            conveyor.draw(surface)

        # Draw stations
        for station in self.stations:
            station.draw(surface)

            # Highlight selected station
            if station == self.selected_station:
                pygame.draw.rect(
                    surface,
                    ACCENT_COLOR,
                    (
                        station.x * GRID_SIZE,
                        station.y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                    3,
                )

        # Draw UI panel
        self._draw_ui(surface)

    def _draw_ui(self, surface):
        """Draw UI panel with factory info and controls"""
        # Draw UI background
        pygame.draw.rect(surface, UI_COLOR, self.ui_panel_rect)
        pygame.draw.line(
            surface, ACCENT_COLOR, (WIDTH - 250, 0), (WIDTH - 250, HEIGHT), 2
        )

        # Draw factory title
        title = large_font.render("Factory Controls", True, TEXT_COLOR)
        surface.blit(title, (WIDTH - 230, 20))

        # Draw money
        money_text = font.render(f"Money: ${self.money}", True, TEXT_COLOR)
        surface.blit(money_text, (WIDTH - 230, 60))

        # Draw selected station info
        y_offset = 100
        if self.selected_station:
            station_title = font.render(
                f"Selected: {self.selected_station.station_type}", True, TEXT_COLOR
            )
            surface.blit(station_title, (WIDTH - 230, y_offset))
            y_offset += 25

            status = "Active" if self.selected_station.active else "Inactive"
            status_color = (
                (100, 200, 100) if self.selected_station.active else (200, 100, 100)
            )
            status_text = font.render(f"Status: {status}", True, status_color)
            surface.blit(status_text, (WIDTH - 230, y_offset))
            y_offset += 25

            # Draw toggle button
            toggle_rect = pygame.Rect(WIDTH - 230, y_offset, 100, 30)
            pygame.draw.rect(surface, ACCENT_COLOR, toggle_rect)
            toggle_text = font.render("Toggle Power", True, TEXT_COLOR)
            surface.blit(toggle_text, (WIDTH - 225, y_offset + 7))
            y_offset += 40

            # Queue information
            input_text = font.render(
                f"Input Queue: {self.selected_station.input_queue.size()}/{self.selected_station.input_queue.max_size}",
                True,
                TEXT_COLOR,
            )
            surface.blit(input_text, (WIDTH - 230, y_offset))
            y_offset += 25

            output_text = font.render(
                f"Output Queue: {self.selected_station.output_queue.size()}/{self.selected_station.output_queue.max_size}",
                True,
                TEXT_COLOR,
            )
            surface.blit(output_text, (WIDTH - 230, y_offset))
            y_offset += 25

            stack_text = font.render(
                f"Storage Stack: {self.selected_station.storage_stack.size()}/{self.selected_station.storage_stack.max_size}",
                True,
                TEXT_COLOR,
            )
            surface.blit(stack_text, (WIDTH - 230, y_offset))
            y_offset += 40

        # Factory stats
        y_offset = max(y_offset, 300)
        stats_title = font.render("Factory Statistics", True, TEXT_COLOR)
        surface.blit(stats_title, (WIDTH - 230, y_offset))
        y_offset += 25

        # Count stations by type
        station_counts = {}
        for station in self.stations:
            station_type = station.station_type
            station_counts[station_type] = station_counts.get(station_type, 0) + 1

        for i, (station_type, count) in enumerate(station_counts.items()):
            count_text = font.render(
                f"{station_type.capitalize()}: {count}", True, TEXT_COLOR
            )
            surface.blit(count_text, (WIDTH - 230, y_offset + i * 20))

        y_offset += len(station_counts) * 20 + 20

        # Production metrics
        total_output = sum(
            s.products_completed for s in self.stations if isinstance(s, OutputStation)
        )
        output_text = font.render(f"Total Products: {total_output}", True, TEXT_COLOR)
        surface.blit(output_text, (WIDTH - 230, y_offset))
        y_offset += 25

        # Help text
        y_offset = HEIGHT - 100
        help_text = font.render("Click on stations to select", True, TEXT_COLOR)
        surface.blit(help_text, (WIDTH - 230, y_offset))
        help_text2 = font.render("Toggle power to control", True, TEXT_COLOR)
        surface.blit(help_text2, (WIDTH - 230, y_offset + 20))
        help_text3 = font.render("production", True, TEXT_COLOR)
        surface.blit(help_text3, (WIDTH - 230, y_offset + 40))

    def handle_click(self, pos):
        """Handle mouse click on factory grid"""
        x, y = pos

        # Check if click is in UI panel
        if self.ui_panel_rect.collidepoint(pos):
            self._handle_ui_click(pos)
            return

        # Convert to grid coordinates
        grid_x = x // GRID_SIZE
        grid_y = y // GRID_SIZE

        # Check if clicked on a station
        for station in self.stations:
            if station.is_at_position(grid_x, grid_y):
                self.selected_station = station
                return

        # If no station clicked, deselect
        self.selected_station = None

    def _handle_ui_click(self, pos):
        """Handle clicks on UI elements"""
        x, y = pos

        if self.selected_station:
            # Check if toggle button clicked
            toggle_rect = pygame.Rect(WIDTH - 230, 150, 100, 30)
            if toggle_rect.collidepoint(pos):
                self.selected_station.toggle_active()


def main():
    """Main game function"""
    factory = Factory()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    factory.handle_click(event.pos)

        # Update factory
        factory.update()

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        factory.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
