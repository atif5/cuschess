
import pygame
import time

pygame.font.init()

FONT_NAME = "dejavuserif"
FONT_SIZE = 30
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

WHITE = "#FFFFFF"
BLACK = "#000000"


class Option:
    def __init__(self, pos, text, size, color, funcs):
        global FONT_NAME
        self.pos = pos
        self.text = text
        self.size = size
        self.color = color
        self.funcs = funcs
        self.font = pygame.font.SysFont(FONT_NAME, self.size)
        self.surface = self.font.render(self.text, True, self.color)
        self.ssize = self.surface.get_size()
        self.highlighted = False
        self.ender = None

    def highlight(self, color):
        if not self.highlighted:
            hfont = pygame.font.SysFont(FONT_NAME, self.size+2)
            self.surface = hfont.render(self.text, True, color)
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
            print(f"clicked on {self.text}")
            return self.is_focused()

    def reset(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.highlighted = False

    def on_focus(self, color):
        self.highlight(color)

    def on_click(self):
        for func in self.funcs:
            args = self.funcs[func]
            func(*args)

    def on_unfocus(self):
        self.reset()

    def exist(self, screen, focus_color=(255, 255, 255)):
        self.draw(screen)
        if self.is_clicked():
            self.on_click()
            if self.ender:
                return True
        if self.is_focused():
            self.on_focus(focus_color)
        else:
            if self.highlighted:
                self.on_unfocus()


class InformingText:
    def __init__(self, pos, text, size, color, midst=False, screen=None):
        global FONT_NAME
        self.pos = pos
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont(FONT_NAME, self.size)
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.ssize = self.surface.get_size()
        if midst:
            self.midst(screen)

    def exist(self, screen):
        screen.blit(self.surface, self.pos)

    def midst(self, screen):
        x = screen.get_size()[0]
        self.pos = ((x-self.ssize[0])//2, self.pos[1])


class Menu:
    def __init__(self, color, widgets, screen, clean=True):
        self.color = color
        self.widgets = widgets
        self.screen = screen
        self.clean = clean

    def init_enders(self, texts):
        for widget in self.widgets:
            if widget.text in texts:
                widget.ender = True

    def draw(self):
        clock = pygame.time.Clock()
        while True:
            pygame.event.pump()
            for widget in self.widgets:
                if widget.exist(self.screen):
                    pygame.event.pump()
                    print("menu ended.")
                    return
                pygame.event.pump()
            pygame.display.flip()
            clock.tick(60)
            if self.clean:
                self.screen.fill(WHITE)
                self.screen.fill(self.color)
