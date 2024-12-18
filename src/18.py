import argparse
import itertools
import re


def parse(fh):
    size, coords = fh.read().strip().split("\n\n")
    digits = re.compile(r"(\d+)")

    lower, upper, byte_limit = list(map(int, digits.findall(size)))
    points = [tuple(map(int, digits.findall(line))) for line in coords.split("\n")]

    return lower, upper, byte_limit, points


def render(lower, upper, points):
    lines = []
    for y in range(lower, upper + 1):
        line = []
        for x in range(lower, upper + 1):
            if (x, y) in points:
                line.append("#")
            else:
                line.append(".")
        lines.append("".join(line))
    return "\n".join(lines)


def dijkstra(lower, upper, points):
    points = set(points)
    assert (0, 0) not in points
    unvisited = {(x, y) for x, y in itertools.product(range(lower, upper + 1), repeat=2) if (x, y) not in points}
    dist = {(0, 0): 0}
    dirs = (
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    )

    while True:
        current, d = None, 0
        for p, v in dist.items():
            if p in unvisited:
                if current is None or v < d:
                    current = p
                    d = v
        if current is None:
            break

        (x, y) = current
        for dx, dy in dirs:
            pt = (x + dx, y + dy)
            if not (0 <= pt[0] <= upper and 0 <= pt[1] <= upper):
                continue
            if pt in points:
                continue
            if pt in dist:
                dist[pt] = min(dist[pt], dist[current] + 1)
            else:
                dist[pt] = dist[current] + 1

        unvisited.remove(current)

    return dist


def part1(data):
    lower, upper, byte_limit, points = data
    dist = dijkstra(lower, upper, points[:byte_limit])

    return dist[(upper, upper)]


def part2(data):
    lower, upper, byte_limit, points = data

    good = 0
    bad = len(points) - 1
    idx = (good + bad) // 2
    while good < idx < bad:
        escape = (upper, upper) in dijkstra(lower, upper, points[:idx])
        print(f"good={good}, bad={bad}, idx={idx}, escaped={escape}")
        if escape:
            good = idx
        else:
            bad = idx
        idx = (good + bad) // 2
    print(f"good={good}, bad={bad}, idx={idx}, escaped={escape}")

    return f"{points[good][0]},{points[good][1]}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
