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


def in_order(line, rules):
    return all(tuple(ab) in rules for ab in itertools.combinations(line, 2))


def part1(data):
    rules, lines = data

    total = 0
    for line in lines:
        if in_order(line, rules):
            total += line[len(line) // 2]

    return total


def part2(data):
    rules, lines = data

    total = 0
    for line in lines:
        if in_order(line, rules):
            continue

        line = list(line)
        while not in_order(line, rules):
            for i in range(len(line) - 1):
                for j in range(i + 1, len(line)):
                    if (line[i], line[j]) not in rules and (line[j], line[i]) in rules:
                        line[i], line[j] = line[j], line[i]
        total += line[len(line) // 2]

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
