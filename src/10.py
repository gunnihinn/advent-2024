import argparse
import collections
import itertools


def parse(fh):
    data = {}
    for j, line in enumerate(fh.readlines()):
        for i, char in enumerate(line.strip()):
            data[(i, j)] = int(char)

    return data


def dijkstra(data, start):
    unvisited = {xy for xy in data}
    dist = {xy: None for xy in data}
    dist[start] = 0
    infty = 10 * len(data)

    while True:
        try:
            current = next(xy for xy in unvisited if xy in dist)
        except StopIteration:
            break

        x, y = current
        for dx, dy in itertools.product((-1, 1), repeat=2):
            neighbor = (x + dx, y + dy)
            if neighbor not in data:
                continue
            elif data[neighbor] != data[current] + 1:
                continue
            else:
                dist[neighbor] = min(dist.get(neighbor, infty), dist[(x, y)] + 1)

        unvisited.remove(current)

    return dist


def part1(data):
    total = 0

    starts = {xy for xy, v in data.items() if v == 0}
    ends = {xy for xy, v in data.items() if v == 9}
    for start in starts:
        dist = dijkstra(data, start)
        for end in ends:
            if end in dist:
                total += 1

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
