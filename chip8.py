import time
import curses
from opcodes import optable
from display import Display

class Chip8:
    """Chip-8"""

    def __init__(self, rom):
        self.__PCSTART = 0x200
        self.pc = self.__PCSTART
        self.v = [0] * 16
        self.i = 0
        self.memory = [0] * 4096
        self.display = None
        #self.draw_flag = True
        self.delay = 0
        self.sound = 0
        self.stack = []
        self.reset_keys = -1
        self.key_map = {
            '1': 1,
            '2': 2,
            '3': 3,
            'q': 4,
            'w': 5,
            'e': 6,
            'a': 7,
            's': 8,
            'd': 9,
            'z': 0xA,
            'x': 0,
            'c': 0xB,
            '4': 0xC,
            'r': 0xD,
            'f': 0xE,
            'v': 0xF
        }

        self.key_status = [False] * 16

        # Load fonts into memory
        #fontset = [
        self.memory[0:79] = [
               0xF0, 0x90, 0x90, 0x90, 0xF0, #0
               0x20, 0x60, 0x20, 0x20, 0x70, #1
               0xF0, 0x10, 0xF0, 0x80, 0xF0, #2
               0xF0, 0x10, 0xF0, 0x10, 0xF0, #3
               0x90, 0x90, 0xF0, 0x10, 0x10, #4
               0xF0, 0x80, 0xF0, 0x10, 0xF0, #5
               0xF0, 0x80, 0xF0, 0x90, 0xF0, #6
               0xF0, 0x10, 0x20, 0x40, 0x40, #7
               0xF0, 0x90, 0xF0, 0x90, 0xF0, #8
               0xF0, 0x90, 0xF0, 0x10, 0xF0, #9
               0xF0, 0x90, 0xF0, 0x90, 0x90, #A
               0xE0, 0x90, 0xE0, 0x90, 0xE0, #B
               0xF0, 0x80, 0x80, 0x80, 0xF0, #C
               0xE0, 0x90, 0x90, 0x90, 0xE0, #D
               0xF0, 0x80, 0xF0, 0x80, 0xF0, #E
               0xF0, 0x80, 0xF0, 0x80, 0x80  #F
               ]

        r = open(rom, "rb").read()
        self.memory[512:512+len(r)] = r

        self.quirks = {
            'shift': True,
            'load_store': True
        }

    def timers(self):
        if self.sound > 0:
            #TODO emit sound
            self.sound -= 1
        if self.delay > 0:
            self.delay -= 1

    def fetch(self):
        ins = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        return ins

    def getkey(self):
        if self.reset_keys >= 0:
            self.reset_keys -= 1

        if self.reset_keys == 0:
            self.key_status = [False] * 16

        while True:
            try:
                key = self.display.stdscr.getkey()
            except curses.error:
                break
            else:
                if key in self.key_map:
                    self.key_status[self.key_map[key]] = True
                self.reset_keys = 20

    def loop(self, stdscr):
        self.display = Display(stdscr)
        while True:
            time.sleep(0.003)
            self.getkey()
            ins = self.fetch()
            try:
                optable[(ins & 0xF000) >> 12](self, ins)
            except KeyError:
                #exit(f"{ins} not valid")
                print(f"{ins} not valid")
                pass
            self.timers()
