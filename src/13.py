import argparse
import collections
import itertools
import re

re_digit = re.compile(r"\+?(\d+)")


def parse(fh):
    blob = fh.read().strip()
    data = []
    for machine in blob.split("\n\n"):
        m = re_digit.findall(machine)
        Ax = int(m[0])
        Ay = int(m[1])
        Bx = int(m[2])
        By = int(m[3])
        X = int(m[4])
        Y = int(m[5])
        data.append(((Ax, Ay), (Bx, By), X, Y))

    return data


def solve2x2(machine):
    A, B, X, Y = machine
    ax, ay = A
    bx, by = B
    det = ax * by - ay * bx
    if abs(det) == 0:
        raise ValueError(f"A={A}, B={B}, X={X}, Y={Y}, det=0")

    u, v = (by * X - bx * Y) // det, (-ay * X + ax * Y) // det
    if ax * u + bx * v == X and ay * u + by * v == Y:
        return 3 * u + v

    return 0


def part1(data):
    return sum(solve2x2(machine) for machine in data)


def part2(data):
    return sum(solve2x2((A, B, X + 10000000000000, Y + 10000000000000)) for A, B, X, Y in data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
