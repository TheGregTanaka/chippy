import random

t   = lambda op: (op & 0xF000) >> 12
x   = lambda op: (op & 0x0F00) >> 8
y   = lambda op: (op & 0x00F0) >> 4
n   = lambda op: (op & 0x000F)
nn  = lambda op: (op & 0x00FF)
nnn = lambda op: (op & 0x0FFF)


def o_001N(c8, op):
    exit(n(op))

def o_00CN(c8, op):
    c8.display.scroll('down', n)

def o_00BN(c8, op):
    c8.display.scroll('up', n)

# clear display
def o_00E0(c8, op):
    c8.draw_flag = True
    c8.display.clear()

# return from subroutine
def o_00EE(c8, op):
    c8.pc = c8.stack.pop()

##
def o_00FA(c8, op):
    #TODO
    c8.quirks.load_store = not c8.quirks.load_store

def o_00FB(c8, op):
    c8.display.scroll('right', 4)
def o_00FC(c8, op):
    c8.display.scroll('left', 4)
def o_00FE(c8, op):
    #TODO c8.display.lo_res()
    pass
def o_00FF(c8, op):
    #TODO c8.display.hi_res()
    pass
    

# goto nnn
def o_1NNN(c8, op):
    c8.PC = nnn(op)

# call subroutine at nnn
def o_2NNN(c8, op):
    c8.stack.append(c8.pc)
    c8.pc = nnn(op)

# skip if  equal
def o_3XNN(c8, op):
    if c8.v[x(op)] == nn(op):
        c8.pc += 2

# skip if unequal
def o_4XNN(c8, op):
    if c8.v[x(op)] != nn(op):
        c8.pc += 2

# skip if Vx==Vy
def o_5XY0(c8, op):
    if c8.v[x(op)] == c8.v[y(op)]:
        c8.pc += 2

def o_5XY2(c8, op):
    #TODO
    pass
def o_5x03(c8, op):
    #TODO
    pass

# write nn to Vx
def o_6XNN(c8, op):
    c8.v[x(op)] = nn(op)

# add nn to Vx
def o_7XNN(c8, op):
    c8.v[x(op)] += nn(op)

# Vx = Vy
def o_8XY0(c8, op):
    c8.v[x(op)] = c8.v[y(op)]

# or Vx = Vx|Vy
def o_8XY1(c8, op):
    c8.v[x(op)] |= c8.v[y(op)]

# and Vx = Vx&Vy
def o_8XY2(c8, op):
    c8.v[x(op)] &= c8.v[y(op)]

# xor Vx = Vx^Vy
def o_8XY3(c8, op):
    c8.v[x(op)] ^= c8.v[y(op)]

# Vx += Vy, set carry
def o_8XY4(c8, op):
    xx = x(op)
    z = c8.v[xx] + c8.v[y(op)]
    c8.v[0xF] = 1 if z > 255 else 0
    c8.v[xx] = z & 0xFF

# Vx -= Vy, set ~borrow
def o_8XY5(c8, op):
    xx = x(op)
    yy = y(op)
    c8.v[0xF] = 1 if c8.v[xx] > c8.v[yy] else 0
    c8.v[xx] -= c8.v[yy]

# check lsb
def o_8XY6(c8, op):
    xx = x(op)
    lsb = c8.v[xx] & 1
    c8.v[0xF] = lsb
    c8.v[xx] >>= 1

# Vx = Vy-Vx, set ~borrow
def o_8XY7(c8, op):
    xx = x(op)
    z = c8.v[y(op)] - c8.v[xx]
    c8.v[0xF] = 1 if  z > 0 else 0
    c8.v[xx] = z

# Vx = Vx << 1
def o_8XYE(c8, op):
    xx = x(op)
    msb = (c8.v[xx] & 0x80) >> 7
    c8.v[0xF] = msb
    c8.v[xx] = c8.v[xx] << 1

# skip on unequal
def o_9XY0(c8, op):
    if c8.v[x(op)] != c8.v[y(op)]:
        c8.pc += 2

# I = nnn
def o_ANNN(c8, op):
    c8.i = nnn(op)

# Jump to nnn+V0
def o_BNNN(c8, op):
    c8.pc = c8.v[0] + nnn(op)

#TODO quirk?

# Vx = nn & rand
def o_CXNN(c8, op):
    c8.v[x(op)] = random.randint(0, 256) & nn(op)

