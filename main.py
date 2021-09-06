import curses
import sys
from chip8 import Chip8

def main():
    try:
        rom = sys.argv[1]
    except:
        rom = "roms/ibm_logo.ch8"

    c = Chip8(rom)

    try:
        curses.wrapper(c.loop)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
