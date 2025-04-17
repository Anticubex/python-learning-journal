from station import Station


class Core(Station):
    def __init__(self, name, x, y, inventory):
        super().__init__(name, x, y)
        self.inventory = inventory

    def insert_item(self, item):
        self.inventory[item.name] = self.inventory.get(item.name, 0) + 1
        return True
