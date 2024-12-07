import argparse
import itertools


def parse(fh):
    data = {}
    for line in fh.readlines():
        val, rest = line.strip().split(": ")
        data[int(val)] = tuple(map(int, rest.split(" ")))

    return data


def calc(nums, combo):
    total = nums[0]
    for n, op in zip(nums[1:], combo):
        if op == "+":
            total += n
        elif op == "*":
            total *= n
        elif op == "|":
            d = len(str(n))
            total = total * 10**d + n

    return total


def eq(val, nums, ops):
    for combo in itertools.product(ops, repeat=len(nums) - 1):
        if val == calc(nums, combo):
            return True
    return False


def part1(data):
    ops = ("+", "*")
    return sum(val for val, nums in data.items() if eq(val, nums, ops))


def part2(data):
    ops = ("+", "*", "|")
    return sum(val for val, nums in data.items() if eq(val, nums, ops))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(data))
    print(part2(data))
