import argparse
import collections
import copy

names = {
    (0, -1): "^",
    (1, 0): ">",
    (0, 1): "v",
    (-1, 0): "<",
}


def parse(fh):
    blob = fh.read().strip().split("\n\n")

    robot = None
    grid = collections.defaultdict(str)
    for y, line in enumerate(blob[0].split("\n")):
        for x, char in enumerate(line):
            if char == "@":
                robot = (x, y)
            elif char != ".":
                grid[(x, y)] = char

    dirs = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
    }
    moves = []
    for line in blob[1].split("\n"):
        for char in line:
            moves.append(dirs[char])

    return grid, robot, moves


def render(grid, robot):
    max_x = max(x for x, _ in grid) + 1
    max_y = max(y for _, y in grid) + 1

    lines = []
    for y in range(max_y):
        line = []
        for x in range(max_x):
            if (x, y) == robot:
                line.append("@")
            else:
                line.append(grid[(x, y)] or ".")
        lines.append("".join(line))

    return "\n".join(lines)


def gps(xy):
    return 100 * xy[1] + xy[0]


def moves(grid, robot, move):
    x, y = robot
    dx, dy = move
    steps = 1
    while True:
        pos = (x + steps * dx, y + steps * dy)
        char = grid[pos]
        if char == "#":
            return False, steps
        if not char:
            return True, steps
        steps += 1


def step(grid, robot, move):
    do, steps = moves(grid, robot, move)
    if not do:
        return grid, robot

    x, y = robot
    dx, dy = move
    assert (v := grid[(x + steps * dx, y + steps * dy)]) == "", f"expected empty string got {v}"
    for n in range(steps, 1, -1):
        grid[(x + n * dx, y + n * dy)] = grid[(x + (n - 1) * dx, y + (n - 1) * dy)]
    grid[(x, y)] = ""

    return grid, (x + dx, y + dy)


def part1(data):
    grid, robot, moves = data

    # print("initial")
    # print(render(grid, robot))
    for move in moves:
        grid, robot = step(grid, robot, move)
        # print(f"Move {names[move]}")
        # print(render(grid, robot))

    return sum(gps(xy) for xy, v in grid.items() if v == "O")


def embiggen(grid, robot):
    new = collections.defaultdict(str)
    for (x, y), char in grid.items():
        if char == "#":
            new[(2 * x, y)] = char
            new[(2 * x + 1, y)] = char
        elif char == "O":
            new[(2 * x, y)] = "["
            new[(2 * x + 1, y)] = "]"

    x, y = robot
    new[(2 * x, y)] = "@"

    return new, (2 * x, y)


def moves2(grid, robot, move):
    if move[1] == 0:
        return moves(grid, robot, move)
    x, y = robot
    dx, dy = move
    steps = 1
    while True:
        pos = (x + steps * dx, y + steps * dy)
        char = grid[pos]
        if char == "#":
            return False, steps
        if not char:
            return True, steps
        steps += 1


def step2(grid, robot, move):
    do, steps = moves2(grid, robot, move)
    if not do:
        return grid, robot

    x, y = robot
    dx, dy = move
    assert (v := grid[(x + steps * dx, y + steps * dy)]) == "", f"expected empty string got {v}"
    for n in range(steps, 1, -1):
        grid[(x + n * dx, y + n * dy)] = grid[(x + (n - 1) * dx, y + (n - 1) * dy)]
    grid[(x, y)] = ""

    return grid, (x + dx, y + dy)


def part2(data):
    grid, robot, moves = data
    grid, robot = embiggen(grid, robot)

    print("initial")
    print(render(grid, robot))
    for move in moves:
        grid, robot = step2(grid, robot, move)
        print(f"Move {names[move]}")
        print(render(grid, robot))
        break

    return sum(gps(xy) for xy, v in grid.items() if v == "O")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(copy.deepcopy(data)))
    print(part2(copy.deepcopy(data)))
