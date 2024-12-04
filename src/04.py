import argparse
import collections
import itertools
from typing import *


def parse(fh):
    return [list(line.strip()) for line in fh.readlines()]


def xmas(data, dirs, i, j):
    if data[j][i] != "X":
        return 0

    c = 0
    for dij in dirs:
        try:
            if all(
                (
                    0 <= i + dij[2][0],
                    0 <= j + dij[2][1],
                    data[j + dij[0][1]][i + dij[0][0]] == "M",
                    data[j + dij[1][1]][i + dij[1][0]] == "A",
                    data[j + dij[2][1]][i + dij[2][0]] == "S",
                )
            ):
                c += 1
        except IndexError:
            continue

    return c


def x_mas(data, dirs, i, j):
    if data[j][i] != "A":
        return 0

    c = 0
    for d1, d2 in itertools.combinations(dirs, 2):
        try:
            if all(
                (
                    0 <= i + d1[0][0],
                    0 <= i + d1[1][0],
                    0 <= j + d1[0][1],
                    0 <= j + d1[1][1],
                    data[j + d1[0][1]][i + d1[0][0]] == "M",
                    data[j + d1[1][1]][i + d1[1][0]] == "S",
                    0 <= i + d2[0][0],
                    0 <= i + d2[1][0],
                    0 <= j + d2[0][1],
                    0 <= j + d2[1][1],
                    data[j + d2[0][1]][i + d2[0][0]] == "M",
                    data[j + d2[1][1]][i + d2[1][0]] == "S",
                )
            ):
                c += 1
        except IndexError:
            continue

    return c


def part1(data):
    dirs = [
        [(1, 0), (2, 0), (3, 0)],
        [(1, 1), (2, 2), (3, 3)],
        [(0, 1), (0, 2), (0, 3)],
        [(-1, 1), (-2, 2), (-3, 3)],
        [(-1, 0), (-2, 0), (-3, 0)],
        [(-1, -1), (-2, -2), (-3, -3)],
        [(0, -1), (0, -2), (0, -3)],
        [(1, -1), (2, -2), (3, -3)],
    ]

    count = 0
    for j in range(len(data)):
        for i in range(len(data[0])):
            count += xmas(data, dirs, i, j)

    return count


def part2(data):
    dirs = [
        [(1, 1), (-1, -1)],
        [(-1, 1), (1, -1)],
        [(-1, -1), (1, 1)],
        [(1, -1), (-1, 1)],
    ]

    count = 0
    for j in range(len(data)):
        for i in range(len(data[0])):
            count += x_mas(data, dirs, i, j)

    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
