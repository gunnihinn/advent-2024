import argparse
import collections
import itertools


def parse(fh):
    guard = None
    grid = collections.defaultdict(str)

    for j, line in enumerate(fh.readlines()):
        for i, char in enumerate(line.strip()):
            if char != "#" and char != ".":
                guard = (i, j, char)
                grid[(i, j)] = "."
            else:
                grid[(i, j)] = char

    return guard, grid


def render(guard, grid):
    m_x = max(v[0] for v in grid)
    m_y = max(v[1] for v in grid)

    for y in range(m_y + 1):
        line = []
        for x in range(m_x + 1):
            if guard[0] == x and guard[1] == y:
                line.append(guard[2])
            else:
                line.append(grid[(x, y)])
        print("".join(line))


def part1(data):
    (x, y, d), grid = data

    dirs = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^",
    }
    visited = set()
    while grid[(x, y)]:
        visited.add((x, y))
        if d == "^":
            dx, dy = 0, -1
        elif d == ">":
            dx, dy = 1, 0
        elif d == "v":
            dx, dy = 0, 1
        elif d == "<":
            dx, dy = -1, 0

        if grid[(x + dx, y + dy)] == "#":
            d = dirs[d]
            continue

        x, y = x + dx, y + dy

    return len(visited)


def part2(data):
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
