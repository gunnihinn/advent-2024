import argparse
import collections
import itertools


def parse(fh):
    rules = set()
    lines = []

    in_rules = True
    for line in (line.strip() for line in fh.readlines()):
        if not line:
            in_rules = False
        elif in_rules:
            rules.add(tuple(map(int, line.split("|"))))
        else:
            lines.append(tuple(map(int, line.split(","))))

    return (rules, lines)


def part1(data):
    rules, lines = data

    total = 0

    for line in lines:
        if all(tuple(ab) in rules for ab in itertools.combinations(line, 2)):
            total += line[len(line) // 2]

    return total


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
