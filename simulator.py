from collections import defaultdict


class Simulator:
    __slots__ = "cars", "grid_x", "grid_y", "is_running", "completed_cars", "crashed_cars", "direction_degrees"

    def __init__(self):
        self.cars = {}  # name: [position, direction, instructions]
        self.completed_cars = {}  # position: name, direction
        self.crashed_cars = defaultdict(list)  # position: [(name, crashed_step), ...]

        self.grid_x = 100
        self.grid_y = 100

        self.is_running = False

        self.direction_degrees = {"N": 0, "E": 90, "S": 180, "W": 270}

    def add(self, name: str, position: tuple[int, int], direction: str, instructions: str) -> None:
        self.cars[name] = [position, self.direction_degrees[direction],
                           bytearray(instructions, encoding="utf-8")]

    def remove(self, car_name: str):
        if car_name in self.cars:
            del self.cars[car_name]

    def next_position(self, curr_pos: tuple[int, int], direction: int) -> tuple:
        x, y = curr_pos
        if direction == 0:
            y += 1
        elif direction == 90:
            x += 1
        elif direction == 180:
            y -= 1
        else:
            x -= 1

        if x < 0 or x >= self.grid_x or y < 0 or y >= self.grid_y:
            x, y = curr_pos

        return x, y

    def run(self):
        self.is_running = True
        self.completed_cars.clear(), self.crashed_cars.clear()
        step = 0
        while self.cars:
            hash_map = defaultdict(list)  # pos: [car_name, ...]
            cars_to_move = []
            for name in self.cars:
                car = self.cars[name]
                # check if the car's instructions are complete
                if len(car[2]) <= step:
                    self.completed_cars[car[0]] = name, car[1]
                    cars_to_move.append(name)
                    continue

                # calculate the next position of the car
                ins = car[2][step]
                if ins == 82:  # R
                    car[1] = (car[1] + 90) % 360
                elif ins == 76:  # L
                    car[1] = car[1] - 90 if car[1] else 270
                elif ins == 70:  # F
                    car[0] = self.next_position(car[0], car[1])
                else:  # unknown instruction
                    raise ValueError(f"Unknown instruction {ins} for car {name}")

                hash_map[car[0]].append(name)

            for car in cars_to_move:
                del self.cars[car]

            # check for crashed cars
            for pos, car_names in hash_map.items():
                if pos not in self.completed_cars and pos not in self.crashed_cars and len(car_names) == 1:
                    continue

                if pos in self.completed_cars:
                    self.crashed_cars[pos].append((self.completed_cars[pos][0], step + 1))
                    del self.completed_cars[pos]

                # step is 1-indexed according to the requirement
                for name in car_names:
                    self.crashed_cars[pos].append((name, step + 1))
                    del self.cars[name]

            step += 1
        self.is_running = False
