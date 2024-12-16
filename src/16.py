import argparse
import copy
import functools
import itertools

turns = {
    (-1, 0): ((0, 1), (0, -1)),
    (1, 0): ((0, 1), (0, -1)),
    (0, 1): ((1, 0), (-1, 0)),
    (0, -1): ((1, 0), (-1, 0)),
}


def parse(fh):
    blob = fh.read().strip().split("\n\n")

    start, end = None, None
    grid = {}
    for y, line in enumerate(blob[0].split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                grid[(x, y)] = char
            elif char == "S":
                start = (x, y)
                grid[(x, y)] = "."
            elif char == "E":
                end = (x, y)
                grid[(x, y)] = "."
            else:
                grid[(x, y)] = char

    return grid, start, end


def render(grid, start, end):
    max_x = max(x for x, _ in grid) + 1
    max_y = max(y for _, y in grid) + 1

    lines = []
    for y in range(max_y):
        line = []
        for x in range(max_x):
            if (x, y) == start:
                line.append("S")
            elif (x, y) == end:
                line.append("E")
            else:
                line.append(grid[(x, y)])
        lines.append("".join(line))

    return "\n".join(lines)


def dijkstra(grid, start):
    unvisited = set(itertools.product(grid.keys(), turns.keys()))
    dist = {(start, (1, 0)): 0}

    while True:
        current, d = None, 0
        for p, v in dist.items():
            if p in unvisited:
                if current is None or v < d:
                    current = p
                    d = v
        if current is None:
            break

        (x, y), (dx, dy) = current
        neighbors = []
        if grid[pt := (x + dx, y + dy)] == ".":
            neighbors.append(((pt, (dx, dy)), 1))
        for dz, dw in turns[(dx, dy)]:
            neighbors.append((((x, y), (dz, dw)), 1000))

        for neighbor, cost in neighbors:
            if neighbor in dist:
                dist[neighbor] = min(dist[neighbor], dist[current] + cost)
            else:
                dist[neighbor] = dist[current] + cost

        unvisited.remove(current)

    return dist


def part1(data):
    grid, start, end = data
    dist = dijkstra(grid, start)

    return min(dist.get((end, t), 10**20) for t in turns)


def score(path):
    total = 0

    for (_, dt1), (_, dt2) in itertools.pairwise(path):
        if dt1 == dt2:
            total += 1
        else:
            total += 1001

    return total


def part2(data):
    grid, start, end = data

    paths = [((start, (1, 0)),)]
    completed = []
    while paths:
        i = 0
        while i < len(paths):
            path = paths.pop(i)
            (x, y), (dx, dy) = path[-1]
            if grid[pt := (x + dx, y + dy)] == ".":
                if all(xy != pt for xy, _ in path):
                    if pt == end:
                        completed.append(path + ((pt, (dx, dy)),))
                    else:
                        paths.insert(i, path + ((pt, (dx, dy)),))
                        i += 1
            for dx, dy in turns[(dx, dy)]:
                if grid[pt := (x + dx, y + dy)] == ".":
                    if all(xy != pt for xy, _ in path):
                        if pt == end:
                            completed.append(path + ((pt, (dx, dy)),))
                        else:
                            paths.insert(i, path + ((pt, (dx, dy)),))
                            i += 1

    m = min(score(path) for path in completed)
    walked = set()
    for path in completed:
        if score(path) == m:
            for xy, _ in path:
                walked.add(xy)

    return len(walked)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(copy.deepcopy(data)))
    print(part2(copy.deepcopy(data)))
