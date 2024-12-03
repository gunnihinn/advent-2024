import argparse
import collections
import itertools
import re
from typing import *


def parse(fh):
    re_mul = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    lines = []
    for line in fh.readlines():
        pairs = []
        while m := re_mul.search(line):
            pairs.append((int(m.group(1)), int(m.group(2))))
            line = line[m.span()[1] :]
        lines.append(pairs)

    return lines


def part1(data):
    return sum(sum(a * b for a, b in pairs) for pairs in data)


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
