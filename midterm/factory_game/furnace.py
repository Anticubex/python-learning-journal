from station import Station
from item import Item


class Furnace(Station):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

    def step(self):
        for i in range(len(self.inputs)):
            raw = self.inputs[i].name
            if raw == "Iron Ore":
                del self.inputs[i]
                self.output_buffer.append(Item("Iron"))
                break
            elif raw == "Copper Ore":
                del self.inputs[i]
                self.output_buffer.append(Item("Copper"))
                break
