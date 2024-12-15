import argparse
import collections


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
    moves = list(map(lambda c: dirs[c], blob[1]))

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


def part1(data):
    grid, robot, moves = data

    print(render(grid, robot))
    print(moves)

    total = 0
    return total


def part2(data):
    total = 0
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
