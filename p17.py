NBITS = 3
BASE = 1 << NBITS

# Make this work by copying the values from data/input_p17.txt into these tuples
#REGISTERS_START = (#, #, #)
#PROGRAM = (#, #, #, #, #, #, #, #, #, #, #, #, #, #, #, #)

def _combo_op(opcode, regs):
    if opcode == 0: return 0
    if opcode == 1: return 1
    if opcode == 2: return 2
    if opcode == 3: return 3
    if opcode == 4: return regs[0]
    if opcode == 5: return regs[1]
    if opcode == 6: return regs[2]
    if opcode == 7: raise ValueError("Bad combo opcode!")

def _adv(op, regs, ip):
    regs[0] = regs[0] >> _combo_op(op, regs)
    return ip + 2, None

def _bxl(op, regs, ip):
    regs[1] = regs[1] ^ op
    return ip + 2, None

def _bst(op, regs, ip):
    regs[1] = _combo_op(op, regs) & (BASE - 1)
    return ip + 2, None

def _jnz(op, regs, ip):
    return (ip + 2 if regs[0] == 0 else op), None

def _bxc(op, regs, ip):
    regs[1] = regs[1] ^ regs[2]
    return ip + 2, None

def _out(op, regs, ip):
    return ip + 2, _combo_op(op, regs) & (BASE - 1)

def _bdv(op, regs, ip):
    regs[1] = regs[0] >> _combo_op(op, regs)
    return ip + 2, None

def _cdv(op, regs, ip):
    regs[2] = regs[0] >> _combo_op(op, regs)
    return ip + 2, None


OPS = {
    0: _adv,  # a = a >> combo_op
    1: _bxl,  # b ^= op
    2: _bst,  # b = combo_op mod 8
    3: _jnz,  # jump to op if a is 0
    4: _bxc,  # b ^= c
    5: _out,  # output combo_op mod 8
    6: _bdv,  # b = a >> combo_op
    7: _cdv,  # c = a >> combo_op
}

def p17a(program, registers):
    ip = 0  # instruction pointer
    regs = list(registers)
    output = []
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        ip, out = OPS[opcode](operand, regs, ip)
        if out is not None:
            output.append(out)

    return tuple(output)

def p17b(program):
    wq = [()]
    while wq:
        inp = wq.pop()
        working_newvals = []
        for newval in range(8):
            regA = 0
            for val in inp:
                regA = (regA | val) << 3
            regA |= newval
            out = p17a(program, (regA, 0, 0))
            if out == program[-len(out):]:
                if len(out) == len(program):
                    return regA
                working_newvals.append(newval)
        for wnv in working_newvals[::-1]:
            wq.append(inp + (wnv,))


if __name__ == "__main__":
    print("Part 1: {}".format(p17a(PROGRAM, REGISTERS_START)))
    print("Part 2: {}".format(p17b(PROGRAM)))
