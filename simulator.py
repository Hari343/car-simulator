from collections import defaultdict


class Car:
    grid_x = 10
    grid_y = 10

    def __init__(self, name: str, pos: tuple[int, int, int], instructions: str):
        self.name = name
        self.initial_pos = pos
        self.instructions = instructions

        self.current_pos = self.initial_pos
        self.ip = 0

    @classmethod
    def update_grid_size(cls, x: int, y: int):
        cls.grid_x = x
        cls.grid_y = y

    def __iter__(self) -> 'Car':
        self.reset()
        return self

    def __next__(self) -> tuple[int, int, int]:
        if self.ip >= len(self.instructions):
            raise StopIteration
        self.current_pos = self._process_instruction(self.instructions[self.ip])
        self.ip += 1
        return self.current_pos

    def reset(self):
        self.ip = 0

    def _process_instruction(self, ins: str) -> tuple[int, int, int]:
        x, y, direction = self.current_pos
        _x, _y = x, y  # just in case
        if ins == "L":
            direction = direction - 90 if direction else 270
        elif ins == "R":
            direction = (direction + 90) % 360
        elif ins == "F":
            if direction == 0:
                y += 1
            elif direction == 90:
                x += 1
            elif direction == 180:
                y -= 1
            else:
                x -= 1

            if x < 0 or x >= self.grid_x or y < 0 or y >= self.grid_y:
                x, y = _x, _y

        return x, y, direction


class Simulator:
    __slots__ = "cars", "grid_x", "grid_y", "is_running", "completed_cars", "crashed_cars", "direction_degrees"

    def __init__(self):
        self.cars = []
        self.completed_cars = {}  # position: name, direction
        self.crashed_cars = {}  # position: [(name, crashed_step), ...]

        self.grid_x = 100
        self.grid_y = 100

        self.is_running = False

        self.direction_degrees = {"N": 0, "E": 90, "S": 180, "W": 270}

    def add(self, name: str, position: tuple[int, int], direction: str, instructions: str) -> None:
        self.cars.append(Car(name, (*position, self.direction_degrees[direction]), instructions))

    def run(self):
        self.is_running = True
        Car.update_grid_size(self.grid_x, self.grid_y)
        cars = {car.name: iter(car) for car in self.cars}
        completed_cars = {}  # pos: car_name
        crashed_cars = {}  # pos: [car_name, ...]
        while 1:
            if not cars:
                break

            locations, cars_to_move = defaultdict(list), []
            for car in cars.values():
                try:
                    *pos, _ = next(car)
                    locations[tuple(pos)].append(car)
                except StopIteration:
                    *pos, direction = car.current_pos
                    completed_cars[tuple(pos)] = car.name, direction
                    cars_to_move.append(car.name)

            for car_name in cars_to_move:
                del cars[car_name]

            for pos, _cars in locations.items():
                if pos in completed_cars:
                    if pos in crashed_cars:
                        crashed_cars[pos].append(completed_cars[pos])
                    else:
                        crashed_cars[pos] = [completed_cars[pos]]

                    del completed_cars[pos]

                if len(_cars) > 1:
                    if pos in crashed_cars:
                        crashed_cars[pos].extend((car.name, car.ip) for car in _cars)
                    else:
                        crashed_cars[pos] = [(car.name, car.ip) for car in _cars]

                    for car in _cars:
                        del cars[car.name]

        self.completed_cars, self.crashed_cars = completed_cars, crashed_cars

        self.is_running = False

