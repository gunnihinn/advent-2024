import argparse
import collections
import copy
import functools
import re


def parse(fh):
    digit = re.compile(r"(\-?\d+)")
    data = []
    for line in fh.readlines():
        m = digit.findall(line)
        data.append(
            (
                (int(m[0]), int(m[1])),
                (int(m[2]), int(m[3])),
            )
        )

    return data


def part1(data, seconds=100):
    max_x = max(p[0] for p, v in data)
    max_y = max(p[1] for p, v in data)

    quadrants = collections.defaultdict(int)
    middle_x = max_x // 2
    middle_y = max_y // 2

    for (x, y), (dx, dy) in data:
        nx = (x + seconds * dx) % (max_x + 1)
        ny = (y + seconds * dy) % (max_y + 1)
        if nx != middle_x and ny != middle_y:
            quadrants[(nx < middle_x, ny < middle_y)] += 1

    return functools.reduce(lambda a, b: a * b, quadrants.values(), 1)


def part2(data, start=0):
    max_x = max(p[0] for p, v in data)
    max_y = max(p[1] for p, v in data)

    def render(pos):
        lines = []
        for y in range(max_y + 1):
            line = []
            for x in range(max_x + 1):
                if (x, y) in pos:
                    line.append(str(pos[(x, y)]))
                else:
                    line.append(".")
            lines.append("".join(line))

        return "\n".join(lines)

    dirs = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    )

    def count_pts_with_neighbors(pos):
        return sum(any((xy[0] + dx, xy[1] + dy) in pos for dx, dy in dirs) for xy in pos)

    seconds = start
    while True:
        pos = {}
        for (x, y), (dx, dy) in data:
            nx = (x + seconds * dx) % (max_x + 1)
            ny = (y + seconds * dy) % (max_y + 1)
            pos[(nx, ny)] = pos.get((nx, ny), 0) + 1

        if seconds % 1000 == 0:
            print(f"seconds={seconds}")

        if count_pts_with_neighbors(pos) > len(data) * 0.5:
            print(render(pos))
            return seconds

        seconds += 1

    return seconds


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(copy.deepcopy(data)))
    print(part2(copy.deepcopy(data)))
