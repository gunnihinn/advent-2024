import argparse
import collections
import itertools


def parse(fh):
    data = {}
    for j, line in enumerate(fh.readlines()):
        for i, char in enumerate(line.strip()):
            data[(i, j)] = int(char)

    return data


def part1(data):
    starts = {xy for xy, v in data.items() if v == 0}
    paths = {(start,) for start in starts}
    dirs = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    for _ in range(9):
        new_paths = set()
        for path in paths:
            # print(f"path={path}")
            x, y = path[-1]
            for dx, dy in dirs:
                neighbor = (x + dx, y + dy)
                if neighbor not in data:
                    # print(f"neighbor={neighbor} not in grid")
                    continue
                elif data[neighbor] != data[(x, y)] + 1:
                    # print(f"neighbor={neighbor} not accessible")
                    continue
                # print(f"{path} -> {neighbor}")
                new_paths.add(path + (neighbor,))

        # print(f"paths={paths}")
        # print(f"new_paths={new_paths}")
        paths = new_paths

    scores = collections.defaultdict(set)
    for path in paths:
        scores[path[0]].add(path[-1])

    return sum(len(v) for v in scores.values())


def part2(data):
    starts = {xy for xy, v in data.items() if v == 0}
    paths = {(start,) for start in starts}
    dirs = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    for _ in range(9):
        new_paths = set()
        for path in paths:
            # print(f"path={path}")
            x, y = path[-1]
            for dx, dy in dirs:
                neighbor = (x + dx, y + dy)
                if neighbor not in data:
                    # print(f"neighbor={neighbor} not in grid")
                    continue
                elif data[neighbor] != data[(x, y)] + 1:
                    # print(f"neighbor={neighbor} not accessible")
                    continue
                # print(f"{path} -> {neighbor}")
                new_paths.add(path + (neighbor,))

        # print(f"paths={paths}")
        # print(f"new_paths={new_paths}")
        paths = new_paths

    return len(paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
