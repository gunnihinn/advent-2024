import argparse
import copy
import itertools

turns = {
    (-1, 0): ((-1, 0), (0, 1), (0, -1)),
    (1, 0): ((1, 0), (0, 1), (0, -1)),
    (0, 1): ((0, 1), (1, 0), (-1, 0)),
    (0, -1): ((0, -1), (1, 0), (-1, 0)),
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

        (x, y), dt = current
        neighbors = []
        for dx, dy in turns[dt]:
            if grid[pt := (x + dx, y + dy)] == ".":
                cost = 1 if (dx, dy) == dt else 1001
                neighbors.append(((pt, (dx, dy)), cost))

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
    points, start, end, _ = path

    x, y = start
    dt = (1, 0)
    total = 0
    while (x, y) != end:
        for dx, dy in turns[dt]:
            if (pt := (x + dx, y + dy)) in points:
                cost = 1 if (dx, dy) == dt else 1001
                total += cost
                dt = (dx, dy)
                x, y = pt
                break
        else:
            break

    return total


def p2(grid, start, end, best, path):
    if path[4] > best:
        return None

    x, y = path[2]
    dt = path[3]
    for dx, dy in turns[dt]:
        if grid[pt := (x + dx, y + dy)] == "." and pt not in path[0]:
            cost = 1 if (dx, dy) == dt else 1001
            if path[4] + cost <= best:
                p = copy.deepcopy(path)
                p[4] += cost
                p[0].add(pt)
                if pt == end:
                    p[2] = pt
                    p[3] = (dx, dy)
                    yield p
                else:
                    p[2] = pt
                    p[3] = (dx, dy)
                    yield from p2(grid, start, end, best, p)


def part2rec(data, best):
    grid, start, end = data

    walked = set()
    for path in p2(grid, start, end, best, [{start}, start, start, (1, 0), 0]):
        print(f"path={path}")
        if path is not None and path[4] == best:
            walked.update(path[0])

    return len(walked)


def part2(data, best):
    grid, start, end = data

    # path: [points, start, current, tangent]

    paths = [[{start}, start, start, (1, 0)]]
    completed = []
    while paths:
        i = 0
        print(f"checking {len(paths)} paths, completed {len(completed)}")
        while i < len(paths):
            path = paths.pop(i)
            if score(path) > best:
                continue

            x, y = path[2]
            dt = path[3]
            for dx, dy in turns[dt]:
                if grid[pt := (x + dx, y + dy)] == "." and pt not in path[0]:
                    p = copy.deepcopy(path)
                    p[0].add(pt)
                    if pt == end:
                        p[2] = pt
                        p[3] = (dx, dy)
                        completed.append(p)
                    else:
                        p[2] = pt
                        p[3] = (dx, dy)
                        paths.insert(i, p)
                        i += 1

    walked = set()
    for path in completed:
        if score(path) == best:
            walked.update(path[0])

    return len(walked)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    # best = part1(copy.deepcopy(data))
    # print(best)
    # print(part2(copy.deepcopy(data), 75416))
    print(part2rec(copy.deepcopy(data), 75416))
