import argparse
import collections
import itertools
import math
import re


class Computer:
    def __init__(self, registers, program):
        self.A, self.B, self.C = registers
        self.program = program
        self.ip = 0

    def literal(self, idx):
        return self.program[idx]

    def combo(self, idx):
        op = self.program[idx]
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return self.A
        elif op == 5:
            return self.B
        elif op == 6:
            return self.C
        else:
            raise ValueError(f"Reserved operand {op}")

    def instruction(self):
        ins = self.program[self.ip]

        if ins == 0:
            self.A = math.floor(self.A / 2 ** self.combo(self.ip + 1))
        elif ins == 1:
            self.B = self.B ^ self.literal(self.ip + 1)
        elif ins == 2:
            self.B = self.combo(self.ip + 1) % 8
        elif ins == 3:
            if self.A == 0:
                pass
            else:
                self.ip = self.literal(self.ip + 1)
                return
                # no ip increase
        elif ins == 4:
            self.B = self.B ^ self.C
        elif ins == 5:
            print(f"{self.combo(self.ip + 1) % 8},", end="")
        elif ins == 6:
            self.B = math.floor(self.A / 2 ** self.combo(self.ip + 1))
        elif ins == 7:
            self.C = math.floor(self.A / 2 ** self.combo(self.ip + 1))
        self.ip += 2

    def run(self):
        while True:
            try:
                self.instruction()
            except IndexError:
                return


def parse(fh):
    digits = re.compile(r"(\d+)")

    regs, prog = fh.read().strip().split("\n\n")
    registers = list(map(int, digits.findall(regs)))
    program = list(map(int, digits.findall(prog)))

    return Computer(registers, program)


def part1(data):
    data.run()
    print("")


def part2(data):
    total = 0
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    part1(data)
    print(part2(data))
