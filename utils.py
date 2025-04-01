from random import randint, choice


def load_input_from_file(filename: str) -> list:
    cars = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line_segments = line.split(",")
            car_name = line_segments[0].strip()
            pos = int(line_segments[1].strip()), int(line_segments[2].strip())
            direction = line_segments[3].strip().upper()
            instructions = line_segments[4].strip().upper()
            cars.append((car_name, pos, direction, instructions))

    return cars


def generate_inputs(output_file: str, num_cars: int = 100, grid_x: int = 1_000, grid_y: int = 1_000,
                    avg_instruction_size: int = 1_000, max_deviation: int = 500):
    """
        Inputs will be written to the output file in the following format (each line will consist of an input):
        name, pos_x, pos_y, direction, instructions

        This function can be used to generate large amounts of data to test the performance of the app
    """

    alphabet = "FRL"
    # starting pos cannot be duplicate
    hash_set = set()

    # generate starting pos
    for _ in range(num_cars):
        pos = randint(0, grid_x - 1), randint(0, grid_y)
        while pos in hash_set:
            pos = randint(0, grid_x - 1), randint(0, grid_y)
        hash_set.add(pos)

    initial_pos = list(hash_set)
    directions = [choice("NSEW") for _ in range(num_cars)]
    instructions = ["".join(choice(alphabet) for _ in range(randint(avg_instruction_size - max_deviation,
                                                                    avg_instruction_size + max_deviation)))
                    for _ in range(num_cars)]

    with open(output_file, "w") as f:
        for i, (pos, direction, instructions) in enumerate(zip(initial_pos, directions, instructions)):
            line = f"car_{i}, {str(pos)[1:-1]}, {direction}, {instructions}\n"
            f.write(line)
