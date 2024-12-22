import argparse

prune = 16777216


def parse(fh):
    return list(int(line) for line in fh.readlines())


def mul(factor):
    return lambda n: (n ^ (n * factor)) % prune


def div(factor):
    return lambda n: (n ^ (n // factor)) % prune


def part1(data):
    steps = [mul(64), div(32), mul(2048)]

    def proc(n):
        for fn in steps:
            n = fn(n)
        return n

    def g(n):
        for _ in range(2000):
            n = proc(n)
        return n

    return sum(g(n) for n in data)


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
