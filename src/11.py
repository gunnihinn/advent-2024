import argparse
import copy
import functools
import math


def parse(fh):
    return list(map(int, fh.read().strip().split()))


def num_digits(n):
    return math.floor(math.log10(n)) + 1


@functools.cache
def rec(n, blink):
    while blink:
        if n == 0:
            n = 1
        elif (d := num_digits(n)) % 2 == 0:
            m = 10 ** (d // 2)
            return rec(n // m, blink - 1) + rec(n % m, blink - 1)
        else:
            n *= 2024
        blink -= 1

    return 1


def part2(data, repeat):
    return sum(rec(n, repeat) for n in data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part2(copy.deepcopy(data), 25))
    print(part2(copy.deepcopy(data), 75))
