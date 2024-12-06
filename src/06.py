import argparse
import collections


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
    m_x = max(v[0] for v in grid) + 1
    m_y = max(v[1] for v in grid) + 1

    for y in range(m_y):
        line = []
        for x in range(m_x):
            if guard[0] == x and guard[1] == y:
                line.append(guard[2])
            else:
                line.append(grid[(x, y)])
        print("".join(line))


def escapes_after(guard, grid):
    "Return number of steps until guard escapes or 0 if they loop"
    x, y, d = guard

    dirs = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^",
    }
    visited = set()
    while grid[(x, y)]:
        if (x, y, d) in visited:
            return 0

        visited.add((x, y, d))
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

    return len(set((x, y) for x, y, d in visited))


def part1(data):
    guard, grid = data

    return escapes_after(guard, grid)


def part2(data):
    guard, grid = data

    count = 0
    m_x = max(v[0] for v in grid) + 1
    m_y = max(v[1] for v in grid) + 1
    n = 0
    for x in range(m_x):
        for y in range(m_y):
            if guard[0] == x and guard[1] == y:
                continue
            orig = grid[(x, y)]
            grid[(x, y)] = "#"
            if not escapes_after(guard, grid):
                count += 1
            grid[(x, y)] = orig

            n += 1

    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
