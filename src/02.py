import argparse
import collections
import itertools
from typing import *


def sign(n: int) -> int:
    if n == 0:
        return 0
    elif n > 0:
        return 1
    else:
        return -1


def monotone(ns: Sequence[int]) -> bool:
    return abs(sum(sign(a - b) for a, b in zip(ns, ns[1:]))) == len(ns) - 1


def bounded(ns: Sequence[int]) -> bool:
    return all(1 <= abs(a - b) <= 3 for a, b in zip(ns, ns[1:]))


def part1(data: List[Tuple[int, ...]]) -> int:
    return sum(monotone(ns) and bounded(ns) for ns in data)


def safe_subset(ns: Tuple[int, ...]) -> bool:
    for i in range(len(ns)):
        ms = list(ns)
        ms.pop(i)
        if monotone(ms) and bounded(ms):
            return True

    return False


def part2(data: List[Tuple[int, ...]]) -> int:
    return sum(safe_subset(ns) for ns in data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    data = []
    with open(args.filename) as fh:
        for line in fh.readlines():
            data.append(tuple(int(n) for n in line.split()))

    print(part1(data))
    print(part2(data))
