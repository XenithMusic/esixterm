import re,wcwidth

class CChar:
    def __init__(self,chr:str,col:str|int,bold:bool=False,italic:bool=False,strike:bool=False,under:bool=False,dark:bool=False,hyperlink:str=""):
        assert len(chr) == 1 or len(chr) == 0
        self.chr = chr
        self.col = col
        self.bold = bold
        self.italic = italic
        self.strike = strike
        self.under = under
        self.dark = dark
        self.hyperlink = hyperlink
    def __len__(self):
        wid = wcwidth.wcwidth(self.chr)
        return 2 if wid < 0 else wid
    def getAnsi(self) -> str:
        ansis = [0]
        if self.chr != "" or self.col != 0:
            ansis += [self.col]
            if self.bold: ansis += [1]
            if self.italic: ansis += [3]
            if self.strike: ansis += [9]
            if self.under: ansis += [4]
            if self.dark: ansis += [30]
        ansistr = ""
        ansistr += ";".join([str(x) for x in ansis])
        return f"\033[{ansistr}m" + (f"\033]8;;{self.hyperlink}\033\\" if self.hyperlink != "" else "")
    def getChr(self) -> str:
        return self.chr
    def getCode(self) -> str:
        codestr = str(self.col)
        if self.bold: codestr += "b"
        if self.dark: codestr += "d"
        return f"§{codestr}§"

class CString:
    """
    Colored strings.

    Usage:
        "§(ansiColorCode)(flags)§color" results in a colored string.
        Multiple color codes can be specified, like §30;41§
    Flags:
        b: bold
        i: italic
        s: strikethrough
        u: underline
        d: dark foreground (equivalent to a color of 30)
    """
    def __init__(self,text:str):
        self.chrs = []
        self.set_text(text)
    @classmethod
    def from_chrs(cls,chrs:list[CChar]) -> CString:
        a = cls("")
        a.chrs = chrs
        return a
    @classmethod
    def from_val(cls,val) -> CString:
        if isinstance(val,CString): return val
        if isinstance(val,str): return CString(val)
        return CString(str(val))
    def join(self,vals:list[CString]) -> CString:
        final = CString("")
        for i,v in enumerate(vals):
            final += CString.from_val(v)
            if i != len(vals)-1: final += self
        return final
    def set_text(self,text:str):
        activeColor = 0
        activeHyperlink = ""
        bold = False
        italic = False
        strike = False
        under = False
        dark = False # used if fg is false, makes fg color black instead of white
        while len(text) >= 1:
            while text.startswith("§"):
                match = re.search(r"§.*?§", text)
                match = match[0]
                if not ">" in match:
                    bold = False
                    italic = False
                    strike = False
                    under = False
                    dark = False
                    activeHyperlink = ""
                if match == None:
                    raise RuntimeError("couldn't find ending § in color string")
                toSkip = len(match)
                match = match.replace("§","")
                match,sep,hyperlink = match.partition("|")
                if "b" in match:
                    bold = not bold
                if "i" in match:
                    italic = not italic
                if "s" in match:
                    strike = not strike
                if "u" in match:
                    under = not under
                if "d" in match:
                    dark = not dark
                toRemove = list("bisud>")
                for i in toRemove:
                    match = match.replace(i,"")
                if sep != "":
                    activeHyperlink = hyperlink
                if match == "": match = "0"
                activeColor = match
                text = text[toSkip:]
            if len(text) == 0: break
            chr = text[0]
            text = text[1:]
            self.chrs += [CChar(chr,activeColor,bold,italic,strike,under,dark,activeHyperlink)]
    def parse(self,fn=CChar.getAnsi):
        final = ""
        pushAnsi = True
        for i,chr in enumerate(self.chrs):
            if len(self.chrs)-1 > i+1:
                nextchr = self.chrs[i+1]
            else:
                nextchr = CChar("",0,False)
            if pushAnsi:
                final += fn(chr)
            final += chr.getChr()
            pushAnsi = fn(chr) != fn(nextchr)
            if pushAnsi:
                final += "\033]8;;\033\\"
        return final
    def halfparse(self):
        return self.parse(CChar.getCode)
    def __getitem__(self, key:int):
        return CString.from_chrs(self.chrs[key])
    def first(self,chr:str):
        for i,v in enumerate(self.chrs):
            if v.chr == chr: return i
    def last(self,chr:str):
        for i,v in enumerate(self.chrs[::-1]):
            if v.chr == chr: return len(self.chrs) - 1 - i
    def count(self,chr:str):
        ct = 0
        for i in self.chrs:
            if i.chr == chr: ct += 1
        return ct
    def copy(self):
        return CString.from_chrs(self.chrs)
    def __len__(self):
        return sum(len(x) for x in self.chrs)
    def __add__(self, other): # self + other
        if isinstance(other,str):
            other = CString(other)
        return CString.from_chrs(self.chrs + other.chrs)
    def __radd__(self, other): # other + self
        if isinstance(other,str):
            other = CString(other)
        return other + self
    def __repr__(self):
        return self.parse()
    def findSlicePosition(self,pos):
        sliced = self[:pos]
        while len(sliced) > pos:
            sliced = sliced[:-1]
        return len(sliced.chrs)
    def wrap(self,wrapLen=99999):
        text = self.copy()
        lines = []
        hasElipsis = False
        while len(text) >= 1:
            elstr = "…" if hasElipsis else ""
            text = elstr + text
            hasElipsis = False
            slicepos = text.findSlicePosition(wrapLen)
            s:CString = text[:slicepos]
            if len(text) <= wrapLen:
                lines += [s]
                break
            if s.count(" ") == 0:
                lines += [text[:(slicepos-1)] + "…"]
                text = text[(slicepos-1):]
                hasElipsis = True
            else:
                idx = s.last(" ")
                lines += [text[:(idx)]]
                text = text[(idx+1):]
        return lines