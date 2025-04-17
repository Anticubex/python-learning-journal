from station import Station
from collections import Counter
from item import Item


class Assembler(Station):
    def __init__(self, name, x, y, recipe):
        super().__init__(name, x, y)
        self.recipe = recipe

    def step(self):
        input_counts = Counter([item.name for item in self.inputs])
        can_assemble = all(
            input_counts.get(name, 0) >= count for name, count in self.recipe.items()
        )

        if can_assemble:
            for name, count in self.recipe.items():
                removed = 0
                for i in range(len(self.inputs) - 1, -1, -1):
                    if self.inputs[i].name == name:
                        del self.inputs[i]
                        removed += 1
                        if removed == count:
                            break
            self.output_buffer.append(Item("Product"))
