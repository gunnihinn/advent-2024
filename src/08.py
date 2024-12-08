import argparse
import collections
import itertools


class Grid:
    def __init__(self, m_x, m_y, antennas, orig):
        self.m_x = m_x
        self.m_y = m_y
        self.antennas = antennas
        self.orig = orig

    def inside(self, x, y):
        return 0 <= x < self.m_x and 0 <= y < self.m_y


def parse(fh):
    antennas = collections.defaultdict(list)
    m_x = 0
    m_y = 0
    orig = fh.read()

    for y, line in enumerate(orig.strip().split()):
        m_y += 1
        for x, char in enumerate(line.strip()):
            m_x = len(line.strip())
            if char != ".":
                antennas[char].append((x, y))

    return Grid(m_x, m_y, antennas, orig.strip().split())


def render(grid, antinodes):
    for y, line in enumerate(grid.orig):
        chars = []
        for x, char in enumerate(line):
            if (x, y) in antinodes:
                chars.append("#")
            else:
                chars.append(char)
        print("".join(chars))


def part1(data):
    antinodes = set()

    for freq in data.antennas:
        for fst, snd in itertools.combinations(data.antennas[freq], 2):
            dx, dy = snd[0] - fst[0], snd[1] - fst[1]
            antinodes.add((fst[0] - dx, fst[1] - dy))
            antinodes.add((snd[0] + dx, snd[1] + dy))

    return sum(data.inside(x, y) for x, y in antinodes)


def part2(data):
    antinodes = set()

    for freq in data.antennas:
        for fst, snd in itertools.combinations(data.antennas[freq], 2):
            dx, dy = snd[0] - fst[0], snd[1] - fst[1]

            x, y = fst
            while data.inside(x, y):
                antinodes.add((x, y))
                x, y = x - dx, y - dy

            x, y = snd
            while data.inside(x, y):
                antinodes.add((x, y))
                x, y = x + dx, y + dy

    return sum(data.inside(x, y) for x, y in antinodes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
