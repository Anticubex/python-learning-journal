import pygame


class World:
    def __init__(self):
        self.stations = []
        self.inventory = {}
        self.camera_offset = [0, 0]

    def add_station(self, station):
        self.stations.append(station)

    def step(self):
        for station in self.stations:
            station.step()

    def draw(self, surface):
        surface.fill((50, 50, 50))
        for station in self.stations:
            station.draw(surface, self.camera_offset)

    def pan_camera(self, dx, dy):
        self.camera_offset[0] += dx
        self.camera_offset[1] += dy
