from collections import namedtuple


Record = namedtuple("Record", ["id", "size"])

def _to_internal(data, ndigit=1):
    nbatch = (len(data) + ndigit - 1) // ndigit
    file_id = 0
    my_data = []
    for ibatch in range(nbatch):
        batch = data[(ibatch * ndigit):((ibatch + 1) * ndigit)]
        is_file = not (ibatch % 2)
        if is_file:
            my_data.append(Record(file_id, int(batch)))
            file_id += 1
        else:
            my_data.append(Record(-1, int(batch)))

    return my_data


def p09a(data, ndigit=1):
    data = _to_internal(data, ndigit)
    lidx = 1  # first free space element
    ridx = ((len(data) - 1) // 2) * 2  # last file element
    while lidx < ridx:
        space_avail = data[lidx].size
        if space_avail == 0:
            # No space to put data in; go to the next free space
            lidx += 2
            continue
        size_moved = min(space_avail, data[ridx].size)
        # Handle the left-hand side
        space_avail -= size_moved
        data[lidx] = Record(-1, 0)
        data.insert(lidx + 1, Record(data[ridx].id, size_moved))
        data.insert(lidx + 2, Record(-1, space_avail))
        lidx += 2
        ridx += 2  # To account for the two inserted records
        # Handle the right-hand side
        data[ridx] = Record(data[ridx].id, data[ridx].size - size_moved)
        if data[ridx].size == 0:
            data.pop(ridx)
            ridx -= 2

    idx = 0
    checksum = 0
    for record in data:
        if record.id == -1:
            continue
        for _ in range(record.size):
            checksum += idx * record.id
            idx += 1

    return checksum


def p09b(data):
    data = _to_internal(data)  # ndigit is still 1; so much for predicting what part 2 would do
    # lidx[i] always points to the leftmost free space element of size (i+1) or greater
    lidx = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ridx = ((len(data) - 1) // 2) * 2  # Last file element
    while ridx > 0:
        for i in range(len(lidx)):
            while data[lidx[i]].size < i + 1 and lidx[i] < ridx and lidx[i] < len(data) - 2:
                lidx[i] += 2
        idx = lidx[data[ridx].size - 1]
        if idx < ridx:
            extra_space = data[idx].size - data[ridx].size
            data[idx] = Record(-1, 0)
            data.insert(idx + 1, data[ridx])
            data.insert(idx + 2, Record(-1, extra_space))
            ridx += 2  # To account for the two inserted records
            combined_size = data[ridx - 1].size
            combined_size += data.pop(ridx).size
            if ridx < len(data):
                combined_size += data.pop(ridx).size
            data[ridx - 1] = Record(-1, combined_size)
        ridx -= 2

    idx = 0
    checksum = 0
    for record in data:
        if record.id == -1:
            idx += record.size
            continue
        for _ in range(record.size):
            checksum += idx * record.id
            idx += 1

    return checksum


if __name__ == "__main__":
    with open("data/input_p09.txt", "r") as f:
        data = f.readlines()[0].strip()

    print("Part 1: {}".format(p09a(data)))
    print("Part 2: {}".format(p09b(data)))
