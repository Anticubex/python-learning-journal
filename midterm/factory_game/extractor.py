from station import Station
from item import Item


class Extractor(Station):
    def __init__(self, name, x, y, resource):
        super().__init__(name, x, y)
        self.resource = resource
        self.timer = 0

    def step(self):
        self.timer += 1
        if self.timer >= 60:
            self.output_buffer.append(Item(self.resource))
            self.timer = 0
