def ingest_p05(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    parsing_rules = True
    rules = {}
    data = []
    for line in lines:
        if not line:
            parsing_rules = False
            continue
        if parsing_rules:
            a, b = [int(x) for x in line.split("|")]
            rules[b] = rules.get(b, []) + [a]
        else:
            data.append([int(x) for x in line.split(",")])

    return rules, data


def p05a(rules, data):
    total = 0
    for update in data:
        verboten = set()
        seen = set()
        is_safe = True
        for item in update:
            if item in verboten:
                # unsafe update
                is_safe = False
                break
            deps = rules.get(item, [])
            for dep in deps:
                if dep not in seen:
                    verboten.add(dep)
            seen.add(item)
        if is_safe:
            total += update[len(update) // 2]

    return total


def p05b(rules, data):
    total = 0
    for update in data:
        is_safe = True
        lidx = 0
        while lidx < len(update):
            for ridx in range(lidx + 1, len(update)):
                verboten = set(rules.get(update[lidx], []))
                if update[ridx] in verboten:
                    is_safe = False
                    # Move the rule-breaking number just before the current number
                    # Then start again at the same index
                    rbn = update[ridx]
                    update.pop(ridx)
                    update.insert(lidx, rbn)
                    lidx -= 1
                    break
            lidx += 1
        if not is_safe:
            total += update[len(update) // 2]

    return total


if __name__ == "__main__":
    rules, data = ingest_p05("data/input_p05.txt")

    print("Part 1: {}".format(p05a(rules, data)))
    print("Part 2: {}".format(p05b(rules, data)))
