
from .graphical import WHITE, BLACK, pygame

pygame.font.init()

FONT_NAME = "dejavuserif"
FONT_SIZE = 30
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

VIOLET = "#946C94"


class Option:
    def __init__(self, pos, text, size, color, funcs, high_color=WHITE, midst=False, leng=None):
        global FONT_NAME
        self.pos = pos
        self.text = text
        self.size = size
        self.color = color
        self.funcs = funcs
        self.high_color = high_color
        self.font = pygame.font.SysFont(FONT_NAME, self.size)
        self.surface = self.font.render(self.text, True, self.color)
        self.ssize = self.surface.get_size()
        self.highlighted = False
        self.ender = None
        if midst:
            self.midst(leng)

    def highlight(self):
        if not self.highlighted:
            hfont = pygame.font.SysFont(FONT_NAME, self.size+2)
            self.surface = hfont.render(self.text, True, self.high_color)
            self.highlighted = True

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

    def is_focused(self):
        mx, my = pygame.mouse.get_pos()
        px, py = self.pos
        sx, sy = self.ssize
        if mx in range(px, px+sx) and my in range(py, py+sy):
            return True
        else:
            return False

    def is_clicked(self):
        if pygame.mouse.get_pressed()[0]:
            return self.is_focused()

    def reset(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.highlighted = False

    def on_focus(self):
        self.highlight()

    def on_click(self):
        for func in self.funcs:
            args = self.funcs[func]
            func(*args)
            pygame.event.pump()
            return True

    def on_unfocus(self):
        self.reset()

    def exist(self, screen, focus_color=(255, 255, 255)):
        self.draw(screen)
        if self.is_clicked():
            return self.on_click()
        if self.is_focused():
            self.on_focus()
        else:
            if self.highlighted:
                self.on_unfocus()

    def midst(self, leng):
        self.pos = ((leng-self.ssize[0])//2, self.pos[1])


class InformingText:
    def __init__(self, pos, text, size, color, midst=False, leng=None):
        global FONT_NAME
        self.pos = pos
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont(FONT_NAME, self.size)
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.ssize = self.surface.get_size()
        if midst:
            self.midst(leng)

    def exist(self, screen):
        screen.blit(self.surface, self.pos)

    def midst(self, leng):
        self.pos = ((leng-self.ssize[0])//2, self.pos[1])


class Menu:
    def __init__(self, color, widgets, clean=True):
        self.color = color
        self.widgets = widgets
        self.clean = clean
        self.options = [
            widget for widget in self.widgets if type(widget) is Option]
        self.texts = [
            widget for widget in self.widgets if type(widget) is InformingText]
    
    def waitfor_unpress(self):
        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            pass

    def init_enders(self, texts):
        for widget in self.widgets:
            if widget.text in texts:
                widget.ender = True

    def draw(self, screen):
        self.waitfor_unpress()
        clock = pygame.time.Clock()
        while True:
            pygame.event.pump()
            for option in self.options:
                if option.exist(screen):
                    self.waitfor_unpress()
                    pygame.event.pump()
                    if option.ender:
                        return
            for text in self.texts:
                text.exist(screen)
            pygame.display.flip()
            clock.tick(60)
            if self.clean:
                screen.fill(WHITE)
                screen.fill(self.color)
