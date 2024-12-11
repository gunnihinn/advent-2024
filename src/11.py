import argparse
import copy
import math


def parse(fh):
    return list(map(int, fh.read().strip().split()))


def num_digits(n):
    return math.floor(math.log10(n)) + 1


def part1(data, blink):
    for i in range(blink):
        new_data = []
        for n in data:
            if n == 0:
                new_data.append(1)
                continue
            d = num_digits(n)
            if d % 2 == 0:
                m = 10 ** (d // 2)
                new_data.append(n // m)
                new_data.append(n % m)
            else:
                new_data.append(n * 2024)
        data = new_data

    return len(data)


def rec(n, blink, limit, cache):
    if blink == limit:
        return 1

    if (n, blink) in cache:
        return cache[(n, blink)]

    while blink < limit:
        if n == 0:
            n = 1
        else:
            d = num_digits(n)
            if d % 2 == 0:
                m = 10 ** (d // 2)
                a = rec(n // m, blink + 1, limit, cache)
                b = rec(n % m, blink + 1, limit, cache)
                cache[(n // m, blink + 1)] = a
                cache[(n % m, blink + 1)] = b
                return a + b
            else:
                n *= 2024

        blink += 1

    return 1


def part2(data, repeat):
    total = 0

    cache = {}
    for n in data:
        a = rec(n, 0, repeat, cache)
        cache[(n, repeat)] = a
        total += a

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(copy.deepcopy(data), 25))
    print(part2(copy.deepcopy(data), 75))
