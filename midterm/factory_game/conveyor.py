from station import Station


class Conveyor(Station):
    def __init__(self, name, x, y, input_stations=None, next_station=None):
        super().__init__(name, x, y)
        self.input_stations = input_stations
        self.inputs = []
        self.next_station = next_station

    def step(self):
        for station in self.input_stations:
            self.inputs.append(station.output_item())
        if self.inputs:
            item = self.inputs.pop(0)
            if self.next_station:
                accepted = self.next_station.insert_item(item)
                if not accepted:
                    self.inputs.insert(0, item)
