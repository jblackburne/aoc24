from itertools import product


def ingest_p07(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    values, operands = zip(*[line.split(": ") for line in lines])
    values = [int(val) for val in values]
    operands = [[int(val) for val in operand.split()] for operand in operands]

    return values, operands


def p07a(values, operands, oplist=(int.__mul__, int.__add__)):
    total = 0
    for val, nums in zip(values, operands):
        n_nums = len(nums)
        for opcombo in product(oplist, repeat=n_nums-1):
            partial = nums[0]
            for op, nextnum in zip(opcombo, nums[1:]):
                partial = op(partial, nextnum)
            if partial > val:
                continue
            elif partial == val:
                total += val
                break

    return total

def p07b(values, operands):
    concat = lambda x, y: int(str(x) + str(y))
    oplist = (int.__mul__, int.__add__, concat)
    return p07a(values, operands, oplist)


if __name__ == "__main__":
    values, operands = ingest_p07("data/input_p07.txt")

    print("Part 1: {}".format(p07a(values, operands)))
    print("Part 2: {}".format(p07b(values, operands)))
