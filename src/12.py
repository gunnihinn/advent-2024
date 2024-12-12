import argparse
import collections
import itertools

S = (0, 1)
N = (0, -1)
W = (-1, 0)
E = (1, 0)


def parse(fh):
    grid = collections.defaultdict(str)
    for y, line in enumerate(fh.readlines()):
        for x, char in enumerate(line.strip()):
            grid[(x, y)] = char

    regions = partition(grid)

    return grid, regions


def partition(data):
    "Partition grid into regions"
    regions = []
    dirs = (N, S, W, E)
    todo = set(data.keys())

    while todo:
        current = todo.pop()
        letter = data[current]
        region = {current}
        while ext := {
            pt
            for (z, w), (dx, dy) in itertools.product(region, dirs)
            if (pt := (z + dx, w + dy)) not in region and data[pt] == letter
        }:
            region.update(ext)
        regions.append(region)
        todo.difference_update(region)

    return regions


def perimiter(region):
    dirs = (N, S, W, E)
    return sum((x + dx, y + dy) not in region for (x, y), (dx, dy) in itertools.product(region, dirs))


def intervals(interval):
    "Count continuous intervals of integers in interval"
    if not interval:
        return 0

    return sum(b - a > 1 for a, b in itertools.pairwise(interval)) + 1


def sides(region):
    "Count the sides of region"
    dirs = (N, S, W, E)

    boundary = [(x, y) for x, y in region if any((x + dx, y + dy) not in region for dx, dy in dirs)]
    hedgehog = [((x, y), (dx, dy)) for x, y in region for dx, dy in dirs if (x + dx, y + dy) not in region]

    m_x = min(x for x, _ in boundary)
    M_x = max(x for x, _ in boundary) + 1
    m_y = min(y for _, y in boundary)
    M_y = max(y for _, y in boundary) + 1

    count = 0
    for x in range(m_x, M_x):
        count += intervals([y for y in range(m_y, M_y) if ((x, y), W) in hedgehog])
        count += intervals([y for y in range(m_y, M_y) if ((x, y), E) in hedgehog])

    for y in range(m_y, M_y):
        count += intervals([x for x in range(m_x, M_x) if ((x, y), N) in hedgehog])
        count += intervals([x for x in range(m_x, M_x) if ((x, y), S) in hedgehog])

    return count


def part1(data):
    grid, regions = data

    return sum(len(region) * perimiter(region) for region in regions)


def part2(data):
    grid, regions = data

    return sum(len(region) * sides(region) for region in regions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
