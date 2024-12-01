import argparse
import collections


def part1(data):
    fst = sorted(a for a, _ in data)
    snd = sorted(b for _, b in data)

    return sum(abs(a - b) for a, b in zip(fst, snd))


def part2(data):
    fst = collections.Counter(a for a, _ in data)
    snd = collections.Counter(b for _, b in data)
    count = collections.defaultdict(int)

    for n in fst:
        count[n] += snd.get(n, 0)

    s = 0
    for a, b in data:
        s += a * count[a]

    return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    data = []
    with open(args.filename) as fh:
        for line in fh.readlines():
            a, b = line.split()
            data.append((int(a), int(b)))

    print(part1(data))
    print(part2(data))
