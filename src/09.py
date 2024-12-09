import argparse
import collections
import copy

# Real input has ~ 100.000 items if we expand it.

Block = collections.namedtuple("Block", ["id", "file", "size"])


def parse(blob):
    data = []

    for _id, rep in enumerate(blob):
        data.extend([Block(int(_id) // 2, int(_id) % 2 == 0, int(rep))] * int(rep))

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
    idx_free = min(i for i, block in enumerate(data) if not block.file)
    idx_file = max(i for i, block in enumerate(data) if block.file)

    while idx_free < idx_file:
        data[idx_free], data[idx_file] = data[idx_file], data[idx_free]
        while data[idx_free].file:
            idx_free += 1
        while not data[idx_file].file:
            idx_file -= 1

    return sum(i * block.id for i, block in enumerate(data) if block.file)


def get_free_size(data, idx_free):
    size_free = 0
    i = idx_free
    while not data[i].file and i < len(data):
        size_free += 1
        i += 1

    return size_free


def find_free(data, size, upper_limit):
    i = 0
    while i < upper_limit:
        if data[i].file:
            i += data[i].size
        else:
            s = get_free_size(data, i)
            if s >= size:
                return i
            else:
                i += s

    raise Exception(f"No free space of size {size}")


def part2(data):
    idx_free = next(i for i, block in enumerate(data) if not block.file)
    idx_file = len(data)
    assert data[-1].file
    max_id = data[-1].id

    for fid in range(max_id, -1, -1):
        idx_file = next(i for i, block in enumerate(data) if block.file and block.id == fid)
        try:
            idx_free = find_free(data, data[idx_file].size, idx_file)
        except Exception:
            continue

        for i in range(data[idx_file].size):
            data[idx_free + i], data[idx_file + i] = (
                data[idx_file + i],
                data[idx_free + i],
            )

    return sum(i * block.id for i, block in enumerate(data) if block.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with problem input")
    args = parser.parse_args()

    with open(args.filename) as fh:
        blob = fh.read().strip()
        data = parse(blob)

    print(part1(copy.deepcopy(data)))
    print(part2(copy.deepcopy(data)))