# draw TODO
def o_DXYN(c8, op):
    nn = n(op)
    offset = 16 if nn == 0 else nn
    sprite = c8.memory[c8.i:c8.i + offset]
    c8.v[0xF] = c8.display.draw(c8.v[x(op)], c8.v[y(op)], sprite)
    '''
    c8.v[0xF] = 0
    c8.draw_flag = True
    for yline in range(n(op)):
        row_byte = c8.memory[c8.i + (8*yline)]
        yc = (c8.v[y(op)] + yline) %32
        for xline in range(8):
            xc = (c8.v[x(op)] + xline) % 64
            fb = (yc * 32) + xc
            pixel = row_byte & (0x80 >> xline)
            if pixel == 1 and c8.display.frame_buffer[fb] == 1:
                c8.v[0xF] = 1
                c8.display.frame_buffer[fb] = 0
            elif pixel == 1:
                c8.display.frame_buffer[fb] = 1

    c8.pc += 2
    '''
#TODO hi-res mode

# skip if key==Vx
def o_EX9E(c8, op):
    if c8.key[c8.v[x(op)]]:
        c8.pc += 2

# skip if key!=Vx
def o_EXA1(c8, op):
    if not c8.key[c8.v[x(op)]]:
        c8.pc += 2

def o_F000(c8, op):
    c8.i = (c8.memory[c8.pc] << 8) | c8.memory[c8.pc + 1]
    c8.pc += 2

def o_FX01(c8, op):
    #TODO
    pass
def o_FX02(c8, op):
    #TODO
    pass


# set Vx = to delay timer
def o_FX07(c8, op):
    c8.v[x(op)] = c8.delay

# Wait for key
def o_FX0A(c8, op):
    k = c8.getKey()
    if k <= 0 and k < 17:
        c8.v[x(op)] = k
    else:
        c8.pc -= 2

# set delay
def o_FX15(c8, op):
    c8.delay = c8.v[x(op)]

# set sound
def o_FX18(c8, op):
    c8.sound = c8.v[x(op)]

# I += Vx
def o_FX1E(c8, op):
    c8.i += c8.v[x(op)]

# set i to sprite location
def o_FX29(c8, op):
    c8.i = 0x50 + (5 * c8.v[x(op)])

# 
def o_FX33(c8, op):
    val = c8.v[x(op)]
    c8.memory[c8.i + 2] = val % 10
    val /= 10
    c8.memory[c8.i + 1] = val % 10
    val /= 10
    c8.memory[c8.i] = val % 10

# store registers 0-x in mem
def o_FX55(c8, op):
    addr = c8.i
    lim = x(op) + 1
    for n in range(lim):
        c8.memory[addr + n] = c8.v[n]

# read mem into register 0-x
def o_FX65(c8, op):
    addr = c8.i
    lim = x(op) + 1
    for n in range(lim):
        c8.v[n] = c8.memory[addr + n]

#table helpers
def table0(c8, op): 
    yy = y(op)
    if yy < 0xE:
        opTable0Y[yy](c8, op)
    else: 
        opTable0NN[nn(op)](c8, op)

def table5(c8, op): opTable5[n(op)](c8, op)
def table8(c8, op): opTable8[n(op)](c8, op)
def tableE(c8, op): opTableE[n(op)](c8, op)
def tableF(c8, op): opTableF[nn(op)](c8, op)

###
optable = {
        0x0: table0,
        0x1: o_1NNN,
        0x2: o_2NNN,
        0x3: o_3XNN,
        0x4: o_4XNN,
        0x5: table5,
        0x6: o_6XNN,
        0x7: o_7XNN,
        0x8: table8,
        0x9: o_9XY0,
        0xA: o_ANNN,
        0xB: o_BNNN,
        0xC: o_CXNN,
        0xD: o_DXYN,
        0xE: tableE,
        0xF: tableF
        }
opTable0Y = {
        0x1: o_001N,
        0xB: o_00BN,
        0xC: o_00CN,
        0xD: o_00BN
        }
opTable0NN = {
        0xE0: o_00E0,
        0xEE: o_00EE,
        0xFA: o_00FA,
        0xFB: o_00FB,
        0xFC: o_00FC,
        0xFE: o_00FE,
        0xFF: o_00FF
        }
opTable5 = {
        0x0: o_5XY0,
        0x2: o_5XY2,
        0x3: o_5x03
        }
opTable8 = {
        0x0: o_8XY0,
        0x1: o_8XY1,
        0x2: o_8XY2,
        0x3: o_8XY3,
        0x4: o_8XY4,
        0x5: o_8XY5,
        0x6: o_8XY6,
        0x7: o_8XY7,
        0xE: o_8XYE
        }
opTableE = {
        0x1: o_EXA1,
        0xE: o_00EE
        }
opTableF = {
        0x01: o_FX01,
        0x02: o_FX02,
        0x07: o_FX07,
        0x0A: o_FX0A,
        0x15: o_FX15,
        0x18: o_FX18,
        0x1E: o_FX1E,
        0x29: o_FX29,
        0x33: o_FX33,
        0x55: o_FX55,
        0x65: o_FX65,
        }
