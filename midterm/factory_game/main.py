import pygame
from world import World
from extractor import Extractor
from furnace import Furnace
from conveyor import Conveyor
from assembler import Assembler
from core import Core

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

world = World()
core = Core("PlayerCore", 5, 3, world.inventory)


ironExtractor = Extractor("IronExtractor", 1, 1, "Iron Ore")
world.add_station(ironExtractor)
furnace1 = Furnace("Furnace1", 3, 1)
world.add_station(furnace1)
# world.add_station(Conveyor("", 2, 1, [ironExtractor], furnace1))

copperExtractor = Extractor("CopperExtractor", 1, 5, "Copper Ore")
world.add_station(copperExtractor)
furnace2 = Furnace("Furnace2", 3, 5)
world.add_station(furnace2)
# world.add_station(Conveyor("", 2, 5, [copperExtractor], furnace2))

assembler = Assembler("Assembler1", 3, 3, recipe={"Iron": 2, "Copper": 1})
# world.add_station(Conveyor("", 3, 2, [furnace1], assembler))
# world.add_station(Conveyor("", 3, 4, [furnace2], assembler))
world.add_station(assembler)

world.add_station(core)

# world.add_station(Conveyor("", 3, 4, [assembler], core))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        world.pan_camera(0, 5)
    if keys[pygame.K_s]:
        world.pan_camera(0, -5)
    if keys[pygame.K_a]:
        world.pan_camera(5, 0)
    if keys[pygame.K_d]:
        world.pan_camera(-5, 0)

    world.step()
    world.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
