import argparse
import functools


def parse(fh):
    parts = fh.read().strip().split("\n\n")
    patterns = tuple(parts[0].strip().split(", "))
    designs = tuple(parts[1].strip().split("\n"))

    return patterns, designs


@functools.cache
def rec(patterns, design, i=0):
    if i == len(design):
        return 1

    return sum(design.startswith(p, i) and rec(patterns, design, i + len(p)) for p in patterns)


def part1(data):
    patterns, designs = data

    def m(d):
        return rec(patterns, d) > 0

    return sum(m(design) for design in designs)


def part2(data):
    patterns, designs = data

    def m(d):
        return rec(patterns, d)

    return sum(m(design) for design in designs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
