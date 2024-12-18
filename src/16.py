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


def p2(grid, start, end, best, dt, score, path, idx=0):
    x, y = path[idx]
    for dx, dy in turns[dt]:
        if grid[pt := (x + dx, y + dy)] == "." and pt not in path[: idx + 1]:
            cost = 1 if (dx, dy) == dt else 1001
            if score + cost <= best:
                if pt == end:
                    path[idx + 1] = pt
                    yield (score + cost, path[: idx + 2])
                else:
                    path[idx + 1] = pt
                    yield from p2(
                        grid,
                        start,
                        end,
                        best,
                        (dx, dy),
                        score + cost,
                        path,
                        idx + 1,
                    )


def part2rec(data, best):
    grid, start, end = data

    walked = set()
    path = [None] * (len(grid) + 1)
    path[0] = start
    for path in p2(grid, start, end, best, (1, 0), 0, path):
        if path is not None and path[0] == best:
            walked.update(path[1])
            print(f"tiles seen={len(walked)}")

    return len(walked)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    # best = part1(copy.deepcopy(data))
    # print(best)
    # print(part2rec(copy.deepcopy(data), best))
    print(part2rec(copy.deepcopy(data), 75416))
