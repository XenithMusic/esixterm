import unittest,inspect

def passingStr(*args,backs=1):
    level = inspect.currentframe()
    for i in range(backs):
        level = level.f_back
    print(f"\033[32mPassing {level.f_code.co_name}!",*args,"\033[0m")

class TestDText(unittest.TestCase):
    def render_equal(self,torender,equal):
        import DText
        rendered = DText.renderDText(torender)
        self.assertEqual(rendered,equal)
        passingStr(rendered,backs=2)
    def test_renderBISU(self):
        self.render_equal("[b]b[/b][i]i[/i][s]s[/s][u]u[/u][b][i][s]`[u]bisu[/u]`[/s][/i][/b]","§b§b§i§i§s§s§u§u§bis§`[u]bisu[/u]`")
    def test_renderColor(self):
        self.render_equal("[color=red]test[/color]","§31§test")
    def test_renderColorNest(self):
        self.render_equal("[color=red]test[color=lime]test[/color]test[/color]","§31§test§32§test§31§test")
    def test_renderSpoiler(self):
        self.render_equal("[spoiler]test[/spoiler]","§90;100§test")
    def test_renderQuote(self):
        self.render_equal("[quote]test[/quote]test","\n§107d§  test\n§§test")

class TestColoredString(unittest.TestCase):
    def test_generics(self):
        from ColoredString import CString
        from TermUtils import printw
        printw(CString("§90;100§test"),"from [spoiler]test[/spoiler]")
        printw(CString("§b§b§i§i§s§s§u§u§bis§`[u]bisu[/u]`"),"from [b]b[/b][i]i[/i][s]s[/s][u]u[/u][b][i][s]`[u]bisu[/u]`[/s][/i][/b]")
        printw(CString("§31§test"),"from [color=red]test[/color]")
        printw(CString("§31§test§32§test§31§test"),"from [color=red]test[color=lime]test[/color]test[/color]")
if __name__ == "__main__":
    unittest.main()