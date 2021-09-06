import curses

BLOCK = "█"
SPACE = " "

class Display:
    def __init__(self, stdscr):
        self.w = 64
        self.h = 32
        self.stdscr = stdscr
        self.tallM = False
        self.hi_resM = False
        curses.curs_set(False)
        self.stdscr.nodelay(True)

        self.check()
        self.clear()

    def check(self):
        curses.update_lines_cols()
        if curses.LINES < self.h // 2 or curses.COLS < self.w:
            raise curses.error("CHIP-8 needs at least " + str(self.h // 2) + 
                    " lines and " + str(self.w) + " cols, got " + 
                    str(curses.LINES) + " and " + str(curses.COLS))

    #def hi_res(self):
    #def lo_res(self):
    def scroll(self, direction, pixels):
        pass
        
    def clear(self):
        self.stdscr.erase()
        self.stdscr.refresh()

    def draw(self, x, y, sprite):
        colision = 0
        y = y % self.h
        x = x % self.w
        #TODO if hi_resM

        for row, num in enumerate(sprite):
            if y + row > self.h:
                break
            for col in range(8):
                if (num >> (7 - col)) & 1:
                    if x + col > self.w:
                        break
                    if (y + row) % 2 == 0:
                        if self.stdscr.inch((y + row) // 2, x + col) & curses.A_CHARTEXT == 128: #upper
                            collision = 1 # TODO QUIRK
                            self.stdscr.addch((y + row) // 2, x + col, SPACE)
                        elif self.stdscr.inch((y + row) // 2, x + col) & curses.A_CHARTEXT == 132: #lower
                            self.stdscr.addch((y + row) // 2, x + col, BLOCK)
                        elif self.stdscr.inch((y + row) // 2, x + col) & curses.A_CHARTEXT == 136: #full
                            collision = 1 # TODO QUIRK
                            self.stdscr.addch((y + row) // 2, x + col, "▄")
                        else:
                            self.stdscr.addch((y + row) // 2, x + col, "▀")
                    else:
                        if self.stdscr.inch((y + row) // 2, x + col) & curses.A_CHARTEXT == 128: #upper
                            self.stdscr.addch((y + row) // 2, x + col, BLOCK)
                        elif self.stdscr.inch((y + row) // 2, x + col) & curses.A_CHARTEXT == 132: #lower
                            collision = 1 # TODO QUIRK
                            self.stdscr.addch((y + row) // 2, x + col, SPACE)
                        elif self.stdscr.inch((y + row) // 2, x + col) & curses.A_CHARTEXT == 136: #full
                            collision = 1 # TODO QUIRK
                            self.stdscr.addch((y + row) // 2, x + col, "▀")
                        else:
                            self.stdscr.addch((y + row) // 2, x + col, "▄")

        self.stdscr.refresh()
        return colision
