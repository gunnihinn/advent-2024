import argparse
import collections
import itertools

# Real input has ~ 100.000 items if we expand it.

Block = collections.namedtuple("Block", ["id", "file"])


def parse(fh):
    data = []

    for _id, rep in enumerate(fh.read().strip()):
        data.extend([Block(int(_id) // 2, int(_id) % 2 == 0)] * int(rep))

    return data


def render(data):
    s = []
    for block in data:
        if block.file:
            s.append(f"{block.id}")
        else:
            s.append(".")

    return "".join(s)


def part1(data):
    total = 0
    return total


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
