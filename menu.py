
import pygame

pygame.font.init()

FONT_NAME = "dejavuserif"
FONT_SIZE = 30
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)


class ModeOption:
    def __init__(self, pos, text, size, color, mode):
        global FONT
        self.pos = pos
        self.text = text
        self.size = size
        self.color = color
        self.mode = mode
        self.surface = FONT.render(self.text, True, self.color)
        self.ssize = self.surface.get_size()
        self.highlighted = False

    def highlight(self, color):
        hfont = pygame.font.SysFont(FONT_NAME, FONT_SIZE+2)
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
            return self.is_focused()

    def reset(self):
        self.surface = FONT.render(self.text, True, self.color)
        self.highlighted = False

    def on_focus(self, color):
        self.highlight(color)

    def on_click(self, screen):
        if self.text == "Run a server":
            pygame.quit()
            self.mode()
        else:
            self.mode(screen)

    def on_unfocus(self):
        self.reset()

    def exist(self, screen, focus_color=(255, 255, 255)):
        self.draw(screen)
        if self.is_clicked():
            self.on_click(screen)
        if self.is_focused():
            self.on_focus(focus_color)
        else:
            if self.highlighted:  
                self.on_unfocus()





