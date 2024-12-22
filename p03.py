import re

def p03a(lines):
    total = 0
    pattern = r"mul\((\d+),(\d+)\)"
    for line in lines:
        matches = re.findall(pattern, line)
        for a, b in matches:
            total += int(a) * int(b)

    return total

def p03b(lines):
    total = 0
    enabled = True
    pattern = "|".join([
        r"mul\((\d+),(\d+)\)",
        r"(do\(\))",
        r"(don't\(\))",
    ])
    for line in lines:
        matches = re.findall(pattern, line)
        for m in matches:
            if m[2] == "do()":
                enabled = True
            elif m[3] == "don't()":
                enabled = False
            else:
                if enabled:
                    total += int(m[0]) * int(m[1])

    return total

if __name__ == "__main__":
    with open("data/input_p03.txt", "r") as f:
        lines = f.readlines()

    print("Part 1: {}".format(p03a(lines)))
    print("Part 2: {}".format(p03b(lines)))
