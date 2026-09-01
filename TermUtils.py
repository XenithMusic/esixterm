import math
import textwrap,sys,tty,termios
from ColoredString import *
def clear(fn=print):
    """
    Clears the screen. This also clears scrollback.
    """
    fn("\033[2J\033[3J\033[H",end="")
def movup(x,fn=print):
    """
    Moves the cursor up.

    Args:
        x:int   How much to move the cursor by.
    """
    fn(f"\033[{x}A",end="")
def movdown(x,fn=print):
    """
    Moves the cursor down.

    Args:
        x:int   How much to move the cursor by.
    """
    fn(f"\033[{x}B",end="")
def movright(x,fn=print):
    """
    Moves the cursor right.

    Args:
        x:int   How much to move the cursor by.
    """
    fn(f"\033[{x}C",end="")
def movleft(x,fn=print):
    """
    Moves the cursor left.

    Args:
        x:int   How much to move the cursor by.
    """
    fn(f"\033[{x}D",end="")
def curx(x,fn=print):
    """
    Sets the cursor x position.

    Args:
        x:int   New x position.
    """
    fn(f"\033[{x}G",end="")
def cury(x,fn=print):
    """
    Sets the cursor y position.

    Args:
        x:int   New y position.
    """
    fn(f"\033[{x}d",end="")
def savecur(fn=print):
    """
    Saves the cursor position.
    """
    fn(f"\033[s",end="")
def loadcur(fn=print):
    """
    Loads the cursor position.
    """
    fn(f"\033[u",end="")
def printw(*values,sep=CString(" "),end=CString("\n"),flush=False,wrapLen=-1,movedLines=0):
    """
    Prints a wrapped CString.

    Args:
        *values         A list of values to print.
        sep:CString     Emitted between each value.
        end:CString     Emitted at the end of all values.
        flush:bool      Whether or not to flush stdout.
        wrapLen:int     Wrap length. Set to -1 to disable.
        movedLines:int  What to add to the return value.
    
    Returns:
        movedLines:int  How many lines were added.
    """
    if wrapLen == -1:
        wrapLen = 9999999
    s = sep.join([CString.from_val(x) for x in values])
    s = s.wrap(wrapLen)
    s = CString("\n").join(s)
    outstr = s.parse() + end.parse()
    print(outstr,end="",flush=flush)
    return outstr.count("\n")+movedLines
def prints(*values,sep=" ",end="\n",flush=False,movedLines=0):
    """
    Prints a string, with movedLines.

    Args:
        *values         A list of values to print.
        sep:str         Emitted between each value.
        end:str         Emitted at the end of all values.
        flush:bool      Whether or not to flush stdout.
        movedLines:int  What to add to the return value.
    
    Returns:
        movedLines:int  How many lines were added.
    """
    s = sep.join([str(x) for x in values])
    outstr = s + end
    print(outstr,end="",flush=flush)
    return outstr.count("\n") + movedLines
def inputc(prompt:str,commandHistory:list[str]=[],end="\n"):
    """
    Custom input that has command history.

    Args:
        prompt:str                  Prompt to show at the start of the input field.
        commandHistory:list[str]    List of strings apart of the command history.
        end:str                     Printed after enter is pressed.
    
    Returns:
        Typed text
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        typed = ""
        hist = commandHistory.copy()
        hist.append("")
        hist.reverse()
        historyIndex = 0
        cursorPos = 0
        def readseq():
            seq = "\x1b"
            c = sys.stdin.read(1)
            seq += c
            if c == "[":
                while not c.isalpha():
                    c = sys.stdin.read(1)
                    seq += c
            return seq
        def redraw():
            print("\r\033[K", end="",flush=False)       # beginning of line + clear it
            print(prompt + typed, end="", flush=False)
            curx(len(prompt) + cursorPos + 1)
            sys.stdout.flush()
        redraw()
        while True:
            c = sys.stdin.read(1)
            if c == "\x1b":
                seq = readseq()
                if seq == "\x1b[A": # up
                    historyIndex = min(len(hist)-1,historyIndex+1)
                    typed = hist[historyIndex]
                    cursorPos = len(typed)
                elif seq == "\x1b[B": # down
                    historyIndex = max(0,historyIndex-1)
                    typed = hist[historyIndex]
                    cursorPos = len(typed)
                elif seq == "\x1b[C": # right
                    cursorPos = min(cursorPos+1,len(typed))
                elif seq == "\x1b[D": # left
                    cursorPos = max(cursorPos-1,0)
                elif seq == "\x1b[1;5C": # ctrl right
                    typed = "page fore"
                    break
                elif seq == "\x1b[1;5D": # ctrl left
                    typed = "page back"
                    break
                elif seq in ["\x1b[1;5A"]: # ctrl up
                    typed = "l s"
                    break
                elif seq in ["\x1b[1;5B"]: # ctrl down
                    typed = "l p"
                    break
            elif c in ["\r","\n"]:
                break
            elif c in ["\x7f","\x08"]:
                if cursorPos > 0:
                    typed = typed[:cursorPos-1] + typed[cursorPos:]
                    cursorPos -= 1
            else:
                typed = typed[:cursorPos] + c + typed[cursorPos:]
                cursorPos += 1
            hist[historyIndex] = typed
            redraw()
    finally:
        termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
    print("",end=end)
    return typed