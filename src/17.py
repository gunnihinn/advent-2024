import argparse
import copy
import re


class Computer:
    def __init__(self, registers, program):
        self.A, self.B, self.C = registers
        self.program = program
        self.ip = 0
        self.out = []
        self.part2 = False

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
            self.A = self.A >> self.combo(self.ip + 1)
        elif ins == 1:
            self.B = self.B ^ self.literal(self.ip + 1)
        elif ins == 2:
            self.B = self.combo(self.ip + 1) & 0b111
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
            val = self.combo(self.ip + 1) & 0b111
            if self.part2 and not self.program[len(self.out)] == val:
                raise ValueError()
            self.out.append(val)
        elif ins == 6:
            self.B = self.A >> self.combo(self.ip + 1)
        elif ins == 7:
            self.C = self.A >> self.combo(self.ip + 1)
        self.ip += 2

    def run(self, A=None):
        if A is not None:
            self.A = A

        while True:
            try:
                self.instruction()
            except IndexError:
                return self.out

    def run2(self, A):
        b, c = self.B, self.C
        while True:
            if A % 100_000 == 0:
                print(f". A={A}")
            try:
                got = self.run(A)
                if got == self.program:
                    print(f"    got={got}")
                    return A
                else:
                    raise ValueError()
            except ValueError:
                A += 1
                self.B, self.C = b, c
                self.ip = 0
                self.out = []


def parse(fh):
    digits = re.compile(r"(\d+)")

    regs, prog = fh.read().strip().split("\n\n")
    registers = list(map(int, digits.findall(regs)))
    program = list(map(int, digits.findall(prog)))

    return Computer(registers, program)


def part1(data):
    return ",".join(str(n) for n in data.run())


def part2(data, A):
    print(f"program={data.program}")
    assert data.ip == 0
    data.part2 = True
    return data.run2(A)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--A", type=int, default=0, help="start part 2 with this A")
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        data = parse(fh)

    print(part1(copy.deepcopy(data)))
    # Have run up to A=85_000_000
    print(part2(copy.deepcopy(data), args.A))
