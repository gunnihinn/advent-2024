import argparse
import collections
import itertools
import re
from typing import *


def parse(fh):
    re_mul = re.compile(r"(mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don't\(\))")

    lines = []
    do = True
    for line in fh.readlines():
        ms = re_mul.findall(line)
        ops = []
        for m in ms:
            if m[0] == "do()":
                do = True
            elif m[0] == "don't()":
                do = False
            else:
                ops.append((do, int(m[1]), int(m[2])))
        lines.append(ops)

    return lines


def part1(data):
    return sum(sum(a * b for _, a, b in ops) for ops in data)


def part2(data):
    return sum(sum(do * a * b for do, a, b in ops) for ops in data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
