from os import name as osname, path 
from sys import argv, stdin, stdout
import readline


class _Getch:
    def __init__(self) -> None:

        if osname == "posix":
            self.ch = _GetchUnix()
        elif osname == "nt":
            self.ch = _GetchWin()

    def __call__(self): return self.ch()



class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import tty,termios
        fd = stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(stdin.fileno())
            char = stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return char



class _GetchWin:
    def __init__(self) -> None:
        pass

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def read(filename):
    if path.isfile(filename):
        f = open(filename, 'r')
        interpreter(f.read())
        f.close
    else:
        interpreter(filename)

def clean(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def buildbracemap(code):
    temp, bracemap = [], {}

    for pos, char in enumerate(code):
        if char == '[': temp.append(pos)
        if char == ']':
            if not temp:
                print("Error: Mismatched brackets at position", pos)
                return {}
            start = temp.pop()
            bracemap[start] = pos
            bracemap[pos] = start

    if temp:
        print("Error: Unclosed brackets at positions", temp)
        return {}

    return bracemap



def interpreter(code):

    code = clean(list(code))
    bracemap = buildbracemap(code)
    getch = _Getch()

    cells, ptr, cellptr = [0], 0, 0

    while ptr < len(code):
        command = code[ptr]

        if command == '>':
            cellptr += 1
            if cellptr == len(cells): cells.append(0)
        elif command == '<':
            cellptr = 0 if cellptr <= 0 else cellptr - 1
        if command == "+":
          cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

        if command == "-":
          cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

        if command == "[" and cells[cellptr] == 0: ptr = bracemap[ptr]
        if command == "]" and cells[cellptr] != 0: ptr = bracemap[ptr]
        if command == ".": stdout.write(chr(cells[cellptr]))
        if command == ",": cells[cellptr] = ord(getch())
          
        ptr += 1


def usage():
    error_message = f"Error: Invalid command line arguments \n" \
                    f"Usage: {argv[0]} com <filename> \n" \
                    f"  brainfuck.py -> Run in interpreter mode\n" \
                    f"  brainfuck.py com <filename> -> Interpret code from file\n" \

    print(error_message)
    exit(1)



def main():
    if len(argv) == 1:
        try:
            readline.read_history_file('history.txt')
        except FileNotFoundError:
            pass  # Ignore if there's no history file yet

        readline.set_history_length(1000)  # Adjust the number of history entries to keep
        
        count = 0
        while True:
            try:
                command = input("bf [%s] # " % count)
                if command.lower() == "exit" or command.lower() == "quit":
                    exit()
                elif command.lower() == "help":
                    print("\nBrainfuck Live Interpreter")
                    print("Commands:")
                    print("  - Type 'exit' or 'quit' or 'Ctrl-D'to quit.")
                    print("  - Type 'help' for this help message.")
                    print("  - Enter Brainfuck code to interpret.")
                    print("Here is and Hello World! example")
                    print("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
                    print("Just copy and paste")
                    print()
                else:
                    read(command)
                count += 1
            except (KeyboardInterrupt) or (EOFError) as e:
                    print("KeyboardInterrupt %s" % e)
                    print("- Use exit or quit")
                    continue



    elif len(argv) == 2 and argv[1] == "com":
        print("Missing file for interpretation")
        exit(1)

    elif len(argv) == 3 and argv[1] == "com":
        if path.isfile(argv[2]):
            read(argv[2])
        else:
            print("can't open file: '%s' " % path.abspath(argv[2]))
            print("No such file or directory '%s'" % argv[2])
    else:
        usage()
 
    readline.write_history_file('.history.txt')

if __name__ == "__main__":
        try:
            main()
        except EOFError:
            exit()

